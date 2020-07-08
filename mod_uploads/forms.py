from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class FileUploadForm(FlaskForm):
    file = FileField(validators=[DataRequired()])
    upload_file = SubmitField(validators=[DataRequired()])
