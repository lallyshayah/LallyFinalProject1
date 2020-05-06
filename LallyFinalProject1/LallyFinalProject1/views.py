"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from LallyFinalProject1 import app
from flask import Flask, flash, request, redirect

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from LallyFinalProject1.Models.Forms import ExpandForm
from LallyFinalProject1.Models.Forms import CollapseForm
from LallyFinalProject1.Models.Forms import SinglePresidentForm
from LallyFinalProject1.Models.Forms import AllOfTheAboveForm
from LallyFinalProject1.Models.Forms import Covid19DayRatio
from LallyFinalProject1.Models.Forms import OlympicMedals
from LallyFinalProject1.Models.Forms import YomLayla
from LallyFinalProject1.Models.plot_service_functions import plot_case_1
from LallyFinalProject1.Models.plot_service_functions import plot_to_img
from LallyFinalProject1.Models.plot_service_functions import covid19_day_ratio
from LallyFinalProject1.Models.plot_service_functions import get_countries_choices
from LallyFinalProject1.Models.general_service_functions import htmlspecialchars
from LallyFinalProject1.Models.QueryFormStructure import QueryFormStructure 
from LallyFinalProject1.Models.QueryFormStructure import LoginFormStructure 
from LallyFinalProject1.Models.QueryFormStructure import UserRegistrationFormStructure 

from wtforms.fields.html5 import DateField , DateTimeField

from os import path
import io

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from LallyFinalProject1.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

db_Functions = create_LocalDatabaseServiceRoutines() 

app.config['SECRET_KEY'] = 'The first argument to the field'


@app.route('/')
@app.route('/home')
def home():

    print("Home")

    """Renders the home page."""
    
    return render_template(
        'index.html',
        title='',
        img_american_flag = '/static/imgs/american_flag.jpg',
        year=datetime.now().year
    )

@app.route('/contact')
def contact():

    print("Contact")

    """Renders the contact page."""

    return render_template(
        'contact.html',
        title = 'Contact',
        year=datetime.now().year,
        img_tichonet = '/static/imgs/tichonet.png',
        img_oran = '/static/imgs/oran.jpg'
    )

@app.route('/about')
def about():

    print("About")

    """Renders the about page."""
    return render_template(
        'about.html',
        year=datetime.now().year,
        img_tichonet = '/static/imgs/tichonet.png'
    )

@app.route('/data')
def data():

    print("Data")

    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My data page.',
        img_trump = '/static/imgs/trump.jpg',
        img_obama = '/static/imgs/obama.jpg',
        img_bush = '/static/imgs/bush.jpg',
        img_clinton = '/static/imgs/clinton.jpg'
    )

@app.route('/query' , methods = ['GET' , 'POST'])
def query():

    print("Query")

    form1 = SinglePresidentForm()
    chart = {}
    height_case_1 = "100"
    width_case_1 = "250"

    df_trump = pd.read_csv(path.join(path.dirname(__file__), 'static/data/trump.csv'))
    df_obama = pd.read_csv(path.join(path.dirname(__file__), 'static/data/obama.csv'))
    df_bush = pd.read_csv(path.join(path.dirname(__file__), 'static/data/bush.csv'))
    df_clinton = pd.read_csv(path.join(path.dirname(__file__), 'static/data/clinton.csv'))
    presidents_dict = {'trump' : df_trump , 'obama' : df_obama , 'bush' : df_bush , 'clinton' : df_clinton }

    if request.method == 'POST':
        president = form1.president.data 
        start_date = form1.start_date.data
        end_date = form1.end_date.data
        kind = form1.kind.data
        height_case_1 = "300"
        width_case_1 = "750"

        print(president)
        print(start_date)
        print(end_date)
        print(type(start_date))
        x = str(start_date)
        print(x)
        chart = plot_case_1(presidents_dict[president] , start_date , end_date , kind)

    
    return render_template(
        'query.html',
        form1 = form1,
        src_case_1 = chart,
        height_case_1 = height_case_1 ,
        width_case_1 = width_case_1 
    )

