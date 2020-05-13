from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField , HiddenField , DateTimeField , IntegerField , DecimalField , FloatField , RadioField
from wtforms import Form, SelectMultipleField , BooleanField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField
from wtforms import widgets

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"

class SinglePresidentForm(FlaskForm):
    president = MultiCheckboxField('President' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    #start_date = DateField('Start Date' , format='%Y-%m-%d' , validators = [DataRequired])
    #end_date = DateField('End Date' , format='%Y-%m-%d' , validators = [DataRequired])
    kind = SelectField('Chart Kind' , validators = [DataRequired] , choices=[('line', 'line'), ('bar', 'bar')])
    subnmit = SubmitField('הצג')


