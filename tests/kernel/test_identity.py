from kernel.identity import (
    EntityType, authenticate_entity
)


def test_authenticate_identity_default():
    result = authenticate_entity()
    assert result.entity_type is EntityType.anon
    assert result.entity_id is None


def test_authenticate_identity_no_entity_type():
    result = authenticate_entity(entity_id='foo')
    assert result.entity_type is EntityType.anon
    assert result.entity_id is None


def test_authenticate_identity_no_entity_id():
    result = authenticate_entity(entity_type=EntityType.user)
    assert result.entity_type is EntityType.anon
    assert result.entity_id is None


def test_authenticate_identity_type_and_entity_provided():
    result = authenticate_entity(entity_type=EntityType.user, entity_id='foo')
    assert result.entity_type is EntityType.user
    assert result.entity_id is 'foo'
