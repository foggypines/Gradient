import json
from .fusion_event_handler_base import BaseEventHandler
import adsk.core, adsk.fusion, adsk.cam, traceback
import numpy as np

point_on_face_event_id = 'PointOnFaceEventId'
point_on_face_event = None

class PointOnFaceEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        super().__init__(app, ui, design, base_feature)

        self.faces = None

        self.u_vals = []

        self.v_vals = []

        self.point_array = None

    def notify(self, args):

        try:
            if self.ui.activeCommand != 'SelectCommand':
                self.ui.commandDefinitions.itemById('SelectCommand').execute()

            return_list = []

            for face in self.faces:
                                
                eval = face.evaluator

                parametric_range = eval.parametricRange()

                loop_length = len(self.u_vals)

                for i in range(loop_length):
                
                    u = np.interp(self.u_vals[i], [0, 1], [parametric_range.minPoint.x, parametric_range.maxPoint.x])
                    
                    v = np.interp(self.v_vals[i], [0, 1], [parametric_range.minPoint.y, parametric_range.maxPoint.y])

                    p = adsk.core.Point2D.create(u, v)

                    on_face = eval.isParameterOnFace(p)

                    if on_face == True:

                        return_val, point = eval.getPointAtParameter(p)

                        return_list.append(np.array([point.x * 10, point.y * 10, point.z * 10]))

            self.point_array = np.array(return_list)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

            self.point_array = False

    def point_on_face(self, faces, u_vals, v_vals, node_id):

        return_data = {'node_id': node_id}

        return_json = json.dumps(return_data)

        self.faces = faces

        self.u_vals = u_vals

        self.v_vals = v_vals

        self.app.fireCustomEvent(point_on_face_event_id, return_json)
        
        while self.point_array is None:
            pass
        return self.point_array