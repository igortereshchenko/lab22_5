from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators


class CreateStudent(FlaskForm):
    st_info = StringField("st_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    st_review = StringField("st_review: ", [
        validators.DataRequired("Please enter your review.")

    ])

    st_document = StringField("st_document: ", [
        validators.DataRequired("Please enter your document.")

    ])

    submit = SubmitField("Save")


class EditStudent(FlaskForm):
    st_info = StringField("st_info: ", [
        validators.DataRequired("Please enter your info.")

    ])

    st_review = StringField("st_review: ", [
        validators.DataRequired("Please enter your review.")

    ])

    st_document = StringField("st_document: ", [
        validators.DataRequired("Please enter your document.")

    ])

    submit = SubmitField("Save")