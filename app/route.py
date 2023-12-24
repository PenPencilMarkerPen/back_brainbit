from app import app, api, db
from flask_restful import Resource, fields, marshal_with, abort,reqparse
from flask import render_template, redirect, url_for, jsonify
# from flask_sqlalchemy import func
from app.logic import ResponceTest, Registration, Authentication, Download,  DownloadTest, Upload, UploadRelax
from app.model import Data, User, Survey
from app.form import LoginForm
from sqlalchemy import func
import json
import random
from flask_login import current_user, login_user, logout_user
from flask import g
@app.route('/test', methods = [ 'GET'])
def test():
    print(current_user.get_id())
    return render_template("index.html", user_id = current_user.get_id())
@app.route('/profile', methods = [ 'GET'])
def profile():
    print("PROFILE")
    array_data= []
    avg_positive = db.session.query(func.avg(Data.positive)).filter(Data.id_user ==current_user.get_id()).scalar()
    avg_negative = db.session.query(func.avg(Data.negative)).filter(Data.id_user ==current_user.get_id()).scalar()
    item_session = Survey.query.filter_by(id_user=current_user.get_id()).all()
    avg_survey = db.session.query(func.avg(Survey.state)).filter(Survey.id_user == current_user.get_id()).scalar()
    if avg_positive and  avg_negative and item_session and avg_survey:
        avg_positive = int(avg_positive)
        avg_negative= int(avg_negative)
        avg_survey= int(avg_survey)
        for item in item_session:
            data_user_positive = db.session.query(func.avg(Data.positive)).filter(Data.id_survey==item.id).scalar()
            data_user_negative = db.session.query(func.avg(Data.negative)).filter(Data.id_survey==item.id).scalar()
            if data_user_positive and data_user_negative:
                user_info = {
                    'Conc': int(data_user_positive),
                    'Relax': int(data_user_negative),
                    'Static': item.state+1,
                }
                array_data.append(user_info)
    return render_template("profile.html", positive = avg_positive, negative = avg_negative, data_avg = array_data, avg_survey=avg_survey)
@app.route('/', methods = [ 'GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    print(current_user.is_authenticated)
    print(current_user.get_id())
    user_id=0
    if current_user.is_authenticated:
        user_id = current_user.get_id()
    # if current_user.is_authenticated:
    #     json_data = []
    # # for _ in range(1000):
    # #     data_point = {
    # #         "date": str((1500000000+_)),  # Random timestamp between 2017 and 2027
    # #         "positive": str(random.randint(0, 100)),
    # #         "negative": str(random.randint(0, 100)),
    # #     }
    # #     json_data.append(data_point)

    # items = Data.query.filter_by(id_user = 1, id_survey =7).all()
    # for i in items:
    #     data_point ={
    #         "date": i.date,
    #         "positive": i.positive,
    #         "negative": i.negative,
    #     }
    #     json_data.append(data_point)
    # processed_data = []
    # for item in json_data:
    #     date = int(item['date'])
    #     positive = int(item['positive'])
    #     negative = int(item['negative'])
    #     processed_data.append({'x': date, 'y': positive})
    # print(processed_data)
    return render_template('index.html',user=user_id )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index')) 
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
        user = User.query.filter_by(email = str(form.username.data)).first()
        print(user)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        print('Invalid username or password')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



api.add_resource(ResponceTest, '/test')
api.add_resource(Registration, '/registr')
api.add_resource(Authentication, '/auth')
api.add_resource(Download, '/dwn')
api.add_resource(Upload, '/upl')
api.add_resource(UploadRelax, '/uplrelax')
api.add_resource(DownloadTest, '/dwntest')
