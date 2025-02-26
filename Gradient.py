#Author-Dylan Rice
#Description-Node based geometry editor.

#Add modules to system path to allow for direct imports.

import os
import sys

dirname = os.path.dirname(__file__)

mod_name = os.path.join(dirname, 'modules')

sys.path.append(mod_name)

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading

from .lib.fusion_functions.fusion_handler import FusionHandler
from .lib.fusion_functions.fusion_sphere import Sphere_event_id, sphere_event, SphereEventHandler
from .lib.fusion_functions.fusion_cylinder import cylinder_event_id, cylinder_event, CylinderEventHandler
from .lib.fusion_functions.fusion_union import union_event_id, union_event, UnionEventHandler
from .lib.fusion_functions.fusion_transform import transform_event_id, transform_event, TransformEventHandler
from .lib.fusionAddInUtils.general_utils import log

import dearpygui.dearpygui as dpg
from .lib.node_editor import NodeEditor
from .lib.node_functions import node_sphere_func
from .lib.node_functions import node_cylinder_func
from .lib.node_functions import node_union_func
from .lib.node_functions import node_transform_func

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None

# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event, on_sphere_event, on_cylinder_event, on_union_event, on_transform_event):
        threading.Thread.__init__(self)
        self.stopped = event

        self.on_sphere_event = on_sphere_event
        self.on_cylinder_event = on_cylinder_event
        self.on_union_event = on_union_event
        self.on_transform_event = on_transform_event

    def run(self):

        dpg.create_context()
        dpg.create_viewport(title="Gradient",width=1500,height=768)

        def callback_close_program(sender, data):
            exit(0)

        def callback_show_debugger(sender, data):
            dpg.show_debug()

        # with dpg.font_registry():

        #     font1 = dpg.add_font('C:/Users/Dylan Rice/AppData/Roaming/Autodesk/Autodesk Fusion 360/API/AddIns/Gradient/assets/fonts/Nasalization Rg.otf', 13)

        with dpg.viewport_menu_bar():
            dpg.add_menu_item(label="Debugger", callback=callback_show_debugger)
            dpg.add_menu_item(label="Close", callback=callback_close_program)

            # dpg.bind_font(font1)

            nodeEditor = NodeEditor()

        # Setup API connections
        # node_point_func.point_instance.setup(make_point)

        node_sphere_func.make_sphere = self.on_sphere_event.make_sphere
        node_cylinder_func.make_cylinder = self.on_cylinder_event.make_cylinder
        node_union_func.union_bodies = self.on_union_event.union_bodies
        node_transform_func.transform_bodies = self.on_transform_event.transform_bodies

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

        # Register the transform bodies custom event and connect the handler

        global transform_event
        transform_event = app.registerCustomEvent(transform_event_id)
        on_transform_event = TransformEventHandler(app, ui, fusion_handler.design, fusion_handler.base_feature)
        transform_event.add(on_transform_event)
        handlers.append(on_transform_event)

        # Create a new thread for the node processing.        
        global stopFlag        
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag, on_sphere_event, on_cylinder_event, on_union_event, on_transform_event=on_transform_event)
        myThread.start()

        log("Gradient Started")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        if handlers.count:
            sphere_event.remove(handlers[0])
        stopFlag.set() 
        app.unregisterCustomEvent(Sphere_event_id)
        log("Gradient Stopped")
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))