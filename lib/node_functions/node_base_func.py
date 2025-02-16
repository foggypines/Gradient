import dearpygui.dearpygui as dpg
from ... lib.fusionAddInUtils.general_utils import log
from ... lib.node_functions.node_input import NodeInput
from .link import Link
from ... lib.function_node_dict import function_node_dict
from ... lib.utility import *
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from nutree import Tree, IterMethod

@dataclass(kw_only=True)
class BaseNodeFunction(JSONWizard):

    gui_id: str
    outputs: list = field(default_factory=lambda: [])
    links: list[Link] = field(default_factory=lambda: [])
    uptodate: bool = field(default=True)
    ui_pos: tuple[int, int] = field(default=(200,200))

    def compute(self, sender=None, app_data=None):
        pass

    def update(self):

        tree = Tree("chain")

        self.populate_tree(tree = tree, branch = tree)

        tree.print()

        for output in tree.iterator(method = IterMethod.LEVEL_ORDER):

            output_obj = function_node_dict[output.data]

            output_obj.compute()

    def populate_tree(self, tree: Tree, branch: Tree):

        for output in self.outputs:

            if tree.find(output) is None:

                new_branch = branch.add(output)

                output_obj = function_node_dict[output]

                output_obj.populate_tree(tree = tree, branch = new_branch)

        return tree

    # def update(self):

    #     if self.outputs != [] or self.outputs == 0:

    #         for output in self.outputs:

    #             output_obj = function_node_dict[output]

    #             output_obj.compute()

    def parameter_update(self, input, input_name, val):
        
        if input.linked == True:

            if len(input.parameter) == 1:

                dpg.set_value(append_value(self.gui_id + input_name), val)

            else:

                dpg.set_value(append_value(self.gui_id + input_name), 0)

            return val

        else: 

            val = dpg.get_value(append_value(self.gui_id + input_name))

            input.parameter[0] = val

            return val

    def update_input(self, node_input: NodeInput, input_name: str):
        
        if node_input.linked == True:

            dpg.set_value(append_value(self.gui_id + input_name), node_input.parameter)

        else:

            node_input.parameter = dpg.get_value(append_value(self.gui_id + node_input))

    def set_ui(self, input, input_name):
        
        if len(input.parameter) == 1:

            dpg.set_value(append_value(self.gui_id + input_name), input.parameter[0])

        else:

            dpg.set_value(append_value(self.gui_id + input_name), 0)
                    
    def update_ui_pos(self):

        self.ui_pos= dpg.get_item_pos(self.gui_id)

    def sync_ui(self):
        pass