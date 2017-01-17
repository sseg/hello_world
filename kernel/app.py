from kernel.identity import Entity
from kernel.services import greetings_service
from kernel.backends import configure_db
import attr


@attr.s
class Session:
    proxied = attr.ib()
    entity = attr.ib(validator=attr.validators.instance_of(Entity))
    db_session = attr.ib()

    def do(self, op):
        return op(entity=self.entity, db=self.db_session)

    def __getattr__(self, name):
        if name == 'session':
            raise RuntimeError("Nested sessions are not allowed!")
        return getattr(self.proxied, name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            self.db_session.rollback()
        else:
            self.db_session.commit()
        self.db_session.close()


class HelloKernel:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    def initialize_backends(self):
        self.session_maker = configure_db(**self.db_settings)
        self.greetings = greetings_service

    def session(self, entity: Entity) -> Session:
        db_session = self.session_maker()
        return Session(proxied=self, entity=entity, db_session=db_session)  # type: ignore
