import numpy as np
import numexpr as ne
import dearpygui.dearpygui as dpg
from . node_base_func import BaseNodeFunction
from . node_input import NodeInput, all_node_inputs
from ... lib.utility import append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "NodeExpression"
node_output = "_Output"
node_a_var = "_AVar"
node_b_var = "_BVar"
node_expression = "_Expression"

@dataclass
class ExpressionNodeFunction(BaseNodeFunction):

    a_var: NodeInput = field(default = None)
    b_var: NodeInput = field(default = None)
    expression: NodeInput = field(default = None)
    result: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        super().__post_init__()

        if self.a_var is None:

            self.a_var = self.add_input(node_a_var, required=False)

        if self.b_var is None:

            self.b_var = self.add_input(node_b_var, required=False)

        if self.expression is None:

            self.expression =  self.add_input(node_expression, ui_element=True)

    def compute(self, sender=None, app_data=None):

        expr = dpg.get_value(append_value(self.gui_id + node_expression))

        self.expression.parameter = expr

        if expr != "":

            a = self.a_var.parameter

            b = self.b_var.parameter

            pi = np.pi # for easy reference in the expression string

            self.result = ne.evaluate(expr)

            if self.result.size == 1:

                self.result = self.result.item()

            self.output.payload = self.result

            # log(f'Result: {self.result}')

            # for link in self.links:

            #     log(f'link start: {link.start}')

            #     node_input = all_node_inputs[link.end]

            #     node_input.update(self.result)

            # if sender is not None:

            #     self.broadcast_changes()