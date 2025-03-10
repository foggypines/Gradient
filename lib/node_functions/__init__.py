# # Copyright 2021 LuminousLizard
# # Licensed under the MIT-License

# __all__ = ["node_sphere_func", "node_base_func", "node_point_func", "node_input",
#               "node_input_float_func","node_array_func", "node_array_random_func", "node_cylinder_func",
#               "node_expression_func", "node_closest_point_func", "node_readout_func",
#                "node_stack_data_func", "node_delete_index_func", "node_union_func", "node_output", "node_three_dim_func",
#                "node_vector_func", "node_transform_func", "node_bounding_box_func", "node_cross_product_func"]

import os

__all__ = []
nodes_folder = os.path.dirname(__file__)

for filename in os.listdir(nodes_folder):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        __all__.append(module_name)