@app.route('/covid19' , methods = ['GET' , 'POST'])
def covid19():

    print("Covid19")

    form1 = Covid19DayRatio(start_date = pd.Timestamp('2020-03-08'))
    chart_confirmed = '/static/imgs/covid19-world.png'
    chart_deaths = '/static/imgs/covid19-world.png'
    chart_recovered = '/static/imgs/covid19-world.png'
    height_case_1 = "100"
    width_case_1 = "250"

    df_confirmed = pd.read_csv(path.join(path.dirname(_file_), 'static/data/time_series_covid19_confirmed_global.csv'))
    df_deaths = pd.read_csv(path.join(path.dirname(_file_), 'static/data/time_series_covid19_deaths_global.csv'))
    df_recovered = pd.read_csv(path.join(path.dirname(_file_), 'static/data/time_series_covid19_recovered_global.csv'))

    country_choices = get_countries_choices(df_confirmed)
    form1.countries.choices = country_choices       # Taken from: https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
   
    

    if request.method == 'POST':
        countries = form1.countries.data 
        start_date = form1.start_date.data
        end_date = form1.end_date.data
        rolling_window = form1.rolling_window.data
        
        df_tmp = covid19_day_ratio(df_confirmed , countries , start_date , end_date , rolling_window)
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.4)
        ax = fig.add_subplot(111)
        ax.set_ylim(0 , 3)
        df_tmp.plot(ax = ax , kind = 'line', figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_confirmed = plot_to_img(fig)

        df_tmp = covid19_day_ratio(df_deaths , countries , start_date , end_date , rolling_window)
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.4)
        ax = fig.add_subplot(111)
        ax.set_ylim(0 , 3)
        df_tmp.plot(ax = ax , kind = 'bar' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_deaths = plot_to_img(fig)

        df_tmp = covid19_day_ratio(df_recovered , countries , start_date , end_date , rolling_window)
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.4)
        ax = fig.add_subplot(111)
        ax.set_ylim(0 , 3)
        df_tmp.plot(ax = ax , kind = 'line' , figsize = (32, 14) , fontsize = 22 , grid = True)
        chart_recovered = plot_to_img(fig)

    
    return render_template(
        'covid19.html',
        img_under_construction = '/static/imgs/under_construction.png',
        form1 = form1,
        chart_confirmed = chart_confirmed,
        chart_deaths = chart_deaths,
        chart_recovered = chart_recovered
        
    )

