import pyblish.api


class ValidateAvaRigHierarchy(pyblish.api.InstancePlugin):
    """A rig must reside under a single assembly called "ROOT"

    - Must reside within `ROOT` transform

    """

    label = "Rig Hierarchy"
    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    families = ["ava.rig"]

    def process(self, instance):
        from maya import cmds

        assert cmds.ls(instance, assemblies=True) == ["ROOT"], (
            "Rig must have a single parent called 'ROOT'.")
