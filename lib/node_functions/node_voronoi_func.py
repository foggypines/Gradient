import array
import numpy as np
from numpy.linalg import multi_dot
from scipy.spatial import Voronoi
from .node_input import NodeInput
from .node_output import NodeOutput
from .node_base_func import BaseNodeFunction
from dataclasses import dataclass, field
from itertools import combinations
import adsk.core, adsk.fusion


node_name = "Voronoi"
point_set_name = "_Point_set"
boundary_name = "_Boundary"

tolerance=1e-6

@dataclass
class VoronoiNodeFunction(BaseNodeFunction):

    point_set: NodeInput = field(default = None)

    boundary: NodeInput = field(default = None)

    def __post_init__(self):

        super().__post_init__()

        if self.point_set is None:

            self.point_set = self.add_input(point_set_name, required=True, ui_label="Point Set")

        if self.boundary is None:

            self.boundary = self.add_input(boundary_name, required=True, ui_label="Boundary")

    def compute(self, sender=None, app_data=None):

        ori = np.zeros(3)

        #Get resources for generating faces

        app = adsk.core.Application.get()

        self.design = adsk.fusion.Design.cast(app.activeProduct)
        
        temp_brep_mgr = adsk.fusion.TemporaryBRepManager.get()

        rootcomp = self.design.rootComponent

        base_feature_attr_name = "gradient_base_feature"

        base_feature_attr_group = "gradient"

        attributes = self.design.findAttributes(groupName=base_feature_attr_group, 
                                        attributeName=base_feature_attr_name)
        
        stitch_features = rootcomp.features.stitchFeatures

        base_feature = attributes[0].parent

        bodies = rootcomp.bRepBodies

        complex_boundary = self.boundary.parameter[0]

        bounding_box = complex_boundary.boundingBox

        box_min_fusion = bounding_box.minPoint

        box_max_fusion = bounding_box.maxPoint

        box_min = np.array([box_min_fusion.x * 10, box_min_fusion.y * 10, box_min_fusion.z * 10], dtype=np.float64)

        box_max = np.array([box_max_fusion.x * 10, box_max_fusion.y * 10, box_max_fusion.z * 10], dtype=np.float64)    

        #Initial Voronoi calculation

        points = self.point_set.parameter

        # points = np.array([[0, 0, 0], [0, 1, 0], [0, 2, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0],
        #     [2, 0, 0], [2, 1, 0], [2, 2, 0],
        #     [0, 0, 1], [0, 1, 1], [0, 2, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1],
        #     [2, 0, 1], [2, 1, 1], [2, 2, 1],
        #     [0, 0, 2], [0, 1, 2], [0, 2, 2], [1, 0, 2], [1, 1, 2], [1, 2, 2],
        #     [2, 0, 2], [2, 1, 2], [2, 2, 2]], dtype=np.float64)
        
        points = mirror_points(points, box_max_fusion, box_min_fusion)

        self.output.payload = points

        vor = Voronoi(points)

        vertices = vor.vertices

        regions = vor.regions

        point_regions = vor.point_region

        ridge_vertices = vor.ridge_vertices

        ridge_points = vor.ridge_points

        voronoi_cells = []

        # Map voronoi vertices to faces

        for j in range(len(point_regions)):

            point_region = point_regions[j]

            region = regions[point_region]

            cell = VoronoiCell(region)

            for i in range(len(ridge_vertices)):
                
                ridge = ridge_vertices[i]

                if all(v in region for v in ridge):

                    cell.ridges.append(ridge)

                    cell.ridge_indices.append(i)

                    cell.ridge_input_point_indices.append(ridge_points[i])

            cell_infinity = any(v == -1 for v in cell.vertex_indices)

            if cell_infinity == False:

                for k in range(len(cell.ridges)):

                    ridge = cell.ridges[k]

                    inner_face = make_finite_face(ridge, vertices)

                    cell.faces.append(inner_face)

                in_box = False

                for face in cell.faces:

                    for edge in face.edges:

                        start = edge[0]
                        
                        end = edge[1]

                        if point_in_xyz_rectangle(start, box_min, box_max, tol=tolerance) or point_in_xyz_rectangle(end, box_min, box_max, tol=tolerance):

                            in_box = True

                            break   
                if in_box:

                    # Add the cell to the list of voronoi cells
                    voronoi_cells.append(cell)

        #create finite cells

        for cell in voronoi_cells:

            #create the brep

            cell_brep_def = adsk.fusion.BRepBodyDefinition.create()

            cell_points = []

            for vertex_index in cell.vertex_indices:

                if vertex_index != -1:

                    cell_points.append(vertices[vertex_index])

            cell_points = np.array(cell_points)

            cell_center = cell_points.mean(axis=0) # find the center of the cell

            for inner_face in cell.faces:

                edge_defs = []

                face_vec1 = None

                face_vec2 = None

                face_normal = None

                face_point = None

                for edge in inner_face.edges:

                    #get the edge vertices and convert to fusion points

                    start = edge[0]

                    end = edge[1]

                    start_point = adsk.core.Point3D.create(start[0]*0.1, start[1]*0.1, start[2]*0.1)

                    end_point = adsk.core.Point3D.create(end[0]*0.1, end[1]*0.1, end[2]*0.1)

                    #construct the face normal and point

                    if face_vec1 is None:

                        face_vec1 = start - end
                        
                    elif face_vec2 is None:

                        face_vec2 = start - end

                    elif face_normal is None:

                        face_normal = np.cross(face_vec1, face_vec2) * 2

                        if not np.any(face_normal):

                            face_normal = None

                        else:

                            face_point = adsk.core.Point3D.create(start[0]*0.1, start[1]*0.1, start[2]*0.1)

                            face_offset1 = start + face_normal

                            face_offset2 = start - face_normal

                            offset_dist1 = np.linalg.norm(face_offset1 - cell_center)

                            offset_dist2 = np.linalg.norm(face_offset2 - cell_center)

                            if offset_dist2 > offset_dist1:

                                face_normal = -face_normal

                            face_normal = adsk.core.Vector3D.create(face_normal[0], face_normal[1], face_normal[2])

                    #create the edge definition

                    edge_defs.append(create_edge_def(cell_brep_def, start_point, end_point))

                face_plane = adsk.core.Plane.create(face_point, face_normal)

                create_face_for_body_def(cell_brep_def, face_plane, edge_defs)

            cell_brep = cell_brep_def.createBody()

            body = bodies.add(cell_brep, base_feature)

            body_coll = adsk.core.ObjectCollection.create()

            body_coll.add(body)

            val_input = adsk.core.ValueInput.createByString("0.25 mm")

            stitch_input = stitch_features.createInput(body_coll, val_input, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

            stitch_input.targetBaseFeature = base_feature

            stitch_features.add(stitch_input)

            base_bodies = base_feature.bodies

            b_count = base_bodies.count

            cell_body = base_bodies.item(b_count - 1)

            cell_body_copy = temp_brep_mgr.copy(cell_body)

            tool = temp_brep_mgr.copy(complex_boundary)

            try:

                temp_brep_mgr.booleanOperation(cell_body_copy, tool, adsk.fusion.BooleanTypes.IntersectionBooleanType)

            except Exception as e:

                tool.deleteMe()

            base_feature.updateBody(cell_body, cell_body_copy)

        adsk.doEvents()

class VoronoiCell:
    def __init__(self, vertex_indices):
        self.vertex_indices = vertex_indices
        self.ridges = []
        self.ridge_indices = []
        self.faces = []
        self.ridge_input_point_indices = []

class VoronoiFace:
    def __init__(self):
        self.edges = []

def make_finite_face(ridge, vertices):

    face = VoronoiFace()
    
    edge_len = len(ridge)

    j = 0

    while j < edge_len:

        if j == edge_len - 1:

            t = 0

        else:

            t = j + 1

        v1_index = ridge[j]

        v2_index = ridge[t]

        v1 = vertices[v1_index]

        v2 = vertices[v2_index]

        pair = [v1, v2]

        face.edges.append(pair)

        j += 1

    return face

def mirror_points(points, max_point, min_point):

    mirrored_points_x_max = np.copy(points)

    mirrored_points_x_min = np.copy(points)


    mirror_points_y_min = np.copy(points)

    mirror_points_y_max = np.copy(points)


    mirror_points_z_min = np.copy(points)

    mirror_points_z_max = np.copy(points)

    x_min = min_point.x * 10

    x_max = max_point.x * 10

    y_min = min_point.y * 10

    y_max = max_point.y * 10

    z_min = min_point.z * 10

    z_max = max_point.z * 10


    mirrored_points_x_min[:, 0] = x_min - (mirrored_points_x_min[:, 0] - x_min)  # Mirror across x-axis

    mirrored_points_x_max[:, 0] = x_max + (x_max - mirrored_points_x_max[:, 0])  # Mirror across x-axis

    mirror_points_y_min[:, 1] = y_min - (mirror_points_y_min[:, 1] - y_min)  # Mirror across y-axis

    mirror_points_y_max[:, 1] = y_max + (y_max - mirror_points_y_max[:, 1])  # Mirror across y-axis

    mirror_points_z_min[:, 2] = z_min - (mirror_points_z_min[:, 2] - z_min)  # Mirror across z-axis

    mirror_points_z_max[:, 2] = z_max + (z_max - mirror_points_z_max[:, 2])  # Mirror across z-axis


    
    points = np.append(points, mirrored_points_x_min, axis=0)
    
    points = np.append(points, mirrored_points_x_max, axis=0)
    
    points = np.append(points, mirror_points_y_min, axis=0)
    
    points = np.append(points, mirror_points_y_max, axis=0)
    
    points = np.append(points, mirror_points_z_min, axis=0)
    
    points = np.append(points, mirror_points_z_max, axis=0)

    return points

def point_in_xyz_rectangle(point, min_point, max_point, tol=1e-6):
    """
    Checks if a 3D point is inside or on the boundary of an axis-aligned rectangle (box)
    defined by min_point and max_point (adsk.core.Point3D).
    """
    x, y, z = point
    return (min_point[0] - tol <= x <= max_point[0] + tol and
            min_point[1] - tol <= y <= max_point[1] + tol and
            min_point[2] - tol <= z <= max_point[2] + tol)

def create_edge_def(brep_def, start_point, end_point):

    # Create edge definition

    edgeDef = adsk.fusion.BRepEdgeDefinition.cast(None)

    # Create vertex definition

    start_vertex_def = brep_def.createVertexDefinition(start_point)

    end_vertex_def = brep_def.createVertexDefinition(end_point)  

    curve = adsk.core.Line3D.create(start_point, end_point)

    # Create edge definition by curve

    edgeDef = brep_def.createEdgeDefinitionByCurve(start_vertex_def, end_vertex_def, curve)
    
    return edgeDef   

def create_face_for_body_def(brep_def, surface, edge_defs):

    # Create face definition

    faceDef = adsk.fusion.BRepFaceDefinition.cast(None)
    
    # Create lump definition

    lumpDefs = brep_def.lumpDefinitions

    lumpDef = lumpDefs.add()

    # Create shell definition

    shellDefs = lumpDef.shellDefinitions

    shellDef = shellDefs.add()

    # Create face definition

    faceDefs = shellDef.faceDefinitions

    faceDef = faceDefs.add(surface, True)

    # Create loop definition

    loopDefs = faceDef.loopDefinitions

    loopdef = loopDefs.add()
    
    # Create coEdge definitions

    brepCoEdgeDefs = loopdef.bRepCoEdgeDefinitions   

    for edgeDef in edge_defs:

        brepCoEdgeDefs.add(edgeDef, True)

    return faceDef 