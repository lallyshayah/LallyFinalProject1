from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField , HiddenField , DateTimeField , IntegerField , DecimalField , FloatField , RadioField
from wtforms import Form, SelectMultipleField , BooleanField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired




class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"

class SinglePresidentForm(FlaskForm):
    president = SelectField('President' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    start_date = DateField('Start Date' , format='%Y-%m-%d' , validators = [DataRequired])
    end_date = DateField('End Date' , format='%Y-%m-%d' , validators = [DataRequired])
    kind = SelectField('Chart Kind' , validators = [DataRequired] , choices=[('line', 'line'), ('bar', 'bar')])
    subnmit = SubmitField('הצג')


class AllOfTheAboveForm(FlaskForm):
    string_field_entry = StringField('Enter a String:' , validators = [DataRequired])
    text_area_field_entry = TextAreaField('Enter Text:' , validators = [DataRequired])
    password_field_entry = PasswordField('Enter Password:' , validators = [DataRequired])
    date_field_entry = DateField('Enter Date:' , format='%Y-%m-%d' , validators = [DataRequired])
    integer_field_entry = IntegerField('Enter an Integer:' , validators = [DataRequired])
    decimal_field_entry = DecimalField('Enter a Decimal:' , validators = [DataRequired])
    boolean_field_entry = BooleanField('Enter a Boolean:' , validators = [DataRequired])
    radio_field_entry = RadioField('Choose one of:' , validators = [DataRequired] , choices=[('1', 'A'), ('2', 'B'), ('3', 'C') , ('4', 'D')])
    select_field_entry = SelectField('Select:' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    select_field_multiple_entry = SelectMultipleField('Select Multiple:' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    subnmit = SubmitField('submit')


class Covid19DayRatio(FlaskForm):
    countries = SelectMultipleField('Select Multiple:' , validators = [DataRequired] )
    start_date = DateField('Start Date (1/22/20 onwards):' , format='%Y-%m-%d' , validators = [DataRequired])
    end_date = DateField('End Date (Yesterday backwards):' , format='%Y-%m-%d' , validators = [DataRequired])
    rolling_window = IntegerField('Mean over days window size:' , validators = [DataRequired])
    subnmit = SubmitField('submit')

class OlympicMedals(FlaskForm):
    country = SelectField('Select a Country:' , validators = [DataRequired] )
    subnmit = SubmitField('submit')

class YomLayla(FlaskForm):
    yl = RadioField('Choose Day or Night:' , validators = [DataRequired] , choices=[('1', 'Day'), ('5', 'Night')])
    subnmit = SubmitField('Submit')