import Sofa
import os
import Sofa.Core
import Sofa.Simulation
import csv
import math as m
import math
import sys
import shutil
from Sofa.constants import *
from SofaRuntime import Timer
# from stlib3.physics.rigid import Floor
from param import *
 
USE_GUI = 1
contact_distance = 3
contact_alarm = 6
fiber1 = []
fiber2 = []
for i in range(1,3):
    with open('fiber'+str(i)+'_info.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if i == 1:
                fiber1.append(row)
            else:
                fiber2.append(row)

fiber1_dof = []
fiber2_dof = []
fiber1_spring_info = []
fiber2_spring_info = []
for i in range(1,len(fiber1)):
    for j in range(1,4):
        fiber1_dof.append(float(fiber1[i][j])) 
        fiber2_dof.append(float(fiber2[i][j])) 
Ks = 1e5    # spring stiffness
Kd = 5      # Spring damping cofficience
for i in range(1,len(fiber1)-2):
    fiber1_spring_info.append([i, i+1, Ks, Kd, m.sqrt((fiber1_dof[3*i]-fiber1_dof[3*(i+1)])**2+
                                                     (fiber1_dof[3*i+1]-fiber1_dof[3*(i+1)+1])**2+
                                                     (fiber1_dof[3*i+2]-fiber1_dof[3*(i+1)+2])**2)])
    fiber2_spring_info.append([i, i+1, Ks, Kd, m.sqrt((fiber2_dof[3*i]-fiber2_dof[3*(i+1)])**2+
                                                     (fiber2_dof[3*i+1]-fiber2_dof[3*(i+1)+1])**2+
                                                     (fiber2_dof[3*i+2]-fiber2_dof[3*(i+1)+2])**2)])
fiber_dof = [fiber1_dof, fiber2_dof]
spring_info = [fiber1_spring_info, fiber2_spring_info]

class controller(Sofa.Core.Controller):

    # For Rigin3d
    def moveRestPos(self, rest_pos, dx, dy, dz):
        str_out = []
        for i in range(0, len(rest_pos)):
            str_out += [
                [
                    rest_pos[i][0] + dx,
                    rest_pos[i][1] + dy,
                    rest_pos[i][2] + dz,
                ]
            ]
        self.mecawhisker.findData("position").value = str_out
        return str_out

    def rotateRestPos(self, rest_pos, rx, centerPosX, centerPosY):
        str_out = []
        for i in range(0, len(rest_pos)):
            newRestPosX = (
                (rest_pos[i][0] - centerPosX) * math.cos(rx)
                - (rest_pos[i][1] - centerPosY) * math.sin(rx)
                + centerPosX
            )
            newRestPosY = (
                (rest_pos[i][0] - centerPosX) * math.sin(rx)
                + (rest_pos[i][1] - centerPosY) * math.cos(rx)
                + centerPosY
            )
            str_out = str_out + " " + str(newRestPosX)
            str_out = str_out + " " + str(newRestPosY)
            str_out = str_out + " " + str(rest_pos[i][2])
        return str_out

    def indention(self, x, y):
        new_pos = self.moveRestPos(
            self.MecaObjectsurface.rest_position.value,
            x,
            y,
            0.0,
        )
        self.MecaObjectsurface.findData("rest_position").value = new_pos
        return new_pos

    def movenext(self, x, y, z):
        str_out = []
        eulerz = math.atan2(y, x)
        cz = math.cos(eulerz * 0.5)
        sz = math.sin(eulerz * 0.5)
        cy = math.cos(90 * 0.5 * math.pi / 180.0)
        sy = math.sin(90 * 0.5 * math.pi / 180.0)
        cx = math.cos(0 * 0.5 * math.pi / 180.0)
        sx = math.sin(0 * 0.5 * math.pi / 180.0)
        qx = sx * cy * cz - cx * sy * sz
        qy = cx * sy * cz + sx * cy * sz
        qz = cx * cy * sz - sx * sy * cz
        w = cx * cy * cz + sx * sy * sz

        str_out += [
            [
                x + (self.dist_contact + self.pre_gap - 0.45) * math.cos(eulerz),
                y + (self.dist_contact + self.pre_gap - 0.45) * math.sin(eulerz),
                z,
                qx,
                qy,
                qz,
                w,
            ]
        ]
        self.MecaObjectsurface.findData("position").value = str_out
        self.MecaObjectsurface.findData("rest_position").value = str_out
        self.rotAngle = eulerz
        return eulerz, self.rotAngle

    def move_trash_roi(self, current_trash, x, y, z):
        output = []
        output += [
            [current_trash[0][0] + x,current_trash[0][1] + y, current_trash[0][2] + z,
             current_trash[0][3] + x,current_trash[0][4] + y, current_trash[0][5] + z]
        ]
        self.trash_roi.findData("box").value = output
        # self.current_trash_roi = self.trash_roi.findData("box").value

    def convert_euler2quaternion(self, eulerx, eulery, eulerz):
        str_out = []
        cz = math.cos(eulerz * 0.5 * math.pi / 180.0)
        sz = math.sin(eulerz * 0.5 * math.pi / 180.0)
        cy = math.cos(eulery * 0.5 * math.pi / 180.0)
        sy = math.sin(eulery * 0.5 * math.pi / 180.0)
        cx = math.cos(eulerx * 0.5 * math.pi / 180.0)
        sx = math.sin(eulerx * 0.5 * math.pi / 180.0)
        qx = sx * cy * cz - cx * sy * sz
        qy = cx * sy * cz + sx * cy * sz
        qz = cx * cy * sz - sx * sy * cz
        w = cx * cy * cz + sx * sy * sz
        str_out += [qx, qy, qz, w]
        return str_out
    

    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node = kw["node"]
        self.dt = self.node.findData("dt").value
        self.current_time = 0
        # Measurement setting

        self.whisker = self.node.getChild("whisker")
        self.mecawhisker = self.whisker.getObject("DOFs")
        self.trash_roi = self.whisker.getObject("trash")
        # self.current_trash_roi = self.trash_roi.findData("box").value

        self.chamber = self.whisker.getChild('cavity')
        self.pressure = self.chamber.getObject('SurfacePressureConstraint')


    def onKeypressedEvent(self,e):

        increment = 0.2
        # if e["key"] == Sofa.constants.Key.plus:
        #     self.move_trash_roi(self.current_trash_roi,0,0,-increment)
        
        if e["key"] == Sofa.constants.Key.leftarrow:
            self.moveRestPos(self.mecawhisker.findData("position").value, 0, 0, -increment)
        
        if e["key"] == Sofa.constants.Key.rightarrow:
            self.moveRestPos(self.mecawhisker.findData("position").value, 0, 0, increment)

        if e["key"] == Sofa.constants.Key.uparrow:
            self.moveRestPos(self.mecawhisker.findData("position").value, increment, 0, 0)
        
        if e["key"] == Sofa.constants.Key.downarrow:
            self.moveRestPos(self.mecawhisker.findData("position").value, -increment, 0, 0)

        if e["key"] == Sofa.constants.Key.plus:
            pressureValue = self.pressure.value + 0.00001
            if pressureValue > 1.5:
                pressureValue = 1.5
            self.pressure.value = [pressureValue]

        if e["key"] == Sofa.constants.Key.minus:
            pressureValue = self.self.pressure.value - 0.00001
            if pressureValue < 0:
                pressureValue = 0
            self.pressure.value = [pressureValue]


    # def onAnimateBeginEvent(self, event):
        
    #     print('ád')


def createScene(rootNode):
    rootNode.gravity.value = [0, -9810, 0]
    rootNode.dt = 0.01

    rootNode.addObject("RequiredPlugin",pluginName="Softrobots SofaPython3 STLIB SofaGeneralObjectInteraction SofaMeshCollision SofaDeformable SofaEngine SofaLoader SofaOpenglVisual SofaGeneralSimpleFem")
    rootNode.addObject("VisualStyle",displayFlags="showVisualModels hideBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe")
    rootNode.addObject("DefaultVisualManagerLoop")
    rootNode.addObject("DefaultPipeline", name="CollisionPipeline", draw=0)
    rootNode.addObject("FreeMotionAnimationLoop")
    rootNode.addObject("GenericConstraintSolver",name="constraint solver", tolerance=1e-12,maxIterations=100000,computeConstraintForces=0)
    rootNode.addObject("LCPConstraintSolver", maxIt = "1000", tolerance = "0.001")
    rootNode.addObject("BruteForceBroadPhase")
    rootNode.addObject("BVHNarrowPhase")
    rootNode.addObject("DefaultContactManager", name="collision response", response="FrictionContactConstraint", responseParams="mu=0.6")
    rootNode.addObject("LocalMinDistance", name="Proximity", alarmDistance=contact_alarm, contactDistance=contact_distance, angleCone=0.1)
    rootNode.addObject("DiscreteIntersection")
    rootNode.addObject("OglSceneFrame", style="Arrows", alignment="TopRight")

    ## Whisker node

    skin = rootNode.addChild("whisker")
    skin.addObject("EulerImplicitSolver", name="cg_odesolver")
    # skin.addObject('CGLinearSolver', name='linearSolver', tolerance="1e-09", threshold="1e-12")
    skin.addObject("SparseLDLSolver",  name="linearSolver", template="CompressedRowSparseMatrixMat3x3d")
    skin.addObject("MeshVTKLoader", filename="mesh/whisker_init_vtk.vtk", name="loader", createSubelements=1, translation=[0, 0, 0], rotation=[0, 0, 0], flipNormals=0)
    skin.addObject("MechanicalObject", template="Vec3d", src="@loader", name="DOFs", showIndices=0, showIndicesScale=0.001, showColor="red")
    skin.addObject("TetrahedronSetTopologyContainer", src="@loader", name="topology")
    skin.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    skin.addObject("TetrahedronSetGeometryAlgorithms", name="GeomAlgo", template="Vec3d")
    skin.addObject("UniformMass", totalMass="0.000001", name="mass")
    skin.addObject("TetrahedralCorotationalFEMForceField", template="Vec3", name="FEM", method="large", poissonRatio=0.45, youngModulus=0.1562, updateStiffnessMatrix=0, rayleighStiffness=0)
    skin.addObject("BoxROI", template="Vec3d", box="-20 -20 -1 20 20 1", drawBoxes="1", name="FixedROI", computeEdges="1", computeTriangles="0",
        computeTetrahedra="0",
        computeHexahedra="0",
        drawSize="0.5",
    )

    skin.addObject("FixedConstraint", indices="@FixedROI.indices")
    skin.addObject("LinearSolverConstraintCorrection")

    # skin.addObject("BoxROI", template="Vec3d", box="-20 -20 110 20 20 170", drawBoxes="1", name="trash", drawSize="0.5", position = "@DOFs.position", tetrahedra = "@topology.tetrahedra")
    # skin.addObject("TopologicalChangeProcessor", listening = 1, useDataInputs = 1, tetrahedraToRemove="@trash.tetrahedronIndices", timeToRemove=0.1, interval=0.05)

    ## Collision node

    skinCollision = skin.addChild("SkinCollision")
    # skinCollision.addObject("MeshSTLLoader", filename="mesh/whisker_stl.stl", name="loader2", flipNormals=0, rotation=[180, 0, 0])
    # skinCollision.addObject("MeshTopology", src="@loader2", name="topology2")
    # skinCollision.addObject("TriangleSetTopologyContainer",src="@loader2", name="topology2")
    # skinCollision.addObject("MechanicalObject", name="collisMech")
    skinCollision.addObject("TriangleSetTopologyContainer", name="topology2")
    skinCollision.addObject("TriangleSetTopologyModifier", name="Modifier2")
    skinCollision.addObject("TriangleSetGeometryAlgorithms", name="GeomAlgo2", template="Vec3d")
    
    skinCollision.addObject("Tetra2TriangleTopologicalMapping", name="mapping", input="@../topology", output="@topology2")
    # skinCollision.addObject("TriangleCollisionModel", selfCollision=0)
    skinCollision.addObject("LineCollisionModel", selfCollision=0)
    skinCollision.addObject("PointCollisionModel", selfCollision=0)
    # skinCollision.addObject("SphereCollisionModel", radius="1")
    # skinCollision.addObject("BarycentricMapping")

    ## Visual node
    visual = skin.addChild("Visual")
    visual.addObject("OglModel", name="Visual", template="Vec3d", color="yellow")
    # visual.addObject("BarycentricMapping")
    visual.addObject("IdentityMapping", template="Vec3d,Vec3d", name="visualMapping", input="@../DOFs", output="@Visual")
    
    ##########################################
    # Constraint							 #
    ##########################################
    cavity = skin.addChild('cavity')
    cavity.addObject('MeshSTLLoader', name='loader', filename='mesh/whisker_chamber_stl.stl',rotation=[90, 0, 0])
    cavity.addObject('MeshTopology', src='@loader', name='topo')
    cavity.addObject('MechanicalObject', name='cavity')
    cavity.addObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3', value=0.000001,
                        triangles='@topo.triangles', valueType='pressure')
    cavity.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)

    ##########################################
    # Fibers                                 #
    ##########################################
    for fiber_idx in range (2):
        fiber = skin.addChild('fiber'+str(fiber_idx))
        fiber.addObject("MechanicalObject", template="Vec3", name="DOF",
                        position=fiber_dof[fiber_idx],
                        showObject=True, showObjectScale=1,translation=[0, 0, 0.1])
        fiber.addObject('MeshTopology', name='lines', lines=[[i, i + 1] for i in range(len(fiber1)-1)]) 
        fiber.addObject('UniformMass', totalMass=0.000000000000000000000008)
        fiber.addObject("FixedConstraint", name="FixedConstraint", indices=[0])

        fiber.addObject("StiffSpringForceField", template="Vec3d", name="springs", showArrowSize=0.1, drawMode=1,spring=spring_info[fiber_idx])
        fiber.addObject('BarycentricMapping', name='mapping')
        skin.addObject('MechanicalMatrixMapper', template="Vec3,Vec3", name="mapper"+str(fiber_idx),
                         nodeToParse=fiber.linkpath,  # where to find the forces to map
                         object1=skin.DOFs.linkpath, parallelTasks = 0)  # where to map the forces)  # in case of multi-mapping, here you can give the second parent
    

    
    planeNode = rootNode.addChild('Plane')
    planeNode.addObject('MeshSTLLoader', name='loader', filename='mesh/plane.stl', translation=[130, 0, 100], flipNormals=1)
    planeNode.addObject('MeshTopology', src='@loader')
    planeNode.addObject('MechanicalObject', src='@loader')
    # planeNode.addObject('TriangleCollisionModel')
    # planeNode.addObject('LineCollisionModel')
    # planeNode.addObject('PointCollisionModel')
    planeNode.addObject("SphereCollisionModel", radius="6")
    planeNode.addObject('OglModel', name='Visual', src='@loader', color=[1, 0, 0, 1])

    rootNode.addObject(controller(name="MyController", node=rootNode))

    return rootNode


def main():
    import Sofa.Gui
    import SofaRuntime
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")
    SofaRuntime.importPlugin("SofaComponentAll")
    # Check and save if the script is called from python environment
    global _runAsPythonScript
    _runAsPythonScript = True

    # Create and initialize the scene
    root = Sofa.Core.Node("rootNode")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()
    print("End of simulation.")

# Function used only if this script is called from a python environment
if __name__ == "__main__":
    main()
