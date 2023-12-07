import Sofa
import os
import SofaRuntime
import Sofa.Core
import Sofa.Gui
import Sofa.Simulation
import csv
import math as m
import math
import sys
import shutil
from SofaRuntime import Timer


 
USE_GUI = 1
contact_distance = 5
contact_alarm = 7

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
                    rest_pos[i][3],
                    rest_pos[i][4],
                    rest_pos[i][5],
                    rest_pos[i][6],
                ]
            ]
        return str_out

    # def changeRestPos(self, rest_pos, x, y, z):
    #     str_out = " "
    #     for i in range(0, len(rest_pos)):
    #         str_out = str_out + " " + str(x)
    #         str_out = str_out + " " + str(y)
    #         str_out = str_out + " " + str(z)
    #         str_out = str_out + " " + str(rest_pos[i][3])
    #         str_out = str_out + " " + str(rest_pos[i][4])
    #         str_out = str_out + " " + str(rest_pos[i][5])
    #         str_out = str_out + " " + str(rest_pos[i][6])

    #     return str_out

    def rotateRestPos(self,rest_pos,rx,centerPosX,centerPosZ):
        out = []
        for i in range(0,len(rest_pos)) :
            newRestPosX = (rest_pos[i][0] - centerPosX)*math.cos(rx) - (rest_pos[i][2] - centerPosZ)*math.sin(rx) +  centerPosX
            newRestPosZ = (rest_pos[i][0] - centerPosX)*math.sin(rx) + (rest_pos[i][2] - centerPosZ)*math.cos(rx) +  centerPosZ
            out += [[newRestPosX, rest_pos[i][1], newRestPosZ]]
        return out

    # def movenext(self, x, y, z):
    #     str_out = []
    #     eulerz = math.atan2(y, x)
    #     cz = math.cos(eulerz * 0.5)
    #     sz = math.sin(eulerz * 0.5)
    #     cy = math.cos(90 * 0.5 * math.pi / 180.0)
    #     sy = math.sin(90 * 0.5 * math.pi / 180.0)
    #     cx = math.cos(0 * 0.5 * math.pi / 180.0)
    #     sx = math.sin(0 * 0.5 * math.pi / 180.0)
    #     qx = sx * cy * cz - cx * sy * sz
    #     qy = cx * sy * cz + sx * cy * sz
    #     qz = cx * cy * sz - sx * sy * cz
    #     w = cx * cy * cz + sx * sy * sz

    #     str_out += [
    #         [
    #             x + (self.dist_contact + self.pre_gap - 0.45) * math.cos(eulerz),
    #             y + (self.dist_contact + self.pre_gap - 0.45) * math.sin(eulerz),
    #             z,
    #             qx,
    #             qy,
    #             qz,
    #             w,
    #         ]
    #     ]
    #     self.MecaObjectfinger.findData("position").value = str_out
    #     self.MecaObjectfinger.findData("rest_position").value = str_out
    #     self.rotAngle = eulerz
    #     return eulerz, self.rotAngle

    # def convert_euler2quaternion(self, eulerx, eulery, eulerz):
    #     str_out = []
    #     cz = math.cos(eulerz * 0.5 * math.pi / 180.0)
    #     sz = math.sin(eulerz * 0.5 * math.pi / 180.0)
    #     cy = math.cos(eulery * 0.5 * math.pi / 180.0)
    #     sy = math.sin(eulery * 0.5 * math.pi / 180.0)
    #     cx = math.cos(eulerx * 0.5 * math.pi / 180.0)
    #     sx = math.sin(eulerx * 0.5 * math.pi / 180.0)
    #     qx = sx * cy * cz - cx * sy * sz
    #     qy = cx * sy * cz + sx * cy * sz
    #     qz = cx * cy * sz - sx * sy * cz
    #     w = cx * cy * cz + sx * sy * sz
    #     str_out += [qx, qy, qz, w]
    #     return str_out

    # def resetskinshape(self):
    #     self.MecaObjectROBIN_actuator.findData("position").value = self.MecaObjectROBIN_actuator.findData("reset_position").value

    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node = kw["node"]
        self.dt = self.node.findData("dt").value
        self.current_time = 0
        # ROBIN node
        self.robin = self.node.getChild("ROBIN_actuator")

        # Rot plane
        self.rotplane = self.node.getChild("rot_plane")
        self.rotplane_meca = self.rotplane.getObject("rot_plane")

    def onKeypressedEvent(self,e):
        self.rotate_center = [0,50,0]
        angle = m.pi / 300
        if e["key"] == "+":
            self.rotplane_meca.rest_position.value = self.rotateRestPos(self.rotplane_meca.rest_position.value,angle,0,0)

        if e["key"] == "-":
            self.rotplane_meca.rest_position.value = self.rotateRestPos(self.rotplane_meca.rest_position.value,-angle,0,0)

    def onAnimateBeginEvent(self, event):
        self.current_time += self.dt
        # if self.current_time < 2*self.dt:
        #     self.indices1 = []
        #     self.indices2 = []
        #     self.factor = []
        #     self.freeROI_ind = self.robin.getObject("freeROI").indices
        #     self.rot_planeROI_ind = self.rotplane.getObject("rot_planeROI").indices
        #     self.freeROI_pos = self.robin.getObject("freeROI").pointsInROI.value
        #     self.rot_planeROI_pos = self.rotplane.getObject("rot_planeROI").pointsInROI.value
        #     for i in range(len(self.rot_planeROI_ind)):
        #         for j in range(len(self.freeROI_ind)):
        #             diff = m.sqrt((self.freeROI_pos[j][0] - self.rot_planeROI_pos[i][0])** 2 + (self.freeROI_pos[j][2] - self.rot_planeROI_pos[i][2])** 2)
        #             if diff <= 0.1:
        #                 self.indices1.append(self.rot_planeROI_ind[i])
        #                 self.indices2.append(self.freeROI_ind[j])
        #                 self.factor.append(1)
        #                 break

        #     print(self.indices1)
        #     print(len(self.indices1))
        #     print(self.indices2)
        #     print(len(self.indices2))
        #     print(self.factor)
        #     self.node.getObject("attach").indices1 = self.indices1
        #     self.node.getObject("attach").indices2 = self.indices2
        #     self.node.getObject("attach").constraintFactor = self.factor
        

