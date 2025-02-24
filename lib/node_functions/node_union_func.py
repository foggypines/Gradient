from .node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from ..utility import prepend_exclamation
from dataclasses import dataclass, field

node_type = prepend_exclamation("Union")

node_a_input = "_node_a_input"
node_b_input = "_node_b_input"

node_output = "_Output"

union_bodies = None

@dataclass
class UnionNodeFunction(BaseNodeFunction):

    node_a_input: NodeInput = field(default_factory=lambda: None)
    node_b_input: NodeInput = field(default_factory=lambda: None)

    def __post_init__(self):

        super().__post_init__()

        if self.node_a_input is None:

            self.node_a_input = self.add_input(input_name=node_a_input)

        if self.node_b_input is None:
            
            self.node_b_input = self.add_input(input_name=node_b_input)

    def compute(self, sender=None, app_data=None):

        union_bodies(self.node_a_input.parameter[0], self.node_b_input.parameter[0], self.gui_id)

        self.output.payload = self.gui_id

        # for link in self.links:

        #     node_input = all_node_inputs[link.end]

        #     node_input.update(self.gui_id)

        # if sender is not None:

        #     self.broadcast_changes()

    def delete(self):

        union_bodies(self.node_a_input.parameter[0], self.node_b_input.parameter[0], self.gui_id, delete = True)