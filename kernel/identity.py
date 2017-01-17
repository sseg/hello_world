import attr
from enum import Enum
from typing import Optional


class EntityType(Enum):
    anon = 'anon'
    user = 'user'
    admin = 'admin'


@attr.s
class Entity:
    entity_type = attr.ib(
        default=EntityType.anon,
        validator=attr.validators.instance_of(EntityType)
    )
    entity_id = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


def authenticate_entity(
    entity_type: Optional[EntityType]=None,
    entity_id: Optional[str]=None
) -> Entity:
    # do any checks here
    if entity_type is None or entity_id is None:
        return Entity()
    return Entity(entity_type=entity_type, entity_id=entity_id)  # type: ignore
