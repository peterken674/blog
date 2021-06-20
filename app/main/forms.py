from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class NewBlog(FlaskForm):
    title = StringField("", validators =[Required()], render_kw={"placeholder": "Blog title..."})
    content = TextAreaField("", render_kw={"placeholder": "Tell your story..."})
    submit = SubmitField('Publish')

class NewComment(FlaskForm):
    comment = TextAreaField("", render_kw={"placeholder": "Share your thoughts..."})
    submit = SubmitField('Comment')

class UpdateProfilePic(FlaskForm):
    profile = FileField('Change Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images only allowed.')])
    submit = SubmitField('Change')