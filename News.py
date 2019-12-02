from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators


class EditNews(FlaskForm):
    ns_news_info = StringField("ns_news_info: ", [
        validators.DataRequired("Please enter news info.")

    ])

    rs_info = StringField("rs_info: ", [
        validators.DataRequired("Please enter resource info.")

    ])

    ns_likes = IntegerField("ns_likes: ", [
        validators.DataRequired("Please enter your like number.")

    ])

    submit = SubmitField("Save")


class CreateNews(FlaskForm):
    ns_news_info = StringField("ns_news_info: ", [
        validators.DataRequired("Please enter news info.")

    ])

    rs_info = StringField("rs_info: ", [
        validators.DataRequired("Please enter resource info.")

    ])

    ns_likes = IntegerField("ns_likes: ", [
        validators.DataRequired("Please enter your like.")

    ])

    submit = SubmitField("Save")