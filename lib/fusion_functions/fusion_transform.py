import adsk.core, adsk.fusion, adsk.cam, traceback
import json
from ... lib.fusionAddInUtils.general_utils import log
from . fusion_event_handler_base import BaseEventHandler

transform_event_id = 'TransformEventId'
transform_event = None

# The event handler that responds to the custom event being fired.
class TransformEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        BaseEventHandler.__init__(self, app, ui, design, base_feature )
        self.tokens = []
                
    def notify(self, args):
        try:
            # Make sure a command isn't running before changes are made.
            if self.ui.activeCommand != 'SelectCommand':
                self.ui.commandDefinitions.itemById('SelectCommand').execute()     
            
            # Get the value from the JSON data passed through the event.
            eventArgs = json.loads(args.additionalInfo)

            brep_input = str(eventArgs['brep_input'])
            node_id_input = str(eventArgs['node_id'])
            delete = bool(eventArgs['delete'])

            if delete:

                attrs = self.design.findAttributres("Node", node_id_input)

                for attr in attrs:

                    body = self.design.findEntityByToken(attr.value)

                    attr.deleteMe()

                    if body is not None:

                        body.deleteMe()

                adsk.doEvents()

            else:

                temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()

                attributes_a = self.design.findAttributes("Node", brep_input)

                attr = attributes_a[0]

                body = attr.parent

                temp_body = temp_brep_mgr.copy(body)
                
                matrix = adsk.core.Matrix3D.create()

                vector = adsk.core.Vector3D.create()

                vector.x = 3.14

                vector.y = 2.12

                vector.z = 4.2

                matrix.translation = vector

                temp_brep_mgr.transform(temp_body, matrix)
                                                
                self.base_feature.updateBody(body, temp_body)

                adsk.doEvents()

                self.assign_default_color(body)

                token = body.entityToken

                self.tokens.append(token)

                body.attributes.add("Node", node_id_input, token)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def transform_bodies(self, brep_input, node_id, delete = False):

        return_data = {'brep_input': brep_input, 'node_id': node_id, 'delete': delete}

        return_json = json.dumps(return_data)

        self.app.fireCustomEvent(transform_event_id, return_json)
