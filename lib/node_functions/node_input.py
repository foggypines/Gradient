from ... lib.fusionAddInUtils.general_utils import log
import numpy as np
from dataclasses import dataclass, field

all_node_inputs = {}

@dataclass
class NodeInput():

    gui_id: str
    parameter: np.float64 = field(default_factory=lambda: np.array([0], np.float64))
    linked: bool = False

    def __post__init__(self):

        log(f'parameter val: {self.parameter}')

        self.update(self.parameter)

    def update(self, parameter):

        log(f'input parameter is:       {parameter}')

        if isinstance(parameter, list) or isinstance(parameter, np.ndarray):  

            log('recognized as array')

            self.parameter = parameter
        else:

            log('recognized as singular')

            self.parameter = [parameter]