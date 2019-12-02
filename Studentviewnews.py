from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators


class EditStudentviewnews(FlaskForm):
    ns_news_info = StringField("ns_news_info: ", [
        validators.DataRequired("Please enter news info.")

    ])

    st_info = StringField("st_info: ", [
        validators.DataRequired("Please enter your info.")

    ])
    submit = SubmitField("Save")


class CreateStudentviewnews(FlaskForm):
    ns_news_info = StringField("ns_news_info: ", [
        validators.DataRequired("Please enter news info.")

    ])

    st_info = StringField("st_info: ", [
        validators.DataRequired("Please enter your info.")

    ])
    submit = SubmitField("Save")