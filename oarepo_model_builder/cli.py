import pathlib

import click
import pkg_resources

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.schema import ModelSchema, deepmerge


@click.command()
@click.option('--output-directory',
              help='Output directory where the generated files will be placed. '
                   'Defaults to "."')
@click.option('--package',
              help='Package into which the model is generated. '
                   'If not passed, the name of the current directory, '
                   'converted into python package name, is used.')
@click.option('--set', 'sets',
              help='Overwrite option in the model file. Example '
                   '--set name=value',
              multiple=True)
@click.option('--config', 'configs',
              help='Load a config file and replace parts of the model with it. '
                   'The config file can be a json, yaml or a python file. '
                   'If it is a python file, it is evaluated with the current '
                   'model stored in the "oarepo_model" global variable and '
                   'after the evaluation all globals are set on the model.',
              multiple=True)
@click.argument('model_filename')
def run(output_directory, package, sets, configs, model_filename):
    """
    Compiles an oarepo model file given in MODEL_FILENAME into an Invenio repository model.
    """
    output_classes = load_entry_points_list('oarepo_model_builder.ouptuts')
    builder_classes = load_entry_points_list('oarepo_model_builder.builders')
    preprocess_classes = load_entry_points_list('oarepo_model_builder.preprocessors')
    transformer_classes = load_entry_points_list('oarepo_model_builder.transformers')
    loaders = load_entry_points_dict('oarepo_model_builder.loaders')

    schema = ModelSchema(model_filename, loaders=loaders)
    for config in configs:
        load_config(schema, config)

    for s in sets:
        k, v = s.split('=', 1)
        schema.schema[k] = v

    if package:
        schema.schema['package'] = package

    builder = ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        output_preprocessors=preprocess_classes,
        transformers=transformer_classes
    )

    builder.build(schema, output_directory)


def load_entry_points_dict(name):
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(group=name)}


def load_entry_points_list(name):
    return [ep.load() for ep in pkg_resources.iter_entry_points(group=name)]


def load_config(schema, config):
    loaded_file = schema._load(config)
    schema.schema = deepmerge(loaded_file, schema.schema, [])


if __name__ == '__main__':
    run()