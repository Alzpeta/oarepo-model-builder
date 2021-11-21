from oarepo_model_builder.builders.python import PythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioRecordBuilder(PythonBuilder):
    output_builder_type = 'invenio_record'

    def finish(self):
        python_path = self.class_to_path(self.settings.python.record_class)
        self.create_parent_modules(python_path)

        output: PythonOutput = self.builder.get_output(
            'python',
            python_path
        )

        output.merge(
            'record',
            HyphenMunch(settings=self.settings, python=self.settings.python)
        )
