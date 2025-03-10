import numpy as np
from . node_base_func import BaseNodeFunction
from . node_input import NodeInput
from dataclasses import dataclass, field

node_name = "NodeCrossProduct"
node_output = "_Output"
node_a_vector = "_AVector"
node_b_vector = "_BVector"

@dataclass
class CrossProductNodeFunction(BaseNodeFunction):

    a_vector: NodeInput = field(default=None)
    b_vector: NodeInput = field(default=None)
    result: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self):
        super().__post_init__()

        if self.a_vector is None:
            self.a_vector = self.add_input(node_a_vector, required=True)

        if self.b_vector is None:
            self.b_vector = self.add_input(node_b_vector, required=True)

    def compute(self, sender=None, app_data=None):

        a = self.a_vector.parameter

        b = self.b_vector.parameter

        a_len = len(a)

        b_len = len(b)

        if a_len == b_len:

            self.result = np.zeros((a_len, 3), np.float64)

            for i in range(a_len):

                v1 = a[i]

                v2 = b[i]
             
                self.result[i] = np.cross(v1, v2)

        self.output.payload = self.result