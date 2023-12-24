from flask_restful import Resource, fields, marshal_with, abort,reqparse
from flask import make_response, send_file, jsonify,request
from app import db, login
import json
import random
import time
from app.model import User, Survey, Data
from flask_login import current_user, login_user, logout_user
import re
print("hello")
task_post_args = reqparse.RequestParser()
task_post_args.add_argument("text_question",type=str,help="Task is text_question", required= True )

def remove_special_characters(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string)

class ResponceTest(Resource):
    def post(self):
        print("hello")
        args = task_post_args.parse_args()
        print(args['text_question'])
        return 200
    
    def get(self):  
        count = 0
        data = []   
        while count < 100000:
            current_time = str(int(time.time())) 
            count += 1

            positive_count = random.randint(1, 100)
            negative_count = 100 - positive_count
            
            data.append({
                "date": current_time,
                "positive": str(positive_count),
                "negative": str(negative_count)
            })
        with open('data.json', 'w') as file:  
            json.dump(data, file)

        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)

registr_post = reqparse.RequestParser()
registr_post.add_argument("name", type=str, help="Task is email", required = True)
registr_post.add_argument("password", type=str, help="Task is email", required = True)

class Registration(Resource):
    def post(self):
        args = registr_post.parse_args()
        count = User.query.filter_by(email=args["name"]).count()
        if args["name"] and args['password'] and count==0:
            item = User(email = remove_special_characters(args['name']).lower(), password_hash = remove_special_characters(args['password']).lower())
            db.session.add(item)
            db.session.commit()
            return jsonify({"registr" : "true"})
        return  jsonify({"registr" : "false"})

class Authentication(Resource):
    def post(self):
        args = registr_post.parse_args()
        item = User.query.filter_by(email=remove_special_characters(args['name']).lower(), password_hash = remove_special_characters(args['password']).lower()).first()
        print(item)
        if item: 
            return jsonify({"auth" : "true"})
        return jsonify({"auth" : "false"})

class Download(Resource):
    def post(self):
        files = request.get_json()
        # print(files)
        survey = files.get('survey')
        user = files.get('email')
        statistic = files.get('statistic')
        if user and survey and statistic:
            item_survey = Survey(state=survey)
            db.session.add(item_survey)
            db.session.commit()
            print(user)
            item_id = User.query.filter_by(email = user).first().id
            print(item_id)
            for i in statistic:
                item_static = Data(id_user =item_id,  id_survey = int(len(Survey.query.all())), positive =i['positive'], 
                negative = i['negative'], date = i['date'] )
                db.session.add(item_static)
                db.session.commit()
            print(survey)
            print(statistic)
        return {'message': 'Received the data successfully'}, 200

class Upload(Resource):
    def get(self):
        print("Uploda")
        user_id = -1
        user_id = request.args.get('user_id')
        print(user_id)
        json_data = []
        # items = Data.query.filter_by(id_user = 2, id_survey =  int(int(Survey.query.order_by(Survey.id.desc()).first().id))).all()
        print(current_user.is_authenticated)
        print(current_user.get_id())
        items = []
        if user_id != -1: 
            # items = Data.query.filter_by(id_user = current_user.get_id(), id_survey = None).all()
            items = Data.query.filter_by(id_user = user_id, id_survey = None).all()
        if len(items) >0:
            for i in items:
                data_point ={
                    "date": i.date,
                    "positive": i.positive,
                    "negative": i.negative,
                }
                json_data.append(data_point)
        else:
            # survey_id = Survey.query.filter_by(id_user=current_user.get_id()).order_by(Survey.id.desc()).first().id
            survey_id = Survey.query.filter_by(id_user=user_id).order_by(Survey.id.desc()).first().id
            print(survey_id)
            # items = Data.query.filter_by(id_user = current_user.get_id(), id_survey = survey_id).all()
            items = Data.query.filter_by(id_user = user_id, id_survey = survey_id).all()
            for i in items:
                data_point ={
                    "date": i.date,
                    "positive": i.positive,
                    "negative": i.negative,
                }
                json_data.append(data_point)
        processed_data = []
        for item in json_data:
            date = int(item['date'])
            positive = int(item['positive'])
            negative = int(item['negative'])
            processed_data.append({'x': date, 'y': positive})
        return jsonify(processed_data)



