from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length

CATEGORIES = [('tech', 'Tech'), ('scince', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active post')
    publish_date = DateField('Publish date', validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Submit')

