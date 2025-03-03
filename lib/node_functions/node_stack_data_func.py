import numpy as np
from .node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from dataclasses import dataclass, field

node_name = "StackData"
node_output = "_Output"
node_a_data = "_AData"
node_b_data = "_BData"
node_stack_type_name = "_Stacktype"

@dataclass
class StackDataNodeFunction(BaseNodeFunction):

    node_a_data: NodeInput = field(default = None)
    node_b_data: NodeInput = field(default = None)
    stack_type: NodeInput = field(default = None)
    result: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        super().__post_init__()

        if self.node_a_data is None:

            self.node_a_data = self.add_input(node_a_data)

        if self.node_b_data is None:

            self.node_b_data = self.add_input(node_b_data)

        if self.stack_type is None:

            self.stack_type = self.add_input(node_stack_type_name, ui_element=True)

    def compute(self, sender=None, app_data=None):

        stack_type = self.parameter_update(input = self.stack_type,
                                            input_name = node_stack_type_name,
                                            val = self.stack_type.parameter[0])

        if stack_type == 0:

            self.result = np.vstack((self.node_a_data.parameter, self.node_b_data.parameter))

        elif stack_type == 1:

            self.result = np.hstack((self.node_a_data.parameter, self.node_b_data.parameter))

        elif stack_type == 2:
            
            self.result = np.column_stack((self.node_a_data.parameter, self.node_b_data.parameter))

        self.output.payload = self.result