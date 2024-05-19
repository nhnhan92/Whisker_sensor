import gmsh
import math as m
import os


def chamber(no_chamber = int):
    if no_chamber == 2:
        # rot_axis = [[0, chamber_dist, 0, 0, 0, 1],[0, -chamber_dist, 0, 0, 0, 1]]
        # arc_p = [
        #             [[0, chamber_dist, 0],
        #             [m.sqrt(chamber_bot_radius**2 - chamber_dist**2), chamber_dist, 0],
        #             [m.sqrt(chamber_top_radius**2 - chamber_dist**2), chamber_dist,chamber_height],
        #             [0, chamber_dist, chamber_height]],
        #             [[0, -chamber_dist, 0],
        #             [-m.sqrt(chamber_bot_radius**2 - chamber_dist**2), -chamber_dist, 0],
        #             [-m.sqrt(chamber_top_radius**2 - chamber_dist**2), -chamber_dist,chamber_height],
        #             [0, -chamber_dist, chamber_height]]
        #         ]
        rot_axis = [0, 0, 0, 0, 0, 1]
        init_p = [[0,0,0],[chamber_bot_radius, 0,0],[chamber_top_radius, 0,chamber_height],[0, 0,chamber_height]]
        p1 = gmsh.model.occ.addPoint(init_p[0][0], init_p[0][1], init_p[0][2], mesh_size, -1)
        p2 = gmsh.model.occ.addPoint(init_p[1][0], init_p[1][1], init_p[1][2], mesh_size, -1)
        p3 = gmsh.model.occ.addPoint(init_p[2][0], init_p[2][1], init_p[2][2], mesh_size, -1)
        p4 = gmsh.model.occ.addPoint(init_p[3][0], init_p[3][1], init_p[3][2], mesh_size, -1)

        l1 = gmsh.model.occ.addLine(p1, p2, tag=-1)
        l2 = gmsh.model.occ.addLine(p2, p3, tag=-1)
        l3 = gmsh.model.occ.addLine(p3, p4, tag=-1)
        l4 = gmsh.model.occ.addLine(p4, p1, tag=-1)
        gmsh.model.occ.synchronize()

        curve = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4], -1)
        chamber_plane = gmsh.model.occ.addPlaneSurface([curve], tag=-1)
        chamber = gmsh.model.occ.revolve([(2, chamber_plane)], rot_axis[0], rot_axis[1], 
                                        rot_axis[2], rot_axis[3], rot_axis[4], rot_axis[5], 2*m.pi)
        
        p1 = gmsh.model.occ.addPoint(chamber_bot_radius, chamber_dist, 0, mesh_size, -1)
        p2 = gmsh.model.occ.addPoint(-chamber_bot_radius, -chamber_dist, 0, mesh_size, -1)
        p3 = gmsh.model.occ.addPoint(chamber_bot_radius, -chamber_dist, 0, mesh_size, -1)
        p4 = gmsh.model.occ.addPoint(-chamber_bot_radius, chamber_dist, 0, mesh_size, -1)
        
        l1 = gmsh.model.occ.addLine(p1, p4, tag=-1)
        l2 = gmsh.model.occ.addLine(p4, p2, tag=-1)
        l3 = gmsh.model.occ.addLine(p2, p3, tag=-1)
        l4 = gmsh.model.occ.addLine(p3, p1, tag=-1)
        curve = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4], -1)
        cut_plane = gmsh.model.occ.addPlaneSurface([curve], tag=-1)
        gmsh.model.occ.synchronize()
        cut_body = gmsh.model.occ.extrude([(2,cut_plane)],0,0,chamber_height,recombine=0)
        chamber = gmsh.model.occ.cut([(3,2)], [(3,3)], tag=-1,removeObject=1, removeTool=1)
        final_body = gmsh.model.occ.cut([(3,1)], [(3,2),(3,3)], tag=-1,removeObject=1, removeTool=1)
        gmsh.model.occ.remove([(2, chamber_plane)], recursive=1)
    else:
        if no_chamber >= 3:
            rot_axis = []
            init_p = []
            for i in range(no_chamber):
                rot_axis.append([m.cos(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)-chamber_dist*m.sin(chamber_rel_angle*i),
                        m.sin(chamber_rel_angle*i)*chamber_dist/m.tan(chamber_rel_angle/2)+chamber_dist*m.cos(chamber_rel_angle*i),
                        0, 0, 0, 1])
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

        else:
            rot_axis = [[0, 0, 0, 0, 0, 1]]
            init_p = [[[0,0,0],[chamber_bot_radius, 0,0],[chamber_top_radius, 0,chamber_height],[0, 0,chamber_height]]]
        
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
            chamber = gmsh.model.occ.revolve([(2, chamber_plane)], rot_axis[i][0], rot_axis[i][1], 
                                            rot_axis[i][2], rot_axis[i][3], rot_axis[i][4], rot_axis[i][5], chamber_rel_angle)
            gmsh.model.occ.remove([(2, chamber_plane)], recursive=1)
            
            gmsh.model.occ.synchronize()
            ### Cut body
            final_body = gmsh.model.occ.cut([(3,1)], [(3,2)], tag=-1,removeObject=1, removeTool=1)
            gmsh.model.occ.synchronize()
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
print(body)

### Chambers
# Geometry parameters
mesh_size = 4
chamber_bot_radius = 10
chamber_cone_angle = 85.5*m.pi/180
chamber_height = 24
chamber_top_radius = chamber_bot_radius - (chamber_height/m.tan(chamber_cone_angle))
no_chamber = 3
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

print(gmsh.model.getEntities(-1))
gmsh.model.occ.mesh.setSize(gmsh.model.occ.getEntities(-1), mesh_size)
gmsh.model.occ.synchronize()

gmsh.model.mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()
