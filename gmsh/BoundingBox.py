import gmsh
import math as m
# import numpy as np
import os

# def Bounding():
gmsh.initialize()

angle = 180
lc_marker =0.2
lc = 10
number_marker = 100
number_column = 10
number_row = 10
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("Taclink")
path = os.path.dirname(os.path.abspath(__file__))
v1 = gmsh.model.occ.importShapes(os.path.join(path,'skin-protac-ver2.STEP'))
gmsh.model.occ.synchronize()
xmin1, ymin1, zmin1, xmax1, ymax1, zmax1 = gmsh.model.getBoundingBox(
    v1[0][0], v1[0][1])
vin1 = gmsh.model.getEntitiesInBoundingBox(xmin1, ymin1, zmin1, xmax1, ymax1, zmax1)
# list = [109, 127, 145, 163, 181, 199, 217, 235, 253, 271, 289]
# a = [str(i) for i in list]
# res = str(" ".join(a))
# print(res)

gmsh.model.occ.synchronize()
gmsh.model.occ.mesh.setSize(vin1, lc)
# gmsh.model.occ.mesh.setSize(lines_inbox, lc_marker)
# gmsh.model.occ.mesh.setSize(points_inbox, lc_marker)
print(gmsh.model.mesh.getNodes(dim=0, tag=-1, includeBoundary=False, returnParametricCoord=True))

# gmsh.model.occ.synchronize()
# gmsh.model.mesh.generate(3)

path = os.path.dirname(os.path.abspath(__file__))
v1 = gmsh.model.occ.importShapes(os.path.join(path,'PDLC_film.STEP'))
gmsh.model.occ.synchronize()
xmin1, ymin1, zmin1, xmax1, ymax1, zmax1 = gmsh.model.getBoundingBox(
    v1[0][0], v1[0][1])
vin1 = gmsh.model.getEntitiesInBoundingBox(xmin1, ymin1, zmin1, xmax1, ymax1, zmax1)
# list = [109, 127, 145, 163, 181, 199, 217, 235, 253, 271, 289]
# a = [str(i) for i in list]
# res = str(" ".join(a))
# print(res)

gmsh.model.occ.synchronize()
gmsh.model.occ.mesh.setSize(vin1, lc)
# gmsh.model.occ.mesh.setSize(lines_inbox, lc_marker)
# gmsh.model.occ.mesh.setSize(points_inbox, lc_marker)
print(gmsh.model.mesh.getNodes(dim=0, tag=-1, includeBoundary=False, returnParametricCoord=True))

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.fltk.run()

gmsh.finalize()
    # return list_base, a