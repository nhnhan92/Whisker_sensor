import Sofa
from stlib3.physics.mixedmaterial import Rigidify
from stlib3.components import addOrientedBoxRoi
from elasticbody import ElasticBody
from splib3.objectmodel import setData
from articulation_system import ServoArm, ServoMotor, ActuatedArm
from splib3.numerics import vec3

pluginList = [
    "ArticulatedSystemPlugin",
    "Sofa.Component.AnimationLoop",
    "Sofa.Component.Constraint.Lagrangian.Correction",
    "Sofa.Component.Constraint.Lagrangian.Solver",
    "Sofa.Component.Constraint.Projective",
    "Sofa.Component.Engine.Select",
    "Sofa.Component.IO.Mesh",
    "Sofa.Component.LinearSolver.Direct",
    "Sofa.Component.Mapping.MappedMatrix",
    "Sofa.Component.Mass",
    "Sofa.Component.SolidMechanics.FEM.Elastic",
    "Sofa.Component.SolidMechanics.Spring",
    "Sofa.Component.StateContainer",
    "Sofa.Component.Topology.Container.Constant",
    "Sofa.Component.Topology.Container.Dynamic",
    "Sofa.Component.Visual",
    "Sofa.GL.Component.Rendering3D",
    "Sofa.GUI.Component",
    "Sofa.Component.Mapping.Linear",
    "Sofa.Component.Mapping.NonLinear",
    "SoftRobots",
    "STLIB",
]


def ROBIN_actuator(name="ROBIN_actuator"):
    
    def __rigidify(self, translation = [0,0,0], eulerRotation = [0,0,0],scale = [40, 0.5, 40]):
        deformableObject = self.ElasticBody.MechanicalModel
        self.ElasticBody.init()
        name = ["Rigidifiedfree_Base", "RigidifiedBase"]
        for i in range(1,2):
            rot_box = addOrientedBoxRoi(
                self,
                position=[list(j) for j in deformableObject.dofs.rest_position.value],
                name="freeBoxROI"+str(i),
                translation=vec3.vadd(translation, [0.0, 50.0*i, 0.0]),
                eulerRotation=eulerRotation,
                scale=scale,
                drawBoxes=1,
            )

            rot_box.init()
            groupIndices = []
            groupIndices.append([ind for ind in rot_box.indices.value])
            rigidifiedpart = Rigidify(
                self,
                deformableObject,
                groupIndices=groupIndices,
                frames=[[0, 0, 0]],
                name=name[i],
            )
        # groupIndices phai la list chu ko duoc la array

    def __attachToSkin(self):
        rigidParts = self.RigidifiedBase.RigidParts
        arti_system.ServoMotor.Articulation.ServoWheel.addChild(rigidParts)
        # rigidParts_free = self.Rigidifiedfree_Base.RigidParts
        # arti_system.ServoMotor.Articulation.ServoWheel.addChild(rigidParts_free)
        rigidParts.addObject(
            "SubsetMultiMapping",
            input=arti_system.ServoMotor.Articulation.ServoWheel.getLinkPath(),
            output="@./",
            indexPairs=[0, 1],
        )
        # rigidParts_free.addObject(
        #     "SubsetMultiMapping",
        #     input=arti_system.ServoMotor.Articulation.ServoWheel.getLinkPath(),
        #     output="@./",
        #     indexPairs=[0, 1],
        # ) 
          ## idx[0]: node của output model, do đó sẽ lần lượt 0, 1, ..., n
        ### idx[1]: node ucar input model, cái này thì tùy vào node nào muốn được map tương ứng với idx[0]

    # def __constraintfreeend(self):
    #     freeend
    self = Sofa.Core.Node(name)
    
    self.addChild(ElasticBody(translation=[0.0, 0, 0.0], rotation=[0, 0, 0], color="yellow"))
    arti_system = ActuatedArm(
        name="Articulation_system", translation=[0.0, 70.0, 0.0], rotation=[180.0, 0.0, 0.0],
    )
    self.addChild(arti_system)
    __rigidify(self)
    __attachToSkin(self)
    return self


def createScene(rootNode):
    """ """
    from stlib3.scene import MainHeader, Scene
    from stlib3.physics.deformable import ElasticMaterialObject
    import math
    from splib3.animation import animate
    from addconstraint import PartialBox, FixingBox

    scene = Scene(
        rootNode, gravity=[0.0, -9810.0, 0.0], dt=0.01, iterative=False, plugins=pluginList
    )

    scene.addMainHeader()
    scene.addObject("DefaultVisualManagerLoop")
    scene.addObject("FreeMotionAnimationLoop")
    scene.addObject(
        "GenericConstraintSolver", maxIterations=5000, tolerance=1e-10, computeConstraintForces=0
    )
    scene.Simulation.addObject("GenericConstraintCorrection")
    scene.Settings.mouseButton.stiffness = 10
    scene.Simulation.TimeIntegrationSchema.rayleighStiffness = 0.05
    scene.VisualStyle.displayFlags = "showBehavior"
    # scene.Settings.mouseButton.stiffness = 1000

    robin_actuator = scene.Modelling.addChild(ROBIN_actuator())
    # setData(robin_actuator.RigidifiedBase.RigidParts.dofs, showObject=True, showObjectScale=5, drawMode=2)
    # setData(robin_actuator.RigidifiedBase.RigidParts.RigidifiedParticules.dofs, showObject=1, showObjectScale=1,
    # drawMode=1, showColor=[1., 1., 0., 1.])
    # setData(robin_actuator.RigidifiedBase.DeformableParts.dofs, showObject=1, showObjectScale=0.1, drawMode=2)
    FixingBox(
        scene.Modelling,
        robin_actuator.ElasticBody.MechanicalModel,
        scale=[40, 0.2, 40],
        translation=[0.0, 0, 0.0],
    )
    scene.Modelling.FixingBox.BoxROI.drawBoxes = True
    scene.Simulation.addChild(scene.Modelling.ROBIN_actuator)
    scene.Simulation.addChild(scene.Modelling.FixingBox)

    def animation(target, factor):
        target.angleIn.value = factor * 0.85*math.pi

    animate(animation, {"target": robin_actuator.Articulation_system}, duration=2, mode="pingpong")

    scene.Modelling.ROBIN_actuator.Articulation_system.ServoMotor.Articulation.ServoWheel.dofs.showObject = (
        True
    )

    # Temporary additions to have the system correctly built in SOFA
    # Will no longer be required in SOFA v22.06
    scene.Simulation.addObject(
        "MechanicalMatrixMapper",
        template="Vec3,Rigid3",
        name="RigidAndDeformableCoupling",
        object1=robin_actuator.RigidifiedBase.DeformableParts.dofs.getLinkPath(),
        object2=robin_actuator.RigidifiedBase.RigidParts.dofs.getLinkPath(),
        skipJ2tKJ2=True,
        nodeToParse=robin_actuator.RigidifiedBase.DeformableParts.MechanicalModel.getLinkPath(),
    )

    # scene.Simulation.addObject(
    #     "MechanicalMatrixMapper",
    #     template="Vec3,Rigid3",
    #     name="RigidAndDeformableCoupling2",
    #     object1=robin_actuator.Rigidifiedfree_Base.DeformableParts.dofs.getLinkPath(),
    #     object2=robin_actuator.Rigidifiedfree_Base.RigidParts.dofs.getLinkPath(),
    #     skipJ2tKJ2=True,
    #     nodeToParse=robin_actuator.Rigidifiedfree_Base.DeformableParts.MechanicalModel.getLinkPath(),
    # )
