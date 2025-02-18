import adsk.core, adsk.fusion, adsk.cam, traceback
import json
from ... lib.fusionAddInUtils.general_utils import log
from . fusion_event_handler_base import BaseEventHandler

Sphere_event_id = 'SphereEventId'
sphere_event = None

# The event handler that responds to the custom event being fired.
class SphereEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        BaseEventHandler.__init__(self, app, ui, design, base_feature )
        self.tokens = []
        self.spheres = []
        
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

                    sphere_len = 0

                else:

                    sphere_len = len(self.spheres)

                bodies = self.rootcomp.bRepBodies

                while i < max(attr_len,sphere_len):

                    if i < attr_len and i < sphere_len: #update case

                        attr = attributes[i]

                        spheres = self.design.findEntityByToken(attr.value)

                        for sphere in spheres:

                            self.base_feature.updateBody(sphere, self.spheres[i])

                    elif i < attr_len and i >= sphere_len: #delete case

                        attr = attributes[i]

                        spheres = self.design.findEntityByToken(attr.value)

                        attr.deleteMe()

                        for sphere in spheres:

                            sphere.deleteMe()

                    elif i >= attr_len and i < sphere_len: #add case

                        body = bodies.add(self.spheres[i], self.base_feature)

                        self.assign_default_color(body)

                        token = body.entityToken

                        self.tokens.append(token)

                        body.attributes.add("Node", node_id, token)

                    i = i + 1

                adsk.doEvents()

                self.spheres.clear()

            else:

                x = float(eventArgs['x']) * 0.1
                y = float(eventArgs['y']) * 0.1
                z = float(eventArgs['z']) * 0.1
                radius = float(eventArgs['radius']) * 0.1

                #make a temp brep sphere

                point = adsk.core.Point3D.create(x,y,z)

                temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()
                
                sphere = temp_brep_mgr.createSphere(point, radius)

                self.spheres.append(sphere)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def make_sphere(self, x,y,z, radius, node_id, compute = False, delete = False):

        return_data = {'x': x, 'y': y, 'z': z, 'radius': radius,
                        'node_id': node_id, 'compute': compute, 'delete': delete}

        return_json = json.dumps(return_data)

        self.app.fireCustomEvent(Sphere_event_id, return_json)
