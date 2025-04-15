import numpy as np
from .node_base_func import BaseNodeFunction
from .node_output import NodeOutput
from .node_input import NodeInput
from dataclasses import dataclass, field

start_point_input = "_start_point"
end_point_input = "_end_point"
line_input = "_line"

node_output_start_point = "_OutputStartPoint"
node_output_end_point = "_OutputEndPoint"

@dataclass(kw_only=True)
class LineNodeFunction(BaseNodeFunction):

    start_point: NodeInput = field(default=None)

    end_point: NodeInput = field(default=None)

    lines: NodeInput = field(default=None)

    start_point_output: NodeOutput = field(default=None)

    end_point_output: NodeOutput = field(default=None)

    def __post_init__(self):
        super().__post_init__()

        if self.start_point is None:

            self.start_point = self.add_input(start_point_input, ui_label='Start Point', required=True, input_set='points')

        if self.end_point is None:

            self.end_point = self.add_input(end_point_input, ui_label='End Point', required=True, input_set='points')

        if self.lines is None:

            self.lines = self.add_input(line_input, ui_label='Line', required=True, input_set='lines')

        if self.start_point_output is None:
                
            self.start_point_output = self.add_output(node_output_start_point, ui_label='Start Point')

        if self.end_point_output is None:
                    
            self.end_point_output = self.add_output(node_output_end_point, ui_label='End Point')

        self.outputs.append(self.start_point_output)
        self.outputs.append(self.end_point_output)
                
    def compute(self, sender=None, app_data=None):

        if self.start_point.linked == True and self.end_point.linked == True and self.lines.linked == True:

            raise ValueError("Start and end points cannot be linked if line input is linked.")
        
        else:

            if self.start_point.linked == True and self.end_point.linked == True:

                self.point_compute()

            else:

                self.line_compute()

    def line_compute(self):
        '''Computes start and end points for the line case input.'''

        num_lines = len(self.lines.parameter)

        start_points = np.zeros((num_lines, 3), np.float64)
        end_points = np.zeros((num_lines, 3), np.float64)

        i = 0

        for line in self.lines.parameter:

            if line.shape != (2, 3):
                raise ValueError("Line must be a pair of 3D points.")

            start_points[i] = line[0]

            end_points[i] = line[1]
            
            i += 1

        self.output.payload = self.lines.parameter
        self.start_point_output.payload = start_points
        self.end_point_output.payload = end_points


    def point_compute(self):

        start_point_len = len(self.start_point.parameter)

        end_point_len = len(self.end_point.parameter)

        if start_point_len == end_point_len:

            num_points = start_point_len

            lines = np.zeros((num_points, 2, 3), np.float64)

            for i in range(num_points):

                start = np.array(self.start_point.parameter[i], dtype=np.float64)
                end = np.array(self.end_point.parameter[i], dtype=np.float64)

                if start.shape != (3,) or end.shape != (3,):
                    raise ValueError("Start and End points must be 3D coordinates.")
                
                lines[i, 0] = start
                lines[i, 1] = end

                i += 1

            self.output.payload = lines
            self.start_point_output.payload = self.start_point.parameter
            self.end_point_output.payload = self.end_point.parameter
                
        else:

            raise ValueError("Start and End points must have the same length.")