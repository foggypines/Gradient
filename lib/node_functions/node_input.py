from ... lib.fusionAddInUtils.general_utils import log
import numpy as np
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard

all_node_inputs = {}

@dataclass
class NodeInput(JSONWizard):

    gui_id: str
    full_id: str
    parameter: np.float64 = field(default_factory=lambda: np.array([0], np.float64))
    linked: bool = False
    
    #indicates if the node input has a control element that can be used in place of a link to another node
    ui_element: bool = False 

    #indicates if the node input is a required input to it's parent node
    required: bool = True

    def __post_init__(self):

        all_node_inputs[self.full_id] = self

        self.update(self.parameter)

    def update(self, parameter):

        if isinstance(parameter, list) or isinstance(parameter, np.ndarray):  

            self.parameter = parameter

        else:

            self.parameter = [parameter]