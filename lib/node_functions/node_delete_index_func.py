import numpy as np
from .node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from dataclasses import dataclass, field

node_name = "DeleteIndexData"
node_output_name = "_Output"
set_name = "_set"
indices_name = "_index"

@dataclass
class DeleteIndexNodeFunction(BaseNodeFunction):

    set: NodeInput = field(default = None)
    indices: NodeInput = field(default = None)
    result: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        super().__post_init__()

        if self.set is None:

            self.set = self.add_input(set_name)

        if self.indices is None:

            self.indices = self.add_input(indices_name)

    def compute(self, sender=None, app_data=None):

        self.result = np.delete(self.set.parameter, self.indices.parameter)

        self.output.payload = self.result

        # for link in self.links:

        #     node_input = all_node_inputs[link.end]

        #     node_input.update(self.result)

        # if sender is not None: 
            
        #     self.broadcast_changes()