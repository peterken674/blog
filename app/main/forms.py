from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length

class NewBlog(FlaskForm):
    title = StringField("", validators =[Required()], render_kw={"placeholder": "Blog title..."})
    content = TextAreaField("", render_kw={"placeholder": "Tell your story..."})
    submit = SubmitField('Publish')