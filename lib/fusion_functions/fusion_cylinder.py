import adsk.core, adsk.fusion, adsk.cam, traceback
import json
from ... lib.fusionAddInUtils.general_utils import log
from . fusion_event_handler_base import BaseEventHandler

cylinder_event_id = 'CylinderEventId'
cylinder_event = None

# The event handler that responds to the custom event being fired.
class CylinderEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        # super().__init__()
        BaseEventHandler.__init__(self, app, ui, design, base_feature )
        self.tokens = []
        self.cylinders = []
        
    def notify(self, args):
        try:
            # Make sure a command isn't running before changes are made.
            if self.ui.activeCommand != 'SelectCommand':
                self.ui.commandDefinitions.itemById('SelectCommand').execute()     
            
            # Get the value from the JSON data passed through the event.
            eventArgs = json.loads(args.additionalInfo)

            delete = bool(eventArgs['delete'])
            node_id = str(eventArgs['node_id'])

            #Runs when it times to actually add BRep bodies to the active design

            if delete:

                attributes = self.design.findAttributes("Node", node_id)

                for attr in attributes:

                    cylinders = self.design.findEntityByToken(attr.value)

                    attr.deleteMe()

                    for cylinder in cylinders:

                        cylinder.deleteMe()
            
            else:

                temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()

                self.rootcomp.bRepBodies

                bodies = self.rootcomp.bRepBodies

                attributes = self.design.findAttributes("Node", node_id)

                i = 0

                attr_len = len(attributes)

                cylinder_len = len(self.cylinders)

                while i < max(attr_len, cylinder_len):

                    if i < attr_len and i < cylinder_len: #update case

                        attr = attributes[i]

                        old_cylinders = self.design.findEntityByToken(attr.value)

                        for old_cylinder in old_cylinders:

                            cylinder = self.construct_cylinder(self.cylinders[i], temp_brep_mgr)

                            self.base_feature.updateBody(old_cylinder, cylinder)

                    elif i < attr_len and i >= cylinder_len: #delete case

                        attr = attributes[i]

                        cylinders = self.design.findEntityByToken(attr.value)

                        attr.deleteMe()

                        for cylinder in cylinders:

                            cylinder.deleteMe()

                    elif i >= attr_len and i < cylinder_len: #add case

                        cylinder = self.cylinders[i]

                        cylinder_body = self.construct_cylinder(cylinder, temp_brep_mgr)                        

                        body = bodies.add(cylinder_body, self.base_feature)

                        self.assign_default_color(body)

                        token = body.entityToken

                        self.tokens.append(token)

                        body.attributes.add("Node", node_id, token)

                    i = i + 1

                adsk.doEvents()

                self.cylinders.clear()

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def construct_cylinder(self, cylinder, temp_brep_mgr):

        point_x = float(cylinder.point[0]) * 0.1
        point_y = float(cylinder.point[1]) * 0.1
        point_z = float(cylinder.point[2]) * 0.1

        vector_x = float(cylinder.vector[0]) * 0.1
        vector_y = float(cylinder.vector[1]) * 0.1
        vector_z = float(cylinder.vector[2]) * 0.1

        radius = float(cylinder.radius) * 0.1

        # make a temp brep cylinder

        point1 = adsk.core.Point3D.create(point_x, point_y, point_z)

        point2 = adsk.core.Point3D.create(vector_x, vector_y, vector_z)
        
        cylinder = temp_brep_mgr.createCylinderOrCone(point1, radius, point2, radius)

        return cylinder
        

    def make_cylinder(self, node_id, point = None, vector = None, radius = None, compute = False, delete = False):

        if compute == False:

            self.cylinders.append(Cylinder(point, vector, radius))

        else:

            return_data = {'node_id': node_id, 'delete': delete}

            return_json = json.dumps(return_data)

            self.app.fireCustomEvent(cylinder_event_id, return_json)

class Cylinder:
    def __init__(self, point, vector, radius):
        self.point = point
        self.vector = vector
        self.radius = radius