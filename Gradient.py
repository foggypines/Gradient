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
from .lib.fusion_functions.fusion_brep_box import brep_box_event_id, brep_box_event, BRePBoxEventHandler
from .lib.fusion_functions.fusion_get_brep import brep_get_event_id, brep_get_event, BRePGetEventHandler
from .lib.fusionAddInUtils.general_utils import log

import dearpygui.dearpygui as dpg
from .lib.node_editor import NodeEditor
from .lib.nodes.node_themes import apply_gradient_themes
from .lib.node_functions import node_sphere_func
from .lib.node_functions import node_cylinder_func
from .lib.node_functions import node_union_func
from .lib.node_functions import node_transform_func
from .lib.node_functions import node_brep_box_func
from .lib.node_functions import node_get_BReP_func as node_brep_func
from .lib.fusion_functions.event_registrar import EventRegistrar

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None

# The class for the new thread.
class GradientThread(threading.Thread):
    def __init__(self, event, on_sphere_event, on_cylinder_event,
                on_union_event, on_transform_event, on_brep_box_event, on_brep_get_event):
        threading.Thread.__init__(self)
        self.stopped = event

        self.on_sphere_event = on_sphere_event
        self.on_cylinder_event = on_cylinder_event
        self.on_union_event = on_union_event
        self.on_transform_event = on_transform_event
        self.on_brep_box_event = on_brep_box_event
        self.on_brep_get_event = on_brep_get_event


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

            # dpg.bind_font(font1)

            nodeEditor = NodeEditor()

        apply_gradient_themes()

        # Setup API connections
        # node_point_func.point_instance.setup(make_point)

        node_sphere_func.make_sphere = self.on_sphere_event.make_sphere
        node_cylinder_func.make_cylinder = self.on_cylinder_event.make_cylinder
        node_union_func.union_bodies = self.on_union_event.union_bodies
        node_transform_func.transform_bodies = self.on_transform_event.transform_bodies
        node_brep_box_func.make_box = self.on_brep_box_event.make_box
        node_brep_func.get_brep = self.on_brep_get_event.get_brep

        # Main GUI Loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
        
def run(context):
    global ui
    global app
    global event_registrar
    try:

        app = adsk.core.Application.get()

        ui  = app.userInterface
        
        #Start the Fusion Handler

        fusion_handler = FusionHandler(app, ui)

        event_registrar = EventRegistrar(app, fusion_handler)

        on_sphere_event, sphere_event = event_registrar.register_event(Sphere_event_id, SphereEventHandler)
        on_cylinder_event, cylinder_event = event_registrar.register_event(cylinder_event_id, CylinderEventHandler)
        on_union_event, union_event = event_registrar.register_event(union_event_id, UnionEventHandler)
        on_transform_event, transform_event = event_registrar.register_event(transform_event_id, TransformEventHandler)
        on_brep_get_event, brep_get_event = event_registrar.register_event(brep_get_event_id, BRePGetEventHandler)
        on_brep_box_event, brep_box_event = event_registrar.register_event(brep_box_event_id, BRePBoxEventHandler)

        # Create a new thread for the node processing.        
        global stopFlag        
        stopFlag = threading.Event()
        gradient_Thread = GradientThread(stopFlag, on_sphere_event, on_cylinder_event,
                            on_union_event, on_transform_event=on_transform_event,
                            on_brep_box_event=on_brep_box_event,
                            on_brep_get_event=on_brep_get_event)
        
        gradient_Thread.start()

        log("Gradient Started")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        event_registrar.clean_up_events()

        log("Gradient Stopped")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))