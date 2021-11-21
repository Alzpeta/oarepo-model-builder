from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case, snake_case


def last_item(x):
    return x.rsplit('.', maxsplit=1)[-1]


class InvenioModelPreprocessor(ModelPreprocessor):

    def transform(self, schema, settings):
        deepmerge(settings, {
            'python': {
                'record_prefix': camel_case(settings.package.rsplit('.', maxsplit=1)[-1]),
                # just make sure that the templates is always there
                'templates': {
                },
                'marshmallow': {
                    'top_level_properties': True,
                    'mapping': {
                    }
                }
            }
        })

        record_prefix = settings.python.record_prefix
        self.set(settings.python, 'record-prefix-snake',
                 lambda: snake_case(settings.python.record_prefix))

        self.set(settings.python, 'record-class',
                 lambda: (f'{settings.package}.record.{record_prefix}Record'))
        self.set(settings.python, 'record-schema-class',
                 lambda: (f'{settings.package}.schema.{record_prefix}Schema'))
        self.set(settings.python, 'record-schema-properties-class',
                 lambda: (f'{settings.package}.schema.{record_prefix}PropertiesSchema'))
        self.set(settings.python, 'record-metadata-class',
                 lambda: (f'{settings.package}.metadata.{record_prefix}Metadata'))
        self.set(settings.python, 'record-permissions-class',
                 lambda: (f'{settings.package}.permissions.{record_prefix}PermissionPolicy'))
        self.set(settings.python, 'record-dumper-class',
                 lambda: (f'{settings.package}.dumper.{record_prefix}Dumper'))
        self.set(settings.python, 'record-metadata-table-name',
                 lambda: f'{record_prefix.lower()}_metadata')
        self.set(settings.python, 'record-search-options-class',
                 lambda: (f'{settings.package}.search_options.{record_prefix}SearchOptions'))
        self.set(settings.python, 'record-service-config-class',
                 lambda: (f'{settings.package}.service_config.{record_prefix}ServiceConfig'))