def createScene(rootNode):

    rootNode.gravity.value = [0,0, -9810]
    rootNode.dt = 0.01

    rootNode.addObject("RequiredPlugin",
        pluginName="SofaPython3 SoftRobots STLIB MultiThreading SofaGeneralObjectInteraction SofaSparseSolver SofaMeshCollision SofaDeformable SofaGeneralEngine SofaEngine SofaConstraint SofaExporter "
        "SofaImplicitOdeSolver SofaLoader SofaRigid SofaSimpleFem SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem",)
    rootNode.addObject("VisualStyle",
        displayFlags="showVisualModels hideBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe",)
    rootNode.addObject("DefaultVisualManagerLoop")
    rootNode.addObject("DefaultPipeline", name="CollisionPipeline")
    rootNode.addObject("FreeMotionAnimationLoop", parallelODESolving=0)
    rootNode.addObject("GenericConstraintSolver",name="constraint solver", tolerance=1e-12,maxIterations=100000,computeConstraintForces=0)
    # rootNode.addObject("LCPConstraintSolver", maxIt = "1000", tolerance = "0.001")
    rootNode.addObject("BruteForceBroadPhase")
    rootNode.addObject("BVHNarrowPhase")
    rootNode.addObject("DefaultContactManager", name="collision response", response="FrictionContactConstraint", responseParams="mu=0.6")
    rootNode.addObject("LocalMinDistance", name="Proximity", alarmDistance=contact_alarm, contactDistance=contact_distance, angleCone=0.1)
    rootNode.addObject("DiscreteIntersection")
    rootNode.addObject("OglSceneFrame", style="Arrows", alignment="TopRight")


    ## ROBIN_actuator node

    ROBIN_actuator = rootNode.addChild("ROBIN_actuator")
    ROBIN_actuator.addObject("EulerImplicitSolver", name="cg_odesolver")
    # ROBIN_actuator.addObject('CGLinearSolver', name='linearSolver', tolerance="1e-2", threshold="1e-2")
    ROBIN_actuator.addObject("SparseLDLSolver",  name="linearSolver", template="CompressedRowSparseMatrixMat3x3d")
    ROBIN_actuator.addObject("MeshVTKLoader", filename="mesh/test_vtk.vtk", name="loader", createSubelements=1, translation=[0, 0, 0], rotation=[0, 0, 0])
    ROBIN_actuator.addObject("MechanicalObject", template="Vec3d", src="@loader", name="DOFs", showIndices=0, showIndicesScale=0.001, showColor="red")
    ROBIN_actuator.addObject("TetrahedronSetTopologyContainer", src="@loader", name="topology")
    ROBIN_actuator.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    ROBIN_actuator.addObject("TetrahedronSetGeometryAlgorithms", name="GeomAlgo", template="Vec3d")
    ROBIN_actuator.addObject("UniformMass", totalMass="0.000000028", name="mass")
    # ROBIN_actuator.addObject("TetrahedronHyperelasticityFEMForceField", name="FEM", ParameterSet="3000 3000", materialName="NeoHookean")
    ROBIN_actuator.addObject("TetrahedronFEMForceField", template="Vec3", name="FEM", method="large", poissonRatio=0.45, youngModulus=0.0002)
    ROBIN_actuator.addObject("BoxROI", template="Vec3d", box="-40 -0.1 -40 40 0.1 40", drawBoxes="0", name="Partial_FixedROI", computeEdges="1", computeTriangles="0",
        computeTetrahedra="0", computeHexahedra="0", drawSize="0.5")

    ROBIN_actuator.addObject("PartialFixedConstraint", name="partialFixedConstraint", indices="@Partial_FixedROI.indices", fixedDirections="1 1 1")
    ROBIN_actuator.addObject("BoxROI", template="Vec3d", box="-40 49.8 -40 40 50.2 40", drawBoxes="1", name="freeROI", computeEdges="1", computeTriangles="0",
        computeTetrahedra="0", computeHexahedra="0", drawSize="0.5")
    ROBIN_actuator.addObject("RestShapeSpringsForceField", points="@freeROI.indices", stiffness=1e12, angularStiffness=1e12, drawSpring="true")

    ROBIN_actuator.addObject("LinearSolverConstraintCorrection", solverName="linearSolver")
    # ROBIN_actuator.addObject('UncoupledConstraintCorrection')

    ## Collision node
    Collision = ROBIN_actuator.addChild("SkinCollision")
    Collision.addObject("MeshTopology", src="@../loader", name="topology")
    Collision.addObject("MechanicalObject", name="collisMech")
    # Collision.addObject("TriangleCollisionModel", selfCollision=0)
    Collision.addObject("LineCollisionModel", selfCollision=0)
    Collision.addObject("PointCollisionModel", selfCollision=0)
    Collision.addObject("BarycentricMapping")

    ## Visual node
    visual = ROBIN_actuator.addChild("Visual")
    visual.addObject("OglModel", name="Visual", template="Vec3d", color="yellow")
    # visual.addObject("BarycentricMapping")
    visual.addObject("IdentityMapping", template="Vec3d,Vec3d", name="visualMapping", input="@../DOFs", output="@./")
    
    
    ##Rotate plane node
    rot_plane = rootNode.addChild("rot_plane")
    rot_plane.addObject("EulerImplicitSolver", name="cg_odesolver")
    # rot_plane.addObject('CGLinearSolver', name='linearSolver', tolerance="1e-2", threshold="1e-2")
    rot_plane.addObject("SparseLDLSolver",  name="linearSolver", template="CompressedRowSparseMatrixMat3x3d")
    rot_plane.addObject("MeshSTLLoader", filename="mesh/rotate_plane.stl", name="loader", createSubelements=1,  translation=[0, 0, 0])
    rot_plane.addObject("MechanicalObject", name="rot_plane", src = "@loader", template="Vec3d", translation=[0, 0, 0], rotation=[0, 0, 0], showObject=1, showObjectScale=10)
    rot_plane.addObject("BoxROI", template="Vec3d", box="-40 49.5 -40 40 50.5 40", drawBoxes="1", name="rot_planeROI",drawSize="0.5")
    rot_plane.addObject("TriangleSetTopologyContainer", src="@loader", name="topology")
    rot_plane.addObject("TriangleSetGeometryAlgorithms", name="GeomAlgo", template="Vec3d")
    rot_plane.addObject("UniformMass", totalMass="0.00000028", name="mass")
    rot_plane.addObject("TriangleFEMForceField", name="FEM2", youngModulus="5000", poissonRatio="0.3", method="large")
    rot_plane.addObject("RestShapeSpringsForceField", points="@rot_planeROI.indices", stiffness=1e12, angularStiffness=1e12, drawSpring="true")

    # rot_plane.addObject("LinearSolverConstraintCorrection", solverName="linearSolver")
    rot_plane.addObject('UncoupledConstraintCorrection')

    visual = rot_plane.addChild("Visual")
    visual.addObject("MeshSTLLoader", filename="mesh/rotate_plane.stl", name="loader", createSubelements=0,  translation=[0, 0, 0])
    visual.addObject("OglModel", name="visual_rot", template = "Vec3d", src = "@loader",  color="red")
    visual.addObject("IdentityMapping")

    rootNode.addObject("AttachConstraint", name = "attach", object1="@rot_plane", object2="@ROBIN_actuator", twoWay = True, indices1=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 
14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75], 
    indices2=[1511, 1521, 193, 1510, 1520, 11, 201, 1523, 1509, 19, 1522, 1508, 1513, 1516, 8, 1514, 1518, 
190, 204, 1519, 1515, 22, 1517, 1512, 9, 191, 203, 21, 1506, 1525, 14, 1507, 1524, 196, 198, 1504, 16, 1505, 187, 182, 207, 212, 12, 200, 194, 18, 0, 1, 17, 195, 199, 13, 15, 197, 209, 184, 185, 210, 192, 10, 20, 202, 4, 7, 189, 214, 180, 205, 211, 186, 208, 183, 181, 213, 206, 188], 
constraintFactor = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    rootNode.addObject(controller(name="MyController", node=rootNode))

    return rootNode


def main():

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
        Sofa.Gui.GUIManager.SetDimension(1080, 900)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


# Function used only if this script is called from a python environment
if __name__ == "__main__":
    main()
