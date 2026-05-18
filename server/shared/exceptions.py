class HominunError(Exception):
    """Base exception for all domain errors."""


class EntityNotFoundError(HominunError):
    pass


class InvalidActionError(HominunError):
    pass


class SaveVersionMismatchError(HominunError):
    pass


class NarrativeConditionError(HominunError):
    pass


class CombatResolverError(HominunError):
    pass
