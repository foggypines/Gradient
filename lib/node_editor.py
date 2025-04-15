# Copyright 2021 LuminousLizard
# Licensed under the MIT-License

import dearpygui.dearpygui as dpg
from . node_manager import *
from . nodes import *
from . node_position import LastNodePosition
import tkinter as tk
from tkinter import filedialog
from .node_functions import *

# Destroy window if closed
def callback_close_window(sender):
    
    dpg.delete_item(sender)


# Delete selected items
def callback_delete_item(sender):
    
    for selected_node in dpg.get_selected_nodes("NodeEditor"):
        # Deleting node and attached links
        ## Extract all children of the deleted node
        selected_node_children = dpg.get_item_children(selected_node)[1]
        ## Extract all existing links in the Node Editor
        nodeEditor_links = dpg.get_item_children("NodeEditor")[0]
        ## Iterate through NodeEditor elements and delete attached links
        for link in nodeEditor_links:
            if dpg.get_item_configuration(link)["attr_1"] in selected_node_children or dpg.get_item_configuration(link)["attr_2"] in selected_node_children:
                #dpg.delete_item(link)
                func_link_destroyed("NodeEditor", link)
        
        # Deleting node

        node_destroyed(dpg.get_item_alias(selected_node))
        
        # Deleting node
        dpg.delete_item(selected_node)
    for selected_link in dpg.get_selected_links("NodeEditor"):
        func_link_destroyed("NodeEditor", selected_link)

def save_node_file(sender, app_data):
    '''Save the current state to a file'''

    root = tk.Tk()

    root.withdraw()  # Hide the root window

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    if file_path:

        save_state(file_path)

def load_node_file(sender, app_data):
    '''Load a save state from a file'''

    root = tk.Tk()
    
    root.withdraw()  # Hide the root window
  
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
  
    if file_path:
    
        load_state(file_path)    

class NodeEditor:
    def __init__(self):

        dpg.add_button(label="Save As",
                       callback=save_node_file)
        dpg.add_button(label="Load",
                       callback=load_node_file)

        # dpg.window(tag="NodeEditorWindow")

        with dpg.window(tag="NodeEditorWindow",
                        label="Node editor",
                        width=1000,
                        height=700,
                        pos=[50, 50],
                        menubar=True,
                        no_open_over_existing_popup=False,
                        on_close=callback_close_window):
            
            pass

            #Add a menu bar to the window
            with dpg.menu_bar(label="MenuBar"):
                pass
                with dpg.menu(label="Input/Output"):
                    dpg.add_menu_item(tag="Menu_AddNode_InputFloat",
                                      label="Input float",
                                      callback=node_input_float.add_node_input_float,
                                      user_data="Input_Float")
                    dpg.add_menu_item(tag="Menu_AddNode_Array",
                                      label="Array",
                                      callback=node_array.add_node_input_array,
                                      user_data="Array")
                    dpg.add_menu_item(tag="Menu AddNode_Random_Array",
                                      label="Random Array",
                                      callback=node_array_random.add_node_rand_array)
                    dpg.add_menu_item(tag="Menu AddNode_Readout",
                                      label="Readout",
                                      callback=node_readout.add_node_readout)

                with dpg.menu(label = "Math"):
                    dpg.add_menu_item(tag="Menu_AddNode_Expression",
                                      label="Expression",
                                      callback=node_expression.add_node_expr,
                                      user_data="Expression")
                    dpg.add_menu_item(tag="Menu_AddNode_CrossProduct",
                                      label="Cross Product",
                                      callback=node_binding.add_node_cross_product,
                                      user_data="Cross Product")
                    
                with dpg.menu(label = "Data Manipulation"):
                    dpg.add_menu_item(tag = "Menu_stack_data",
                                      label = "Stack Data",
                                      callback = node_stack_data.add_node_stack_data)
                    dpg.add_menu_item(tag = "Menu_delete_index_data",
                                      label = "Delete Index Data",
                                      callback = node_delete_index.add_node_delete_index_data)
                    dpg.add_menu_item(tag = "Menu_get_index_data",
                                      label = "Get Index",
                                      callback = node_binding.add_node_get_index)

                with dpg.menu(label="Primitive Geometry"):
                    node_point.node_point_instance.add_menu_item()

                    dpg.add_menu_item(tag = "Menu_vector",
                                      label = "Vector",
                                      callback = node_vector.add_node_vector)
                    dpg.add_menu_item(tag = "Menu_AddNode_BoundingBox",
                                      label = "Bounding Box",
                                      callback = node_binding.add_node_bounding_box)
                    dpg.add_menu_item(tag = "Menu_line",
                                      label = "Line",
                                      callback = node_binding.add_node_line)

                with dpg.menu(label = "Evaluate"):
                    dpg.add_menu_item(tag = "Menu_AddNode_CloestPoint",
                                      label = "Closest Point",
                                      callback = node_closest_point.add_node_closest_point,
                                      user_data="Closest Point")

                with dpg.menu(label="Solid Geometry"):
                    node_sphere.node_sphere_instance.add_menu_item()
                    dpg.add_menu_item(tag="Menu_AddNode_Cylinder",
                                        label="Cylinder",
                                        callback=node_cylinder.add_node_cylinder,
                                        user_data="Cylinder")
                    dpg.add_menu_item(tag="Menu_AddNode_Union",
                                      label="Union",
                                      callback=node_union.add_node_union_data,
                                      user_data="Union")
                    dpg.add_menu_item(tag = "Menu_AddNode_Transform",
                                      label = "BReP Transform",
                                      callback = node_transform.add_node_transform,
                                      user_data = "BReP Transform")
                    dpg.add_menu_item(tag = "Menu_AddNode_BReP_Box",
                                      label = "BRep Box",
                                      callback = node_binding.add_node_brep_box)
                    dpg.add_menu_item(tag = "Menu_AddNode_GetBRep",
                                      label = "Get BRep",
                                      callback = node_binding.add_node_get_brep)
                    dpg.add_menu_item(tag = "Menu_AddNode_BRep",
                                      label = "BRep",
                                      callback = node_binding.add_node_brep)
                    
                with dpg.menu(label="Algorithm"):
                    dpg.add_menu_item(tag="Menu_AddNode_Delaunay",
                                      label="Delaunay Triangulation",
                                      callback=node_binding.add_node_delaunay)
                    dpg.add_menu_item(tag="Menu_AddNode_Voronoi",
                                      label="Voronoi",
                                      callback=node_binding.add_node_voronoi)
                    dpg.add_menu_item(tag="Menu_AddNode_PointOnFace",
                                      label="Point on Face",
                                      callback=node_binding.add_node_point_on_face,
                                      user_data="Point on Face")                   

            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text(tag="InfoBar")

            #Add node editor to the window
            with dpg.node_editor(tag="NodeEditor",
                                 
                                 # Function call for updating all nodes if a new link is created
                                 callback=func_chain_update,
                                 # Function call for updating if a link is destroyed
                                 delink_callback=func_link_destroyed):
                pass

            with dpg.handler_registry():
                dpg.add_mouse_click_handler(callback=save_last_node_position)

            with dpg.handler_registry():
                dpg.add_key_release_handler(key=dpg.mvKey_Delete, callback=callback_delete_item)

# Saving the position of the last selected node
def save_last_node_position():
    global LastNodePosition
    if dpg.get_selected_nodes("NodeEditor") == []:
        pass
    else:
        LastNodePosition = dpg.get_item_pos(dpg.get_selected_nodes("NodeEditor")[0])