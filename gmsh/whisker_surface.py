import gmsh
import math as m
import os

# from BoundingBox import Bounding
gmsh.initialize()

# Element size for creating mechanical model
lc = 2
lc_marker = 3
lc_pole = 3
# # Element size for creating visual model
# lc = 5


# def skin_sotaro_real():
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("Taclink")
path = os.path.dirname(os.path.abspath(__file__))
v1 = gmsh.model.occ.importShapes(os.path.join(path, 'whisker_step/whisker_surface_80.STEP'))
# v1 = gmsh.model.occ.importShapes(os.path.join(path, 'pole.STEP'))

gmsh.model.occ.synchronize()
xmin1, ymin1, zmin1, xmax1, ymax1, zmax1 = gmsh.model.getBoundingBox(
    v1[0][0], v1[0][1])

box_markers_points = gmsh.model.getEntitiesInBoundingBox(xmin1 - 5, ymin1 - 5, -255, xmax1 + 5,
                                                         ymax1 + 5, -5, 0)

# 
gmsh.model.occ.mesh.setSize(gmsh.model.getEntities(0), lc)
# gmsh.model.occ.mesh.setSize(gmsh.model.getEntities(0), lc_pole)

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)


# outer_surfaces = [2,3]
# outer_lines = [5,6,7,8,9,10]
# idx_outer_surfaces = []
# idx_outer_lines = []

# for i in range(len(outer_surfaces)):
#     idx_outer_surfaces.extend((gmsh.model.mesh.getNodes(dim=2, tag=outer_surfaces[i], includeBoundary=0,
#                                                         returnParametricCoord=False))[0])

# for i in range(len(outer_lines)):
#     idx_outer_surfaces.extend((gmsh.model.mesh.getNodes(dim=1, tag=outer_lines[i], includeBoundary=0,
#                                                         returnParametricCoord=False))[0])

# skin_surfaces = [15, 128, 129, 242, 257, 258]
# marker_surfaces= list(range(1,259))
# for i in skin_surfaces:
#     marker_surfaces.remove(i)

# idx_skin_surfaces = []
# idx_marker_surfaces = []
# for i in skin_surfaces:
#     idx_skin_surfaces.extend((gmsh.model.mesh.getNodes(dim=2, tag=i, includeBoundary=1,
#                                                         returnParametricCoord=False))[0])

# for i in marker_surfaces:
#     idx_marker_surfaces.extend((gmsh.model.mesh.getNodes(dim=2, tag=i, includeBoundary=1,
#                                                         returnParametricCoord=False))[0])

# idx_skin_surfaces = [*set(idx_skin_surfaces)]
# idx_marker_surfaces = [*set(idx_marker_surfaces)]


# for i in range(len(idx_skin_surfaces)):
#     idx_skin_surfaces[i] = int(idx_skin_surfaces[i] - 1)
# print(len(idx_skin_surfaces))
# print(idx_skin_surfaces)
# for i in range(len(idx_marker_surfaces)):
#     idx_marker_surfaces[i] = int(idx_marker_surfaces[i] - 1)
# idx_marker_surfaces.sort()
# print(len(idx_marker_surfaces))
# print(idx_marker_surfaces)


# for i in range(len(idx_outer_surfaces)):
#     idx_outer_surfaces[i] = int(idx_outer_surfaces[i] - 1)
#
# print(gmsh.model.mesh.getElementsByType(2, tag=-1, task=0, numTasks=1))
# print(gmsh.model.mesh.getNodes(dim=-1, tag=-1, includeBoundary=False, returnParametricCoord=0))
# print(gmsh.model.mesh.getElementsByType(2, tag=-1, task=0, numTasks=1)[1])
# print(len(gmsh.model.mesh.getElementsByType(2, tag=-1, task=0, numTasks=1)[0]))
# print(len(gmsh.model.mesh.getElementsByType(2, tag=-1, task=0, numTasks=1)[1]))
# print(len((gmsh.model.mesh.getElements(0,-1))[2]))
# gmsh.option.setNumber("Geometry.SurfaceLabels", 1)

gmsh.fltk.run()
gmsh.finalize()
#     return idx_insurface_skin, pos_insurface_skin
