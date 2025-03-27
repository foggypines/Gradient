import adsk.core, adsk.fusion, adsk.cam, traceback

class BaseEventHandler(adsk.core.CustomEventHandler):
    def __init__(self, app, ui, design, base_feature):
        super().__init__()
        self.app = app
        self.ui = ui
        self.design = design
        self.rootcomp = design.rootComponent
        self.base_feature = base_feature

    def assign_default_color(self, body):

        # Load a local material library. You'll need to edit the path to the libary.
        materialLibs = self.app.materialLibraries
        matlib = materialLibs.load('C:/Temp//APISampleMaterialLibrary2.adsklib')

        appearance = matlib.appearances.item(4)

        body.appearance = appearance

        new_appearance = self.design.appearances.itemByName('my_white_color')

        if new_appearance is None:

            new_appearance = self.design.appearances.addByCopy(appearance, 'my_white_color')

            color_property = adsk.core.ColorProperty.cast(new_appearance.appearanceProperties.itemByName('Color'))

            color_property.value = adsk.core.Color.create(255,255,255,255)

            roughness_prop = adsk.core.FloatProperty.cast(new_appearance.appearanceProperties.itemByName('Roughness'))

            roughness_prop.value = 1.0#.60

        body.appearance = new_appearance