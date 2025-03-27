import adsk.core

class EventRegistrar:
    def __init__(self, app, fusion_handler):
        self.app = app
        self.fusion_handler = fusion_handler
        self.handler_dict = {}

        self.event_dict = {}

    def register_event(self, event_id, event_handler_class):
        event = self.app.registerCustomEvent(event_id)
        event_handler = event_handler_class(self.app, self.app.userInterface, self.fusion_handler.design, self.fusion_handler.base_feature)
        event.add(event_handler)
        self.handler_dict[event_id] = event_handler

        self.event_dict[event_id] = event

        return event_handler, event
    
    def clean_up_events(self):
        for event_id in self.event_dict:
            
            self.event_dict[event_id].remove(self.handler_dict[event_id])
            self.app.unregisterCustomEvent(event_id)