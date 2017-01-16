from kernel.validation.schemas import (
    greeting_schema,
    greeting_patch_schema,
    do_greeting_schema
)
from kernel.validation import validate_input
from kernel.repos import greetings_repo


def add(resource):
    validate_input(resource, greeting_schema)

    def scoped(**context):
        entity = context['entity']
        with_owner = dict(
            owner={
                'entity_type': entity.entity_type,
                'entity_id': entity.entity_id
            },
            **resource
        )
        data = greetings_repo.add_one(context['db'], with_owner)
        return greetings_repo.Greeting.to_display(data)
    return scoped


def get(id):
    def scoped(**context):
        data = greetings_repo.get_one(context['db'], id)
        return greetings_repo.Greeting.to_display(data)
    return scoped


def update(id, updates):
    validate_input(updates, greeting_patch_schema)

    def scoped(**context):
        data = greetings_repo.update_one(context['db'], id, updates)
        return greetings_repo.Greeting.to_display(data)
    return scoped


def delete(id):
    def scoped(**context):
        data = greetings_repo.delete_one(context['db'], id)
        return greetings_repo.Greeting.to_display(data)
    return scoped


def get_all():
    def scoped(**context):
        data = greetings_repo.get_all(context['db'])
        return [greetings_repo.Greeting.to_display(r) for r in data]
    return scoped


def say_hello(id, args):
    validate_input(args, do_greeting_schema)

    def scoped(**context):
        data = greetings_repo.get_one(context['db'], id)
        template = data['template']
        return template.format(**args['template_args'])
    return scoped