@app.route('/olympic-medals' , methods = ['GET' , 'POST'])
def olympic_medals():

    print("Olympic Medals")

    form1 = OlympicMedals()
    chart = '/static/imgs/olympic.png'

   
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/olimpic-medal.csv'))
    country_choices = list(set(df['Country']))
    clean_country_choices = [x for x in country_choices if x == x]
    m = list(zip(clean_country_choices , clean_country_choices))
    form1.country.choices = m 


    if request.method == 'POST':
        country = form1.country.data
        df1 = df.loc[df['Country'] == country]
        s = df1.groupby('Discipline').size().sort_values(ascending=False)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        s.plot(ax = ax , kind = 'bar', figsize = (24, 8) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

    
    return render_template(
        'olympic.html',
        img_under_construction = '/static/imgs/under_construction.png',
        form1 = form1,
        chart = chart
    )

@app.route('/yomlayla' , methods = ['GET' , 'POST'])
def yomlayla():

    print("Yom Layla")

    form1 = YomLayla()
    chart = ''

   
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/accdatwebsite.csv'))


    if request.method == 'POST':
        yl = int(form1.yl.data)


        df = df[['HODESH_TEUNA','YOM_LAYLA','SUG_TEUNA']]
        df = df.loc[(df['YOM_LAYLA'] == yl)]
        new_df = pd.DataFrame()
        hodesh_list = list(set(df['HODESH_TEUNA']))
        new_df['HODESH'] = hodesh_list
        sug_list = list(set(df['SUG_TEUNA']))
        for sug in sug_list:
            df_tmp = df.loc[(df['SUG_TEUNA'] == sug)]
            s = df_tmp.groupby('HODESH_TEUNA').size()
            for i in range(1,13):
                if not i in s.index:
                    s[i] = 0
            s = s.sort_index()
            l = list(s)
            new_df[str(sug)] = l
        new_df = new_df.set_index('HODESH')
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        new_df.plot(ax = ax , kind='bar',stacked=True)
        chart = plot_to_img(fig1)

    
    return render_template(
        'yomlayla.html',
        img_under_construction = '/static/imgs/under_construction.png',
        form1 = form1,
        chart = chart
    )

@app.route('/forms_demo' , methods = ['GET' , 'POST'])
def forms_demo():

    print("Forms Demo")

    form1 = AllOfTheAboveForm()
    

    if request.method == 'POST':
        s1 = form1.string_field_entry.data
        s2 = form1.text_area_field_entry.data
        s3 = form1.password_field_entry.data
        s4 = form1.date_field_entry.data
        s5 = form1.integer_field_entry.data
        s6 = form1.decimal_field_entry.data
        s7 = form1.boolean_field_entry.data
        s8 = form1.radio_field_entry.data
        s9 = form1.select_field_entry.data
        s10 = form1.select_field_multiple_entry.data

        t1 = str(type(s1))
        t2 = str(type(s2))
        t3 = str(type(s3))
        t4 = str(type(s4))
        t5 = str(type(s5))
        t6 = str(type(s6))
        t7 = str(type(s7))
        t8 = str(type(s8))
        t9 = str(type(s9))
        t10 = str(type(s10))
        
    else:
        s1 = 'GET Request'
        s2 = 'GET Request'
        s3 = 'GET Request'
        s4 = 'GET Request'
        s4 = 'GET Request'
        s5 = 'GET Request'
        s6 = 'GET Request'
        s7 = 'GET Request'
        s8 = 'GET Request'
        s9 = 'GET Request'
        s10 = 'GET Request'

        t1 = ''
        t2 = ''
        t3 = ''
        t4 = ''
        t5 = ''
        t6 = ''
        t7 = ''
        t8 = ''
        t9 = ''
        t10 = ''
      
        

    
    return render_template(
        'forms_demo.html',
        form1 = form1,
        
        s1 = s1 ,
        s2 = s2 ,
        s3 = s3 ,
        s4 = s4 ,
        s5 = s5 , 
        s6 = s6 ,
        s7 = s7 ,
        s8 = s8 , 
        s9 = s9 ,
        s10 = s10 , 

        t1 = t1 ,
        t2 = t2 ,
        t3 = t3 ,
        t4 = t4 ,
        t5 = t5 ,
        t6 = t6 ,
        t7 = t7 ,
        t8 = t8 ,
        t9 = t9 ,
        t10 = t10
    )

@app.route('/plot_demo' , methods = ['GET' , 'POST'])
def plot_demo():

    print("Plot Demo")

    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/time_series_covid19_confirmed_global.csv'))
    df = df.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby('Country').sum()
    df = df.loc[['Israel' , 'France' , 'Italy' , 'Spain' , 'United Kingdom']]
    df = df.transpose()
    df = df.reset_index()
    df = df.drop(['index'], 1)
    df = df.tail(30)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(ax = ax , kind = 'line')
    chart = plot_to_img(fig)
    
    return render_template(
        'plot_demo.html',
        img_under_construction = '/static/imgs/under_construction.png',
        chart = chart ,
        height = "300" ,
        width = "750"
    )

@app.route('/project_resources')
def project_resources():

    print("Project Resources")

    """Renders the about page."""
    return render_template(
        'project_resources.html'
    )

@app.route('/hebrew_text')
def hebrew_text():
    """Renders the about page."""
    return render_template(
        'hebrew_text.html'
    )

@app.route('/data/trump' , methods = ['GET' , 'POST'])
def trump():

    print("Trump")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    # df = pd.read_csv(path.join(path.dirname(_file_), 'static\\data\\trump.csv'))
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/trump.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'trump.html',
        title='Trump',
        year=datetime.now().year,
        message='Trump dataset page.',
        img_trump = '/static/imgs/trump.jpg',
        img_obama = '/static/imgs/trump.jpg',
        img_bush = '/static/imgs/trump.jpg',
        img_clinton = '/static/imgs/trump.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/obama' , methods = ['GET' , 'POST'])
