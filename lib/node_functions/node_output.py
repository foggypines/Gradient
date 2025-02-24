from ... lib.fusionAddInUtils.general_utils import log
import numpy as np
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard

all_node_outputs = {}

@dataclass
class NodeOutput(JSONWizard):

    gui_id: str
    full_id: str
    payload: np.float64 = field(default_factory = lambda: np.array([0], np.float64))
    links: list = field(default_factory = lambda: [])

    def __post_init__(self):

        all_node_outputs[self.full_id] = self