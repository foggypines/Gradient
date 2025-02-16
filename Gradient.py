#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading

from .lib.fusion_functions.fusion_handler import FusionHandler
from .lib.fusion_functions.fusion_sphere import Sphere_event_id, sphere_event, SphereEventHandler
from .lib.fusion_functions.fusion_cylinder import cylinder_event_id, cylinder_event, CylinderEventHandler
from .lib.fusion_functions.fusion_union import union_event_id, union_event, UnionEventHandler
from .lib.fusion_functions.fusion_difference import difference_event_id, difference_event, DifferenceEventHandler


import dearpygui.dearpygui as dpg
from .lib.node_editor import NodeEditor
from .lib.node_functions import node_sphere_func
from .lib.node_functions import node_cylinder_func
from .lib.node_functions import node_union_func
from .lib.node_functions import node_difference_func

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None

# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event, on_sphere_event, on_cylinder_event, on_union_event, on_difference_event):
        threading.Thread.__init__(self)
        self.stopped = event

        self.on_sphere_event = on_sphere_event
        self.on_cylinder_event = on_cylinder_event
        self.on_union_event = on_union_event
        self.on_difference_event = on_difference_event

    def run(self):

        dpg.create_context()
        dpg.create_viewport(title="Gradient",width=1500,height=768)

        def callback_close_program(sender, data):
            exit(0)

        def callback_show_debugger(sender, data):
            dpg.show_debug()

        with dpg.viewport_menu_bar():
            dpg.add_menu_item(label="Debugger", callback=callback_show_debugger)
            dpg.add_menu_item(label="Close", callback=callback_close_program)
            #dpg.bind_font(default_font)

            node_sphere_func.make_sphere = self.on_sphere_event.make_sphere
            node_cylinder_func.make_cylinder = self.on_cylinder_event.make_cylinder
            node_union_func.union_bodies = self.on_union_event.union_bodies
            node_difference_func.difference_bodies = self.on_difference_event.difference_bodies

            nodeEditor = NodeEditor()

        # Setup API connections
        # node_point_func.point_instance.setup(make_point)

        # Main GUI Loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
        
def run(context):
    global ui
    global app
    try:

        app = adsk.core.Application.get()

        ui  = app.userInterface
        
        #Start the Fusion Handler

        fusion_handler = FusionHandler(app, ui)

        # Register the sphere custom event and connect the handler.
        global sphere_event
        sphere_event = app.registerCustomEvent(Sphere_event_id)
        on_sphere_event = SphereEventHandler(app, ui, fusion_handler.design, fusion_handler.base_feature)
        sphere_event.add(on_sphere_event)
        handlers.append(on_sphere_event)

        # Register the cylinder custom event and connect the handler.
        global cylinder_event
        cylinder_event = app.registerCustomEvent(cylinder_event_id)
        on_cylinder_event = CylinderEventHandler(app, ui, fusion_handler.design, fusion_handler.base_feature)
        cylinder_event.add(on_cylinder_event)
        handlers.append(on_cylinder_event)

        # Register the on Union custom event and connect the handler

        global union_event
        union_event = app.registerCustomEvent(union_event_id)
        on_union_event = UnionEventHandler(app, ui, fusion_handler.design, fusion_handler.base_feature)
        union_event.add(on_union_event)
        handlers.append(on_union_event)

        # Register the on Difference custom event and connect the handler

        global difference_event
        difference_event = app.registerCustomEvent(difference_event_id)
        on_difference_event = DifferenceEventHandler(app, ui, fusion_handler.design, fusion_handler.base_feature)
        difference_event.add(on_difference_event)
        handlers.append(on_difference_event)

        # Create a new thread for the other processing.        
        global stopFlag        
        stopFlag = threading.Event()
        myThread = MyThread(event = stopFlag,
                            on_sphere_event = on_sphere_event,
                            on_cylinder_event = on_cylinder_event,
                            on_union_event = on_union_event,
                            on_difference_event = on_difference_event)
        myThread.start()

        ui.messageBox("thread started")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        if handlers.count:
            sphere_event.remove(handlers[0])
        stopFlag.set() 
        app.unregisterCustomEvent(Sphere_event_id)
        # ui.messageBox('Stop addin')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))