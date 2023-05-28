from wtforms import fields,widgets
from wtforms.validators import InputRequired




class EnumSelectField(fields.SelectField):
    widget = widgets.Select()

    def __init__(self, enum, *args, **kwargs):
        super(EnumSelectField, self).__init__(*args, **kwargs)
        self.enum = enum
        self.choices = [(choice.value, choice.name) for choice in enum]

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.enum(valuelist[0])
        else:
            self.data = None

    def pre_validate(self, form):
        pass
