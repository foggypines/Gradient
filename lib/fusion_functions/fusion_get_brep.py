import json
import orjson
from .fusion_event_handler_base import BaseEventHandler

import adsk.core, adsk.fusion, adsk.cam, traceback

brep_get_event_id = 'BRePGetEventId'
brep_get_event = None

class BRePGetEventHandler(BaseEventHandler):
    def __init__(self, app, ui, design, base_feature):
        BaseEventHandler.__init__(self, app, ui, design, base_feature)
        self.tokens = []

        self.brep = None

    def notify(self, args):
        try:
            # Make sure a command isn't running before changes are made.
            if self.ui.activeCommand != 'SelectCommand':
                self.ui.commandDefinitions.itemById('SelectCommand').execute()

            # Get the value from the JSON data passed through the event.
            eventArgs = orjson.loads(args.additionalInfo)

            node_id = str(eventArgs['node_id'])

            brepbodies = self.rootcomp.bRepBodies

            brepbody = brepbodies[0]

            temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()

            brep_copy = temp_brep_mgr.copy(brepbody)

            body = brepbodies.add(brep_copy, self.base_feature)

            attr = body.attributes.itemByName("Node", node_id)

            if attr is None:

                body.attributes.add("Node", node_id, brepbody.entityToken)

            self.brep = body

        except:
            
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.autoTerminate(False)

            self.brep = False

    def get_brep(self, node_id: str):

        return_data = {'node_id': node_id}

        json_bytes = orjson.dumps(return_data, option=orjson.OPT_SERIALIZE_NUMPY)
        
        json_str = json_bytes.decode()

        self.app.fireCustomEvent(brep_get_event_id, json_str)

        while self.brep is None:
            pass
        return self.brep