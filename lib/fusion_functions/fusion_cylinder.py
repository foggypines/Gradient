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

            compute = bool(eventArgs['compute'])
            node_id = str(eventArgs['node_id'])

            #Runs when it times to actually add BRep bodies to the active design

            if compute:

                attributes = self.design.findAttributes("Node", node_id)

                i = 0

                attr_len = len(attributes)

                cylinder_len = len(self.cylinders)

                bodies = self.rootcomp.bRepBodies

                while i < max(attr_len, cylinder_len):

                    if i < attr_len and i < cylinder_len: #update case

                        attr = attributes[i]

                        cylinders = self.design.findEntityByToken(attr.value)

                        for cylinder in cylinders:

                            self.base_feature.updateBody(cylinder, self.cylinders[i])

                    elif i < attr_len and i >= cylinder_len: #delete case

                        attr = attributes[i]

                        cylinders = self.design.findEntityByToken(attr.value)

                        attr.deleteMe()

                        for cylinder in cylinders:

                            cylinder.deleteMe()

                    elif i >= attr_len and i < cylinder_len: #add case

                        body = bodies.add(self.cylinders[i], self.base_feature)

                        self.assign_default_color(body)

                        token = body.entityToken

                        self.tokens.append(token)

                        body.attributes.add("Node", node_id, token)

                    i = i + 1

                adsk.doEvents()

                self.cylinders.clear()

                #Delete any old cylinders

                # if self.tokens != []:

                #     for t in self.tokens:

                #         old_cylinder = self.design.findEntityByToken(t)

                #         for c in old_cylinder:

                #             for attr in c.attributes:

                #                 if attr.name == node_id:

                #                     c.deleteMe()

                # bodies = self.rootcomp.bRepBodies

                # #add the sphere to the active designs bodies

                # for cylinder in self.cylinders:

                #     body = bodies.add(cylinder, self.base_feature)

                #     self.assign_default_color(body)

                #     token = body.entityToken

                #     self.tokens.append(token)

                #     body.attributes.add("Node", node_id, "")

                # self.cylinders.clear() #clear out the spheres list

            else:

                point_x = float(eventArgs['point_x']) * 0.1
                point_y = float(eventArgs['point_y']) * 0.1
                point_z = float(eventArgs['point_z']) * 0.1

                vector_x = float(eventArgs['vector_x']) * 0.1
                vector_y = float(eventArgs['vector_y']) * 0.1
                vector_z = float(eventArgs['vector_z']) * 0.1

                radius = float(eventArgs['radius']) * 0.1

                #make a temp brep cylinder

                point1 = adsk.core.Point3D.create(point_x, point_y, point_z)

                point2 = adsk.core.Point3D.create(vector_x, vector_y, vector_z)

                temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()
                
                cylinder = temp_brep_mgr.createCylinderOrCone(point1, radius, point2, radius)

                self.cylinders.append(cylinder)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def make_cylinder(self, point, vector, radius, node_id, compute = False):

        return_data = {'point_x': point[0], 'point_y': point[1], 'point_z': point[2],
                       'vector_x': vector[0], 'vector_y': vector[1], 'vector_z': vector[2],
                        'radius': radius, 'node_id': node_id, 'compute': compute}

        return_json = json.dumps(return_data)

        self.app.fireCustomEvent(cylinder_event_id, return_json)