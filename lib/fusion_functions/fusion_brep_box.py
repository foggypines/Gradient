import adsk.core, adsk.fusion, adsk.cam, traceback
import json
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
            eventArgs = json.loads(args.additionalInfo)

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

                center_point_grad = eventArgs['center_point'] * 0.1
                length_vect_grad = eventArgs['length_vect'] * 0.1
                width_vect_grad = eventArgs['width_vect'] * 0.1

                length = float(eventArgs['length']) * 0.1
                width = float(eventArgs['width']) * 0.1
                height = float(eventArgs['height']) * 0.1

                center_point = adsk.core.Point3D.create(center_point_grad[0],center_point_grad[1],center_point_grad[2])

                length_vect = adsk.core.Vector3D.create(length_vect_grad[0],length_vect_grad[1],length_vect_grad[2])

                width_vect = adsk.core.Vector3D.create(width_vect_grad[0],width_vect_grad[1],width_vect_grad[2])

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

            return_data = {'center_point': None, 'length_vect': None, 'width_vect': None,
                        'length': None, 'width': None, 'height': None, 'compute': None,
                        'delete': delete, 'node_id': node_id}

        else:

            return_data = {'center_point': bounding_box.center_point, 'length_vect': bounding_box.length_vector,
                        'width_vect': bounding_box.width_vector, 'length': bounding_box.length,
                        'width': bounding_box.width, 'height': bounding_box.height, 'compute': compute,
                        'delete': delete, 'node_id': node_id}

        return_json = json.dumps(return_data)

        self.app.fireCustomEvent(brep_box_event_id, return_json)