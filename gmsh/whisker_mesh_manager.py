import gmsh
import math as m
import os

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("whisker_body")
gmsh.logger.start()

### Main body
# Geometry parameters
body_bot_radius = 12
body_cone_angle = 85.5*m.pi/180
body_height = 100
body_top_radius = body_bot_radius - (body_height/m.tan(body_cone_angle))

# Body construction
gmsh.model.occ.addPoint(0, 0, 0, 5, 1)
gmsh.model.occ.addPoint(0, body_bot_radius, 0, 5, 2)
gmsh.model.occ.addPoint(0, body_top_radius, body_height, 5, 3)
gmsh.model.occ.addPoint(0, 0, body_height, 5, 4)

gmsh.model.occ.synchronize()

l_1 = gmsh.model.occ.addLine(1, 2, tag=1)
l_2 = gmsh.model.occ.addLine(2, 3, tag=2)
l_3 = gmsh.model.occ.addLine(3, 4, tag=3)
l_4 = gmsh.model.occ.addLine(4, 1, tag=4)
gmsh.model.occ.addCurveLoop([1, 2, 3, 4], 1)
gmsh.model.occ.addPlaneSurface([1], tag=1)

body = gmsh.model.occ.revolve([(2, 1)], 0, 0, 0, 0, 0, 1, m.pi*2,recombine=1)
gmsh.model.occ.remove([(2, 1)], recursive=1)
gmsh.model.occ.synchronize()


### Chambers
# Geometry parameters
chamber_bot_radius = 10
chamber_cone_angle = 85.5*m.pi/180
chamber_height = 24
chamber_top_radius = chamber_bot_radius - (chamber_height/m.tan(chamber_cone_angle))
no_chamber = 2
chamber_dist = 1.5

# if no_chamber < 2:
#     pass
# else:
#     for i in range(no_chamber):
# Chamber construction
gmsh.model.occ.addPoint(chamber_dist, 0, 0, 5, -1)
gmsh.model.occ.addPoint(chamber_dist, chamber_bot_radius, 0, 5, -1)
gmsh.model.occ.addPoint(chamber_dist, chamber_top_radius, chamber_height, 5, -1)
gmsh.model.occ.addPoint(chamber_dist, 0, chamber_height, 5, -1)

gmsh.model.occ.addLine(4, 5, tag=-1)
gmsh.model.occ.addLine(5, 6, tag=-1)
gmsh.model.occ.addLine(6, 7, tag=-1)
gmsh.model.occ.addLine(7, 4, tag=-1)

gmsh.model.occ.synchronize()

a = gmsh.model.occ.addCurveLoop([7, 8, 9, 10], -1)
chamber_plane = gmsh.model.occ.addPlaneSurface([a], tag=-1)
chamber = gmsh.model.occ.revolve([(2, chamber_plane)], 0, 0, 0, 0, 0, 1, m.pi*2)
gmsh.model.occ.remove([(2, chamber_plane)], recursive=1)

gmsh.model.occ.synchronize()
# gmsh.model.occ.copy([(3, 1)])
### Cut body
final_body = gmsh.model.occ.cut([(3,1)], [(3,2)], tag=-1,removeObject=1, removeTool=1)
gmsh.model.occ.synchronize()


### Mesh creation
# Parameters
mesh_size = 4
gmsh.model.occ.mesh.setSize(gmsh.model.getEntities(-1), mesh_size)
gmsh.model.occ.synchronize()

gmsh.model.mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()
