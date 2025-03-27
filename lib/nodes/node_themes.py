import dearpygui.dearpygui as dpg

error_theme = None

def apply_gradient_themes():
    
    with dpg.theme() as error_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (200, 0, 0), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (200, 0, 0), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (200, 0, 0), category=dpg.mvThemeCat_Nodes)