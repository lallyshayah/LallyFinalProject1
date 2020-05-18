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
from LallyFinalProject1.Models.plot_service_functions import plot_to_img
from LallyFinalProject1.Models.plot_service_functions import plot_case_1
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

    form1 = SinglePresidentForm()#פעולה בונה של הטופס
    chart = "https://iclgroupv2.s3.amazonaws.com/corporateil/wp-content/uploads/sites/1005/2017/12/bigstock-United-States-Of-America-Flag-650785.jpg"
    height_case_1 = "100"
    width_case_1 = "250"

    df_trump = pd.read_csv(path.join(path.dirname(__file__), 'static/data/trump.csv'))
    df_obama = pd.read_csv(path.join(path.dirname(__file__), 'static/data/obama.csv'))
    df_bush = pd.read_csv(path.join(path.dirname(__file__), 'static/data/bush.csv'))
    df_clinton = pd.read_csv(path.join(path.dirname(__file__), 'static/data/clinton.csv'))
    #presidents_dict = {'trump' : df_trump , 'obama' : df_obama , 'bush' : df_bush , 'clinton' : df_clinton }

    if request.method == 'POST': #תנאי: רק אם המשתמש לוחץ הצג
        president = form1.president.data #רשימה של הנשיאים שהמשתמש בחר
        t = pd.DataFrame(index = range(0,12)) #ממלא טבלה חדשה שאמלא בהמשך בכל הדגימות של כל חודש של השנה הראשונה של כל נשיא
        dfl = [df_trump , df_obama , df_bush , df_clinton]
        dflnames = ['trump' , 'obama' , 'bush' , 'clinton'] 
        i = 0
        for df in dfl: #לולאת פור שעוברת על כל איבר בתוך הרשימה שנקראת dfl
            df = df[['Start Date' , 'Approving']] # יוצר טבלה חדשה רק עם העמודות Start Date, Approving
            df = df.set_index('Start Date') #הופכת את start date לאינדקס של הדאטהפריים
            df.index = pd.to_datetime(df.index) # הופכת את האינדקס ממשתנה מסוג סטרינג למשתנה מסוג date time
            s = df['Approving'] #   יוצרת סדרה מתוך הדאטהפריים
            s = s.resample('M').mean() # הופכת את הסדרה לפי חודשים - למשל אם יש שלושה תאריכים באותו חודש היא עושה ממוצע 
            s = s[0:12].to_list() # לוקחת את 12 החודשים הראשונים מהסדרה
            t[dflnames[i]] = s # גורם לסדרה להיכנס לתוך טבלה חדשה בעלת 5 עמדוות ו12 שורות אחת לכל חודש
            i = i + 1

        kind = form1.kind.data
        height_case_1 = "600"
        width_case_1 = "1200"

     
        fig = plt.figure()
        ax = fig.add_subplot(111)
        t[president].plot(ax = ax , kind = kind , figsize = (24, 18) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

    
    return render_template(
        'query.html',
        form1 = form1,
        src_case_1 = chart,
        height_case_1 = height_case_1 ,
        width_case_1 = width_case_1 
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

