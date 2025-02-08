from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class AboutForm(FlaskForm):
    greeting = StringField("Begrüßung", validators=[DataRequired()])
    bio = TextAreaField("Bio", validators=[DataRequired()])
    role = StringField("Rolle", validators=[Optional()])
    submit = SubmitField("Speichern")