class UploadRelax(Resource):
    def get(self):
        print("Uploda")
        json_data = []
        user_id = -1
        user_id = request.args.get('user_id')

        # items = Data.query.filter_by(id_user = 2, id_survey =  int(int(Survey.query.order_by(Survey.id.desc()).first().id))).all()
        print(current_user.is_authenticated)
        print(current_user.get_id())
        items = []

        if user_id != -1: 
            items = Data.query.filter_by(id_user = user_id, id_survey = None).all()
            # items = Data.query.filter_by(id_user = current_user.get_id(), id_survey = None).all()
        if len(items) >0:
            for i in items:
                data_point ={
                    "date": i.date,
                    "positive": i.positive,
                    "negative": i.negative,
                }
                json_data.append(data_point)
        else:
            # survey_id = Survey.query.filter_by(id_user=current_user.get_id()).order_by(Survey.id.desc()).first().id
            survey_id = Survey.query.filter_by(id_user=user_id).order_by(Survey.id.desc()).first().id
            print(survey_id)
            # items = Data.query.filter_by(id_user = current_user.get_id(), id_survey = survey_id).all()
            items = Data.query.filter_by(id_user =user_id, id_survey = survey_id).all()
            for i in items:
                data_point ={
                    "date": i.date,
                    "positive": i.positive,
                    "negative": i.negative,
                }
                json_data.append(data_point)
        processed_data = []
        for item in json_data:
            date = int(item['date'])
            positive = int(item['positive'])
            negative = int(item['negative'])
            processed_data.append({'x': date, 'y': negative})
        return jsonify(processed_data)



# class DownloadTest(Resource):
#     def post(self):
#         files = request.get_json()
#         print("hello")
#         state = files.get('survey')
#         user = files.get('email')
#         print(user)
#         statistic = files.get('data')
#         print(user)
#         print(statistic)
#         if files.get('condition') == "start" and user and statistic:
#             item_id = User.query.filter_by(email = user).first().id
#             item = Survey(id_user=item_id, state=state)
#             db.session.add(item)
#             db.session.commit()
#             for i in statistic:
#                 print(item_id)
#                 item_static = Data(id_user =item_id,  id_survey = int(int(Survey.query.order_by(Survey.id.desc()).first().id)), positive =i['positive'], 
#                 negative = i['negative'], date = i['date'] )
#                 db.session.add(item_static)
#                 db.session.commit()
#         elif files.get('condition') == "end" and user and statistic:
#             for i in statistic:
#                 item_id = User.query.filter_by(email = user).first().id
#                 item_static = Data(id_user =item_id,  id_survey = int(int(Survey.query.order_by(Survey.id.desc()).first().id)), positive =i['positive'], 
#                 negative = i['negative'], date = i['date'] )
#                 db.session.add(item_static)
#                 db.session.commit()
#             item = Survey(id_user=item_id, state=state)
#             db.session.add(item)
#             db.session.commit()



class DownloadTest(Resource):
    def post(self):
        files = request.get_json()
        state = files.get('survey')
        # user = files.get('email')
        user = remove_special_characters(files.get('email')).lower()
        statistic = files.get('data')

        if files.get('condition') == "start" and user and statistic:
            item_id = User.query.filter_by(email=user).first().id
            for i in statistic:
                item_static = Data(
                    id_user=item_id,
                    id_survey=None, 
                    positive=i['positive'],
                    negative=i['negative'],
                    date=i['date']
                )
                db.session.add(item_static)
            db.session.commit()

        elif files.get('condition') == "end" and user and statistic:
            item_id = User.query.filter_by(email=user).first().id

            survey = Survey(id_user=item_id, state=state)
            db.session.add(survey)
            db.session.commit()

            survey_id = survey.id

            previous_data = Data.query.filter_by(id_user=item_id, id_survey=None).all()
            for prev_data in previous_data:
                prev_data.id_survey = survey_id

            for i in statistic:
                item_static = Data(
                    id_user=item_id,
                    id_survey=survey_id,
                    positive=i['positive'],
                    negative=i['negative'],
                    date=i['date']
                )
                db.session.add(item_static)
            db.session.commit()
