from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [('tech', 'Tech'), ('scince', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active post')
    publish_date = DateTimeLocalField('Publish date', format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Submit')

