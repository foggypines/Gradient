import dearpygui.dearpygui as dpg
from ... lib.fusionAddInUtils.general_utils import log
from ... lib.node_functions.node_input import NodeInput, all_node_inputs
from ... lib.node_functions.node_output import NodeOutput, all_node_outputs
from .link import Link
from ... lib.function_node_dict import function_node_dict
from ... lib.utility import *
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard, json_field
from nutree import Tree, IterMethod

node_output = "_Output"

@dataclass(kw_only=True)
class BaseNodeFunction(JSONWizard):

    gui_id: str
    inputs: list[NodeInput] = field(repr=False, default_factory = lambda: [])
    output: NodeOutput = field(default = None)
    outputs: list[NodeOutput] = field(repr=False, default_factory = lambda: [])
    uptodate: bool = field(default = True)
    ui_pos: tuple[int, int] = field(default = (200,200))

    def __post_init__(self):

        if self.output is None:

            self.output = self.add_output(node_output)

        self.outputs.append(self.output)

    def add_input(self, input_name: str, ui_element: bool = False, required: bool = True):

        node_input = NodeInput(gui_id=self.gui_id,
                               full_id=self.gui_id + input_name,
                                ui_element=ui_element,
                                  required=required)

        return node_input
    
    def add_output(self, output_name: str):
        
        node_output = NodeOutput(gui_id = self.gui_id, full_id = self.gui_id + output_name)

        return node_output

    #Validates if all required inputs are linked.
    #This is the default base where all none ui elements are checked
    def inputs_linked(self):

        inputs_linked = True

        for input in self.inputs:

            if input.linked == False and input.ui_element == False and input.required == True:

                inputs_linked = False

        return inputs_linked

    def update(self, sender=None, app_data=None):
        
        if self.inputs_linked():

            self.compute(sender = sender)

            self.set_broadcasts()

            if sender is not None: #only need to run the broadcast method for the first node

                self.broadcast_changes()

    #For each concrete node this method is inherited and is used to data processing.
    def compute(self, sender=None, app_data=None):
        pass

    def set_broadcasts(self):

        for output in self.outputs:

            for link in output.links:

                node_input = all_node_inputs[link]

                node_input.update(output.payload)

    def broadcast_changes(self):

        tree = Tree("chain")

        self.populate_tree(tree = tree, branch = tree)

        tree.print()

        for output in tree.iterator(method = IterMethod.LEVEL_ORDER):

            output_obj = function_node_dict[output.data]

            output_obj.update()

    def populate_tree(self, tree: Tree, branch: Tree):

        for output in self.outputs:

            for node_input_alias in output.links:

                node = simplify_alias(node_input_alias)

                if tree.find(node) is None:
                # if tree.find(output) is None:

                    # new_branch = branch.add(node)

                    new_branch = branch.add(node)

                    output_obj = function_node_dict[node]

                    output_obj.populate_tree(tree = tree, branch = new_branch)

        return tree

    def delete(self):
        pass

    def parameter_update(self, input: NodeInput, input_name: str, val):
        
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

    def set_ui(self, input: NodeInput, input_name: str):
        
        if len(input.parameter) == 1:

            dpg.set_value(append_value(self.gui_id + input_name), input.parameter[0])

        else:

            dpg.set_value(append_value(self.gui_id + input_name), 0)
                    
    def update_ui_pos(self):

        self.ui_pos= dpg.get_item_pos(self.gui_id)

    def sync_ui(self):
        pass