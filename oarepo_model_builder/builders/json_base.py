from pathlib import Path

from oarepo_model_builder.builders import OutputBuilder, process
from oarepo_model_builder.builders.utils import ensure_parent_modules
from oarepo_model_builder.utils.stack import ModelBuilderStack


class JSONBaseBuilder(OutputBuilder):
    output_file_name: str = None
    output_file_type: str = None
    parent_module_root_name: str = None

    def model_element_enter(self, stack: ModelBuilderStack):
        top = stack.top
        match stack.top_type:
            case stack.PRIMITIVE:
                self.output.primitive(top.key, top.data)
            case stack.LIST:
                self.output.enter(top.key, [])
            case stack.DICT:
                self.output.enter(top.key, {})

    def model_element_leave(self, stack: ModelBuilderStack):
        if stack.top_type != stack.PRIMITIVE:
            self.output.leave()

    @process('/model')
    def enter_model(self, stack: ModelBuilderStack):
        output_name = stack[0][self.output_file_name]
        self.output = self.builder.get_output(self.output_file_type, output_name)
        ensure_parent_modules(self.builder, Path(output_name), self.parent_module_root_name)
