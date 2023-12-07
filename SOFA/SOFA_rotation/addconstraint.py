from splib3.objectmodel import SofaPrefab
from splib3.numerics import getOrientedBoxFromTransform


def FixingBox(
    parent,
    target,
    name="FixingBox",
    translation=[0.0, 0.0, 0.0],
    eulerRotation=[0.0, 0.0, 0.0],
    scale=[1.0, 1.0, 1.0],
):
    """Fix a set of 'dofs' according to a translation & orientation"""

    ob = getOrientedBoxFromTransform(
        translation=translation, eulerRotation=eulerRotation, scale=scale
    )

    self = parent.addChild(name)
    self.addObject(
        "BoxROI",
        orientedBox=ob,
        name="BoxROI",
        position=target.dofs.getData("rest_position").getLinkPath(),
        drawBoxes=False,
    )

    c = self.addChild("Constraint")
    target.addChild(c)

    c.addObject(
        "RestShapeSpringsForceField",
        points=self.BoxROI.getData("indices").getLinkPath(),
        stiffness=1e12,
    )
    return self


def PartialBox(
    parent,
    target,
    name="PartialBox",
    translation=[0.0, 0.0, 0.0],
    eulerRotation=[0.0, 0.0, 0.0],
    scale=[1.0, 1.0, 1.0],
):
    """Fix a set of 'dofs' according to a translation & orientation"""

    ob = getOrientedBoxFromTransform(
        translation=translation, eulerRotation=eulerRotation, scale=scale
    )

    self = parent.addChild(name)
    self.addObject(
        "BoxROI",
        orientedBox=ob,
        name="BoxROI",
        position=target.dofs.getData("rest_position").getLinkPath(),
        drawBoxes=False,
    )

    c = self.addChild("Constraint")
    target.addChild(c)
    c.addObject(
        "PartialFixedConstraint",
        name="partialFixedConstraint",
        indices=self.BoxROI.getData("indices").getLinkPath(),
        fixedDirections="1 0 1",
        projectVelocity = 1
    )
    return self

def PartialBox(
    parent,
    target,
    name="PartialBox",
    translation=[0.0, 0.0, 0.0],
    eulerRotation=[0.0, 0.0, 0.0],
    scale=[1.0, 1.0, 1.0],
):
    """Fix a set of 'dofs' according to a translation & orientation"""

    ob = getOrientedBoxFromTransform(
        translation=translation, eulerRotation=eulerRotation, scale=scale
    )

    self = parent.addChild(name)
    self.addObject(
        "BoxROI",
        orientedBox=ob,
        name="BoxROI",
        position=target.dofs.getData("rest_position").getLinkPath(),
        drawBoxes=False,
    )

    c = self.addChild("Constraint")
    target.addChild(c)
    c.addObject(
        "PartialFixedConstraint",
        name="partialFixedConstraint",
        indices=self.BoxROI.getData("indices").getLinkPath(),
        fixedDirections="1 0 1",
        projectVelocity = 1
    )
    return self
