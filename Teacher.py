from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators


class CreateTeacher(FlaskForm):
    tc_info = StringField("tc_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    tc_recomendation = StringField("tc_recomendation: ", [
        validators.DataRequired("Please enter your recomendation.")

    ])



    submit = SubmitField("Save")


class EditTeacher(FlaskForm):
    tc_info = StringField("tc_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    tc_recomendation = StringField("tc_recomendation: ", [
        validators.DataRequired("Please enter your recomendation.")

    ])



    submit = SubmitField("Save")