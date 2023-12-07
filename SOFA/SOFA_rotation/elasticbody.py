# -*- coding: utf-8 -*-
"""
Step 3: Move the content of the ElasticBody in a separated file for reusability
"""
import Sofa


def ElasticBody(name="ElasticBody", rotation=[0, 0, 0], translation=[0, 0, 0], color="yellow"):
    # To simulate an elastic object, we need:
    # - a deformation law (here linear elasticity)
    # - a solving method (here FEM)
    # - as we are using FEM we need a space discretization (here tetrahedron)

    self = Sofa.Core.Node(name)
    mechanicalmodel = self.addChild("MechanicalModel")
    mechanicalmodel.addObject(
        "MeshVTKLoader",
        name="loader",
        rotation=rotation,
        translation=translation,
        createSubelements=0,
        filename="mesh/test_vtk.vtk",
    )
    mechanicalmodel.addObject("TetrahedronSetTopologyContainer", src="@loader", name="container")
    mechanicalmodel.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    mechanicalmodel.addObject("TetrahedronSetGeometryAlgorithms", name="GeomAlgo", template="Vec3d")

    mechanicalmodel.addObject(
        "MechanicalObject",
        name="dofs",
        template="Vec3d",
        position=mechanicalmodel.loader.position.getLinkPath(),
        showObject=False,
        showObjectScale=5.0,
    )
    mechanicalmodel.addObject("UniformMass", name="mass", totalMass=0.00002)

    # ForceField components
    mechanicalmodel.addObject(
        "TetrahedronFEMForceField",
        template="Vec3",
        name="FEM",
        method="large",
        poissonRatio=0.45,
        youngModulus=50,
    )

    # mechanicalmodel.addObject(
    #     "BoxROI",
    #     template="Vec3d",
    #     box="-40 -0.1 -40 40 0.1 40",
    #     drawBoxes="0",
    #     name="Partial_FixedROI",
    #     drawSize="0.5",
    # )
    # mechanicalmodel.addObject(
    #     "PartialFixedConstraint",
    #     name="partialFixedConstraint",
    #     indices="@Partial_FixedROI.indices",
    #     fixedDirections="1 0 1",
    # )
    # mechanicalmodel.addObject(
    #     "BoxROI",
    #     template="Vec3d",
    #     box="-40 49.8 -40 40 50.2 40",
    #     drawBoxes="1",
    #     name="freeROI",
    #     drawSize="0.5",
    # )
    # mechanicalmodel.addObject("RestShapeSpringsForceField", points="@freeROI.indices", stiffness=1e12, drawSpring="true")
    # Visual model
    # visualmodel = Sofa.Core.Node("VisualModel")
    # self.addChild(visualmodel)
    # # # Specific loader for the visual model
    # # # visualmodel.addObject('MeshSTLLoader',
    # # #                       name='loader',
    # # #                       filename='data/mesh/tripod_mid.stl',
    # # #                       rotation=rotation,
    # # #                       translation=translation)
    # # visualmodel.addObject('OglModel',
    # #                       src=mechanicalmodel.loader.position.getLinkPath(),
    # #                       name='renderer',
    # #                       color=color)
    visualmodel = mechanicalmodel.addChild("VisualModel")
    visualmodel.addObject("OglModel", name="renderer", template="Vec3d", color=color)
    visualmodel.addObject(
        "IdentityMapping",
        template="Vec3d,Vec3d",
        name="visualMapping",
        input=mechanicalmodel.dofs.getLinkPath(),
        output=visualmodel.renderer.getLinkPath(),
    )

    # visualmodel.addObject('BarycentricMapping',
    #                       input=mechanicalmodel.dofs.getLinkPath(),
    #                       output=visualmodel.renderer.getLinkPath())

    return self


def createScene(rootNode):
    from stlib3.scene import Scene

    scene = Scene(rootNode, gravity=[0.0, -9810, 0.0], iterative=False)
    scene.addMainHeader()
    scene.addObject("DefaultAnimationLoop")
    scene.addObject("DefaultVisualManagerLoop")
    scene.Simulation.addChild(ElasticBody())
