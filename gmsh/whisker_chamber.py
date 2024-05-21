import gmsh
import math as m
import os
from whisker_mesh_manager import chamber_mesh

# Element size for creating mechanical model
mesh_size = 4

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

gmsh.model.add("whisker_chamber")
gmsh.logger.start()
def mesh_genarator(no_chamber = 2,
                    chamber_bot_radius = 10,
                    cone_angle = 85.5,
                    chamber_height = 24,
                    mesh_size = mesh_size):
    ### Chambers
    chamber_mesh.chamber(no_chamber = no_chamber,
                        chamber_bot_radius = chamber_bot_radius,
                        cone_angle = cone_angle,
                        chamber_height = chamber_height,
                        mesh_size = mesh_size)
    for i in range(no_chamber):
        gmsh.model.occ.remove([(3, i+2)], recursive=1)

    ### Mesh creation
    # Parameters
    gmsh.model.occ.mesh.setSize(gmsh.model.occ.getEntities(-1), mesh_size)
    gmsh.model.occ.synchronize()

    gmsh.model.mesh.generate(2)

    ### Exporting files
    gmsh.write("test_stl.stl")

    gmsh.fltk.run()
    gmsh.finalize()

if __name__ == '__main__':
    mesh_genarator(no_chamber = 1,
                    chamber_bot_radius = 10,
                    cone_angle = 85.5,
                    chamber_height = 24,
                    mesh_size = 4)
    