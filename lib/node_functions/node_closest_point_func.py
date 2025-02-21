import numpy as np
from scipy.spatial import KDTree
import dearpygui.dearpygui as dpg
from . node_base_func import BaseNodeFunction
from .node_input import NodeInput, all_node_inputs
from ... lib.utility import append_value
from ... lib.fusionAddInUtils.general_utils import log
from dataclasses import dataclass, field

node_name = "ClosestPoint"
node_output_closest = "_OutputClosest"
node_output_distance = "_OutputDist"
point_name = "_Point"
point_set_name = "_Point_set"

@dataclass
class ClosestPointNodeFunction(BaseNodeFunction):

    point: NodeInput = field(default = None)
    point_set: NodeInput = field(default = None)
    closest_point: np.float64 = field(default_factory = lambda: np.zeros((1,3), np.float64))
    distance: np.float64 = field(default_factory = lambda: np.zeros((1,1), np.float64))

    def __post_init__(self):

        if self.point is None:

            self.point = self.add_input(point_name)

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name)

    def compute(self, sender=None, app_data=None):

        i = 0

        point_len = len(self.point.parameter)

        self.closest_point = np.zeros((point_len, 3), np.float64)

        self.distance = np.zeros((point_len,1), np.float64)

        for point in self.point.parameter:

            tree = KDTree(self.point_set.parameter)

            distance, index = tree.query(point)

            self.closest_point[i] = self.point_set.parameter[index]

            self.distance[i] = distance

            i = i + 1

        if i == 1:

            self.distance = self.distance[0]

        for link in self.links:

            node_input = all_node_inputs[link.end]

            if node_output_closest in link.start:

                node_input.update(self.closest_point)

            if node_output_distance in link.start:

                node_input.update(self.distance)

        if sender is not None:
        
            self.update()