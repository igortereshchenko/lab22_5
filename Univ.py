from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms import validators

def valid1(FlaskForm, field):
    if int (field.birthday) < 0:
        raise ValidationError ('Birthday > 0')

def valid2(FlaskForm, field):
    if field.city != 'Lviv' or 'Kyiv':
        raise ValidationError ('Enter Lviv or Kyiv')

class CreateUniv(FlaskForm):
    city = StringField("city: ", [
        validators.DataRequired("Please enter city info."), valid2
    ])

    name = StringField("name: ", [
        validators.DataRequired("Please enter name .")

    ])

    rector = IntegerField("rector: ", [
        validators.DataRequired("Please enter rector.")

    ])

    birthday = IntegerField("birthday: ", [
        validators.DataRequired("Please enter birthday."), valid1

    ])

    submit = SubmitField("Save")
