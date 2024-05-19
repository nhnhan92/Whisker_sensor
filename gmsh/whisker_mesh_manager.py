import gmsh
import math as m
import os

def chamber(no_chamber = int):
    if no_chamber >= 3:
        rot_axis = [0, 0, 0, 0, 0, 1]
        init_p = []
        for i in range(no_chamber):
            init_p.append([[m.cos(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)-chamber_dist*m.sin(chamber_rel_angle*i),
                       m.sin(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)+chamber_dist*m.cos(chamber_rel_angle*i),
                       0],
                       [m.cos(chamber_rel_angle*i)*chamber_bot_radius-m.sin(chamber_rel_angle*i)*chamber_dist,
                        m.sin(chamber_rel_angle*i)*chamber_bot_radius+m.cos(chamber_rel_angle*i)*chamber_dist,
                        0],
                        [m.cos(chamber_rel_angle*i)*chamber_top_radius-m.sin(chamber_rel_angle*i)*chamber_dist,
                        m.sin(chamber_rel_angle*i)*chamber_top_radius+m.cos(chamber_rel_angle*i)*chamber_dist,
                        chamber_height],
                        [m.cos(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)-chamber_dist*m.sin(chamber_rel_angle*i),
                       m.sin(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)+chamber_dist*m.cos(chamber_rel_angle*i),
                       chamber_height]])

    elif no_chamber == 2:
        init_p = [
                    [[0, chamber_dist, 0],
                    [m.sqrt(chamber_bot_radius**2 - chamber_dist**2), chamber_dist, 0],
                    [m.sqrt(chamber_top_radius**2 - chamber_dist**2), chamber_dist,chamber_height],
                    [0, chamber_dist, chamber_height]],
                    [[0, -chamber_dist, 0],
                    [-m.sqrt(chamber_bot_radius**2 - chamber_dist**2), -chamber_dist, 0],
                    [-m.sqrt(chamber_top_radius**2 - chamber_dist**2), -chamber_dist,chamber_height],
                    [0, -chamber_dist, chamber_height]]
                ]

    else:
        init_p = [[[0,0,0],[chamber_bot_radius, 0,0],[chamber_top_radius, 0,0],[0, 0,chamber_height]]]
    
    for i in range(no_chamber):
        p1 = gmsh.model.occ.addPoint(init_p[i][0][0], init_p[i][0][1], init_p[i][0][2], 5, -1)
        p2 = gmsh.model.occ.addPoint(init_p[i][1][0], init_p[i][1][1], init_p[i][1][2], 5, -1)
        p3 = gmsh.model.occ.addPoint(init_p[i][2][0], init_p[i][2][1], init_p[i][2][2], 5, -1)
        p4 = gmsh.model.occ.addPoint(init_p[i][3][0], init_p[i][3][1], init_p[i][3][2], 5, -1)

        l1 = gmsh.model.occ.addLine(p1, p2, tag=-1)
        l2 = gmsh.model.occ.addLine(p2, p3, tag=-1)
        l3 = gmsh.model.occ.addLine(p3, p4, tag=-1)
        l4 = gmsh.model.occ.addLine(p4, p1, tag=-1)
        gmsh.model.occ.synchronize()

        curve = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4], -1)
        chamber_plane = gmsh.model.occ.addPlaneSurface([curve], tag=-1)
        chamber = gmsh.model.occ.revolve([(2, chamber_plane)], 0, 1.5, 0, 0, 0, 1, chamber_rel_angle)
        gmsh.model.occ.remove([(2, chamber_plane)], recursive=1)
        
        gmsh.model.occ.synchronize()
        ### Cut body
        # final_body = gmsh.model.occ.cut([(3,1)], [(3,-1)], tag=-1,removeObject=1, removeTool=1)
        gmsh.model.occ.synchronize()
        print(chamber)
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
chamber_rel_angle = 360*m.pi/(no_chamber*180)
init_p = [0,0]
# if no_chamber == 1:
    
# elif no_chamber == 2:
#     init_p = [0,chamber_dist]
#     rot_axis = [0, chamber_dist, 0, 0, chamber_dist, 1]
# else:
#     init_p = [chamber_dist*m.tan(30),chamber_dist]
#     rot_axis = [0, 0, 0, 0, 0, 1]

# for i in range (no_chamber):

chamber(no_chamber)

### Mesh creation
# Parameters
# mesh_size = 4
# gmsh.model.occ.mesh.setSize(gmsh.model.getEntities(-1), mesh_size)
# gmsh.model.occ.synchronize()

# gmsh.model.mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()
