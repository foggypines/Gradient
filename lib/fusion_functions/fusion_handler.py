import adsk.core, adsk.fusion, adsk.cam, traceback

base_feature_attr_name = "gradient_base_feature"

base_feature_attr_group = "gradient"

class FusionHandler:
    def __init__(self, app, ui):
        self.app = app
        self.ui = ui
        self.design = None
        self.base_feature = None

        # Set the parameter value.
        self.design = adsk.fusion.Design.cast(self.app.activeProduct)
        rootcomp = self.design.rootComponent

        #create the context to add to the design

        base_features = rootcomp.features.baseFeatures

        attributes = self.design.findAttributes(groupName=base_feature_attr_group, 
                                                attributeName=base_feature_attr_name)
                                                
        if len(attributes) == 0:

            self.base_feature = base_features.add()

            self.base_feature.attributes.add(groupName=base_feature_attr_group,
                                             name=base_feature_attr_name,
                                             value=str())
            
        else:

            self.base_feature = attributes[0].parent

        self.base_feature.startEdit()