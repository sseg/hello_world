from sqlalchemy import Column, String, Integer, DateTime, Enum, func, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from kernel.backends import Base
from kernel.errors import DataNotFound
from kernel.identity import EntityType
import datetime


class Entity(Base):
    __tablename__ = "Entities"
    id = Column(Integer, primary_key=True)
    entity_type = Column(Enum(EntityType), nullable=False)
    entity_id = Column(String(32), nullable=True)
    unique_idx = UniqueConstraint('entity_type', 'entity_id')
    greetings = relationship("Greeting", backref="owner")


class Greeting(Base):
    __tablename__ = 'Greetings'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=True)
    template = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("Entities.id"))

    @classmethod
    def to_dict(_cls, row_proxy):
        return {
            'id': row_proxy.id,
            'name': row_proxy.name,
            'description': row_proxy.description,
            'template': row_proxy.template,
            'created_at': row_proxy.created_at,
            'updated_at': row_proxy.updated_at,
            'deleted_at': row_proxy.deleted_at,
            'owner': {
                'entity_type': row_proxy.owner.entity_type,
                'entity_id': row_proxy.owner.entity_id
            }
        }

    @classmethod
    def to_display(_cls, data):
        return {
            'id': data['id'],
            'name': data['name'],
            'description': data['description'],
            'template': data['template'],
            'created_at': datetime.datetime.isoformat(data['created_at']),
            'updated_at': datetime.datetime.isoformat(data['updated_at']),
            'owner': {
                'entity_type': data['owner']['entity_type'].value,
                'entity_id': data['owner']['entity_id']
            }
        }


def add_one(db, greeting):
    greeting['owner'] = Entity(**greeting['owner'])
    new_record = Greeting(**greeting)
    db.add(new_record)
    db.flush()
    return Greeting.to_dict(new_record)


def get_one(db, greet_id):
    record = db.query(Greeting).filter(
        Greeting.id == greet_id
    ).filter(
        Greeting.deleted_at.is_(None)
    ).first()
    if record is None:
        raise DataNotFound
    return Greeting.to_dict(record)


def update_one(db, greet_id, updates):
    record = db.query(Greeting).filter(
        Greeting.id == greet_id
    ).filter(
        Greeting.deleted_at.is_(None)
    ).first()
    if record is None:
        raise DataNotFound
    for k, v in updates.items():
        setattr(record, k, v)
    return Greeting.to_dict(record)


def delete_one(db, greet_id):
    record = db.query(Greeting).filter(
        Greeting.id == greet_id
    ).filter(
        Greeting.deleted_at.is_(None)
    ).first()
    if record is None:
        raise DataNotFound
    record.deleted_at = func.now()
    return Greeting.to_dict(record)


def get_all(db):
    records = db.query(Greeting).filter(
        Greeting.deleted_at.is_(None)
    ).all()
    return [
        Greeting.to_dict(r)
        for r in records
    ]
