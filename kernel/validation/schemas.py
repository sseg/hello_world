import jsl


class Greeting(jsl.Document):
    template = jsl.StringField(required=True, max_length=250)
    name = jsl.StringField(required=True, max_length=100)
    description = jsl.StringField(max_length=250)


class GreetingPatch(jsl.Document):
    template = jsl.StringField(max_length=250)
    name = jsl.StringField(max_length=100)
    description = jsl.StringField(max_length=250)


class DoGreetingArgs(jsl.Document):
    template_args = jsl.DictField(
        additional_properties=jsl.StringField(max_length=100),
        max_properties=32,
        required=True
    )

greeting_schema = Greeting.get_schema()
greeting_patch_schema = GreetingPatch.get_schema()
do_greeting_schema = DoGreetingArgs.get_schema()
