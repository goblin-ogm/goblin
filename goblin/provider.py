from typing import Dict, Any

class Provider:
    """Superclass for provider plugins"""
    DEFAULT_OP_ARGS: Dict[Any, Any] = {}

    @classmethod
    def get_default_op_args(cls, processor):
        return cls.DEFAULT_OP_ARGS.get(processor, dict())


class TinkerGraph(Provider):  # TODO
    """Default provider"""

    @staticmethod
    def get_hashable_id(val):
        return val

class JanusGraph(Provider):  # TODO
    """Default provider"""

    @staticmethod
    def get_hashable_id(val):
        if not isinstance(val, dict):
            return val
        type_prop = val.get("@type", None)
        if not type_prop == "janusgraph:RelationIdentifier":
            return val
        val_prop = val.get("@value", None)
        if not isinstance(val_prop, dict):
            return val
        rel_prop = val_prop.get("relationId", None)
        if not rel_prop:
            return val
        return rel_prop

