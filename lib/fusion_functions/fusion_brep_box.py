import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import orjson
from . fusion_event_handler_base import BaseEventHandler
from .. node_functions.node_bounding_box_func import BoundingBox

brep_box_event_id = 'BRePBoxEventId'
brep_box_event = None

# The event handler that responds to the custom event being fired.
class BRePBoxEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        BaseEventHandler.__init__(self, app, ui, design, base_feature )
        self.tokens = []
        self.boxes = []
        
    def notify(self, args):
        try:
            # Make sure a command isn't running before changes are made.
            if self.ui.activeCommand != 'SelectCommand':
                self.ui.commandDefinitions.itemById('SelectCommand').execute()     
            
            # Get the value from the JSON data passed through the event.
            eventArgs = orjson.loads(args.additionalInfo)

            compute = bool(eventArgs['compute'])
            delete = bool(eventArgs['delete'])
            node_id = str(eventArgs['node_id'])

            #Runs when it times to actually add BRep bodies to the active design

            if compute:

                attributes = self.design.findAttributes("Node", node_id)

                i = 0

                attr_len = len(attributes)

                if delete:

                    box_brep_len = 0

                else:

                    box_brep_len = len(self.boxes)

                bodies = self.rootcomp.bRepBodies

                while i < max(attr_len, box_brep_len):

                    if i < attr_len and i < box_brep_len: #update case

                        attr = attributes[i]

                        boxes = self.design.findEntityByToken(attr.value)

                        for box in boxes:

                            self.base_feature.updateBody(box, self.boxes[i])

                    elif i < attr_len and i >= box_brep_len: #delete case

                        attr = attributes[i]

                        boxes = self.design.findEntityByToken(attr.value)

                        attr.deleteMe()

                        for box in boxes:

                            box.deleteMe()

                    elif i >= attr_len and i < box_brep_len: #add case

                        body = bodies.add(self.boxes[i], self.base_feature)

                        self.assign_default_color(body)

                        token = body.entityToken

                        self.tokens.append(token)

                        body.attributes.add("Node", node_id, token)

                    i = i + 1

                adsk.doEvents()

                self.boxes.clear()

            else:

                center_x = eventArgs['center_x'] * 0.1
                center_y = eventArgs['center_y'] * 0.1
                center_z = eventArgs['center_z'] * 0.1

                length_vect_x = eventArgs['l_vect_x'] * 0.1
                length_vect_y = eventArgs['l_vect_y'] * 0.1
                length_vect_z = eventArgs['l_vect_z'] * 0.1

                width_vect_x = eventArgs['w_vect_x'] * 0.1
                width_vect_y = eventArgs['w_vect_y'] * 0.1
                width_vect_z = eventArgs['w_vect_z'] * 0.1

                length = float(eventArgs['length']) * 0.1
                width = float(eventArgs['width']) * 0.1
                height = float(eventArgs['height']) * 0.1

                center_point = adsk.core.Point3D.create(center_x, center_y, center_z)

                length_vect = adsk.core.Vector3D.create(length_vect_x, length_vect_y, length_vect_z)

                width_vect = adsk.core.Vector3D.create(width_vect_x, width_vect_y, width_vect_z)

                bounding_box = adsk.core.OrientedBoundingBox3D.create(center_point, length_vect, width_vect, length, width, height)

                temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()
                
                box = temp_brep_mgr.createBox(bounding_box)

                self.boxes.append(box)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def make_box(self, node_id: str, bounding_box: BoundingBox = None, compute: bool = False, delete: bool = False):

        if bounding_box is None:

            return_data = {'compute': compute, 'delete': delete, 'node_id': node_id}

        else:

            return_data = {'center_x': bounding_box.center_point[0], 'center_y': bounding_box.center_point[1], 'center_z': bounding_box.center_point[2],
                           'l_vect_x': bounding_box.length_vector[0], 'l_vect_y': bounding_box.length_vector[1], 'l_vect_z': bounding_box.length_vector[2],
                           'w_vect_x': bounding_box.width_vector[0], 'w_vect_y': bounding_box.width_vector[1], 'w_vect_z': bounding_box.width_vector[2],
                           'length': bounding_box.length, 'width': bounding_box.width, 'height': bounding_box.height, 'compute': compute, 'delete': delete,
                           'node_id': node_id}

        json_bytes = orjson.dumps(return_data, option=orjson.OPT_SERIALIZE_NUMPY)

        json_str = json_bytes.decode()

        self.app.fireCustomEvent(brep_box_event_id, json_str)