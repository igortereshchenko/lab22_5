from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms import validators


class CreateResources(FlaskForm):
    rs_info = StringField("rs_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    tc_info = StringField("tc_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    rs_activity = BooleanField("rs_activity: ", [
        validators.DataRequired("Please enter your activity.")

    ])

    submit = SubmitField("Save")


class EditResources(FlaskForm):
    rs_info = StringField("rs_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    tc_info = StringField("tc_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    rs_activity = BooleanField("rs_activity: ")

    submit = SubmitField("Save")