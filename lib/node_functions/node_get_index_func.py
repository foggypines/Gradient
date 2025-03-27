import numpy as np
from .node_base_func import BaseNodeFunction
from .node_input import NodeInput
from dataclasses import dataclass, field

node_name = "GetIndex"
data_name = "_Data"
index_name = "_Index"

@dataclass
class GetIndexNodeFunction(BaseNodeFunction):

    node_data: NodeInput = field(default=None)
    node_index: NodeInput = field(default=None)
    result: np.float64 = field(default_factory=lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        super().__post_init__()

        if self.node_data is None:

            self.node_data = self.add_input(data_name)

        if self.node_index is None:

            self.node_index = self.add_input(index_name, ui_element=True)

    def compute(self, sender=None, app_data=None):

        data = self.node_data.parameter

        temp_result = []

        for index in self.node_index.parameter:

            if 0 <= index < len(data):

                item = data[index]

                temp_result.append(item)

            else:
                
                temp_result.append(np.nan)  # or handle the error as needed

        self.result = np.array(temp_result)

        self.output.payload = self.result