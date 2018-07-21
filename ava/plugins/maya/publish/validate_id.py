import pyblish.api


class ValidateAvaID(pyblish.api.InstancePlugin):
    """All models must have an ID attribute"""

    label = "Ava ID"
    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    families = [
        "ava.model",
        "ava.lookdev",
    ]

    def process(self, instance):
        from maya import cmds

        nodes = list(instance)
        nodes += cmds.listRelatives(instance, allDescendents=True) or list()
        missing = list()

        for node in nodes:

            # Only check transforms with shapes that are meshes
            if not cmds.nodeType(node) == "transform":
                continue

            shapes = cmds.listRelatives(node,
                                        shapes=True,
                                        type="mesh") or list()
            meshes = cmds.ls(shapes, type="mesh")

            if not meshes:
                continue

            try:
                self.log.info("Checking '%s'" % node)
                cmds.getAttr(node + ".mbID")
            except ValueError:
                missing.append(node)

        assert not missing, ("Missing ID attribute on: %s"
                             % ", ".join(missing))
