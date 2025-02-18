import adsk.core, adsk.fusion, adsk.cam, traceback
import json
from ... lib.fusionAddInUtils.general_utils import log
from . fusion_event_handler_base import BaseEventHandler

union_event_id = 'UnionEventId'
union_event = None

# The event handler that responds to the custom event being fired.
class UnionEventHandler(BaseEventHandler):
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

            node_a_input = str(eventArgs['node_a_input'])
            node_b_input = str(eventArgs['node_b_input'])
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

                #Runs when it times to actually add BRep bodies to the active design

                attributes_a = self.design.findAttributes("Node", node_a_input)

                body_a = self.design.findEntityByToken(attributes_a[0].value)[0]

                body_a_temp = temp_brep_mgr.copy(body_a)

                attributes_b = self.design.findAttributes("Node", node_b_input)
                
                for attr in attributes_b:

                    body_b = self.design.findEntityByToken(attr.value)[0]

                    body_b_temp = temp_brep_mgr.copy(body_b)

                    temp_brep_mgr.booleanOperation(body_a_temp, body_b_temp, adsk.fusion.BooleanTypes.UnionBooleanType)
                                                
                self.base_feature.updateBody(body_a, body_a_temp)

                adsk.doEvents()

                self.assign_default_color(body_a)

                token = body_a.entityToken

                self.tokens.append(token)

                body_a.attributes.add("Node", node_id_input, token)

        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

    def union_bodies(self, node_a_input, node_b_input, node_id, delete = False):

        return_data = {'node_a_input': node_a_input, 'node_b_input': node_b_input, 'node_id': node_id, 'delete': delete}

        return_json = json.dumps(return_data)

        self.app.fireCustomEvent(union_event_id, return_json)