def obama():

    print("Obama")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    # df = pd.read_csv(path.join(path.dirname(_file_), 'static\\data\\trump.csv'))
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/obama.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'obama.html',
        title='Obama',
        year=datetime.now().year,
        message='Obama dataset page.',
        img_trump = '/static/imgs/obama.jpg',
        img_obama = '/static/imgs/obama.jpg',
        img_bush = '/static/imgs/obama.jpg',
        img_clinton = '/static/imgs/obama.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/bush' , methods = ['GET' , 'POST'])
def bush():

    print("Bush")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    # df = pd.read_csv(path.join(path.dirname(_file_), 'static\\data\\trump.csv'))
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/bush.csv'), encoding = "utf-8")
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'bush.html',
        title='Bush',
        year=datetime.now().year,
        message='Bush dataset page.',
        img_trump = '/static/imgs/bush.jpg',
        img_obama = '/static/imgs/bush.jpg',
        img_bush = '/static/imgs/bush.jpg',
        img_clinton = '/static/imgs/bush.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/clinton' , methods = ['GET' , 'POST'])
def clinton():

    print("Clinton")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    # df = pd.read_csv(path.join(path.dirname(_file_), 'static\\data\\trump.csv'))
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/clinton.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'clinton.html',
        title='Clinton',
        year=datetime.now().year,
        message='Clinton dataset page.',
        img_trump = '/static/imgs/clinton.jpg',
        img_obama = '/static/imgs/clinton.jpg',
        img_bush = '/static/imgs/clinton.jpg',
        img_clinton = '/static/imgs/clinton.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/city_scatter' , methods = ['GET' , 'POST'])
def city_scatter():

    
    df = pd.read_csv(path.join(path.dirname(_file_), 'static/data/city_scatter.csv'))
    df = df.set_index('City')
    raw_data_table = df.to_html(classes = 'table table-hover')

    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot('Education', 'Public Transportation', kind='scatter', ax=ax)
    for k, v in df.iterrows():
        ax.annotate(k, v)
    chart = plot_to_img(fig)

    return render_template(
        'city_scatter.html',
        title='Scatter Chart Example',
        year=datetime.now().year,
        message='City Scatter',
        img_under_construction = '/static/imgs/under_construction.png' ,
        raw_data_table = raw_data_table ,
        chart = chart
    )


@app.route('/data/assignment_5130' , methods = ['GET' , 'POST'])
def assignment_5130():

    print("5130")

    return render_template(
        'assignment_5130.html',

    )

@app.route('/status')
def status():

    print("status")

    st = open(path.join(path.dirname(_file_), 'static/data/status.txt') , 'r' , encoding = 'utf-8').read()

    return render_template(
        'status.html'
    )

@app.route('/tracking_changes')
def tracking_changes():

    print("Tracking Changes")

    """Renders the about page."""
    return render_template(
        'tracking_changes.html',
        title='Tracking changes to the site',
        year=datetime.now().year,
        message=''
    )

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        print(form.username.data)
        print(form.password.data)
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('query')

        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login To Data Analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my data model page',
        year=datetime.now().year,
        message='In this page you will be able to see my data sets'
    )


@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\clinton.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        title='This is Data Set Bill Clinton page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets'
    )

@app.route('/DataSet2')
def DataSet2():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\obama.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet2.html',
        title='This is Data Set Barack Obama page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets'
    )

@app.route('/DataSet3')
def DataSet3():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\bush.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet3.html',
        title='This is Data Set George Bush page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets'
    )

@app.route('/DataSet4')
def DataSet4():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\trump.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet4.html',
        title='This is Data Set Donald Trump page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets'
    )

