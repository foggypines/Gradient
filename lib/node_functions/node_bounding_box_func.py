from ... lib.node_functions.node_input import NodeInput
from . node_base_func import BaseNodeFunction
from dataclasses import dataclass, field
from ... lib.utility import prepend_exclamation
import numpy as np

node_name = "boundingbox"
node_type = prepend_exclamation(node_name)

node_center_point_input = "_input_center_point"
node_length_vector_input = "_input_length_vector"
node_width_vector_input = "_input_width_vector"
node_length_input = "_input_length"
node_width_input = "_input_width"
node_height_input = "_input_height"

@dataclass
class BoundingBoxNodeFunction(BaseNodeFunction):
    
    center_point: NodeInput = field(default_factory=lambda: None)
    length_vector: NodeInput = field(default_factory=lambda: None)
    width_vector: NodeInput = field(default_factory=lambda: None)
    length: NodeInput = field(default_factory=lambda: None)
    width: NodeInput = field(default_factory=lambda: None)
    height: NodeInput = field(default_factory=lambda: None)

    boundingbox: np.ndarray = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.center_point is None:

            self.center_point = self.add_input(node_center_point_input, ui_label = node_center_point_input)

        if self.length_vector is None:

            self.length_vector = self.add_input(node_length_vector_input, ui_label = node_length_vector_input)

        if self.width_vector is None:

            self.width_vector = self.add_input(node_width_vector_input, ui_label = node_width_vector_input)

        if self.length is None:

            self.length = self.add_input(node_length_input, ui_label = node_length_input)

        if self.width is None:

            self.width = self.add_input(node_width_input, ui_label = node_width_input)

        if self.height is None:

            self.height = self.add_input(node_height_input, ui_label = node_height_input)

    def compute(self, sender=None, app_data=None):
        
        center_point_len = len(self.center_point.parameter)
        length_vector_len = len(self.length_vector.parameter)
        width_vector_len = len(self.width_vector.parameter)
        length_len = len(self.length.parameter)
        width_len = len(self.width.parameter)
        height_len = len(self.height.parameter)

        if center_point_len == length_len == width_len == height_len:
        
            if length_vector_len == width_vector_len:

                bounding_boxes = []

                j = 0

                for i in range(0, len(self.center_point.parameter)):

                    center_point = self.center_point.parameter[i]

                    length_vector = self.length_vector.parameter[i]

                    width_vector = self.width_vector.parameter[i]

                    length = self.length.parameter[j]

                    width = self.width.parameter[j]

                    height = self.height.parameter[j]

                    boundingbox = BoundingBox(center_point, length_vector,
                                              width_vector, length, width,
                                              height)
                    
                    bounding_boxes.append(boundingbox)

                    if j == len(self.length.parameter) - 1:
                        j = 0
                    else:
                        j += 1

        self.output.payload = np.array(bounding_boxes)

@dataclass
class BoundingBox:

    center_point: NodeInput = field(default_factory=lambda: np.zeros((1,3), np.float64))
    length_vector: NodeInput = field(default_factory=lambda: np.zeros((1,3), np.float64))
    width_vector: NodeInput = field(default_factory=lambda: np.zeros((1,3), np.float64))
    length: NodeInput = field(default = 0)
    width: NodeInput = field(default = 0)
    height: NodeInput = field(default = 0)