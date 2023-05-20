from swaggerConfig import app
from flask import request, jsonify, send_from_directory, Response
from config import Config as SETTING
from flask_pymongo import pymongo
import os
import json
from passlib.hash import sha256_crypt
import secrets
import requests
import routes.route_auth
import routes.route_playlist
import routes.route_spotify

# app = Flask(__name__)
# app.secret_key = SETTING.FLASK_KEY


# Get Data from Database
myclient = pymongo.MongoClient(SETTING.MONGO_LINK)
GMusicDatabase = myclient[SETTING.DATABASE_NAME]
GMusicDatabaseCollection = GMusicDatabase[SETTING.GMUSIC_DATABASE_COLLECTION]
GMusicUsers = GMusicDatabase[SETTING.USERS_DATABASE_COLLECTION]
GMusicUsersData = GMusicDatabase[SETTING.USERS_DATA_COLLECTION]

# Public Routes
@app.route(f'/{SETTING.VERSION}/popular', methods=['GET'])
def index():
    try:
        if "page" in request.args:
            page = int(request.args.get('page'))
            if page > 0:
                GMusicList = GMusicDatabaseCollection.find({}, {'_id': False}).skip(0 if page == 1 else page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
            else:
                raise ValueError
        else:
            GMusicList = GMusicDatabaseCollection.find({}, {'_id': False}).skip(0).limit(SETTING.PAGING)

        # Convert Data into List
        GMusicFetchData = []
        for GMusic in GMusicList:
            GMusicFetchData.append(GMusic)
        response = Response(json.dumps(GMusicFetchData), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        print(e)
        response = Response(json.dumps({"status" : False, "message" : "Error"}), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{SETTING.VERSION}/spotify/<string:spotify_id>', methods=['GET'])
def spotify_id_func(spotify_id):
    try:
        GMusicList = GMusicDatabaseCollection.find({'spotify_id' : spotify_id}, {'_id': False})

        # Send Response
        response = Response(json.dumps(GMusicList[0]), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except IndexError:
        response = Response(json.dumps({"status": False, "message": "Song not available"}), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response





# Authenticate Routes
@app.route(f'/{SETTING.VERSION}/playlist/<string:playlist_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def add_playlist_func(playlist_name):
    if request.method == "GET":
        try:
            if "api" in request.args:
                api_key = request.args.get("api")
                api_check = GMusicUsers.count_documents({"api" : api_key})
                if api_check != 0:
                    # check that playlist is exists or not
                    user_id = GMusicUsers.find({"api" : api_key}, {"_id" : True})[0]['_id']
                    playlist_check = GMusicUsersData.count_documents({"user_id" : user_id, f"playlists.{playlist_name}" : {"$exists" : True}})
                    if playlist_check == 1:
                        # fetch playlist
                        GMusicList = GMusicUsersData.find({"user_id" : user_id}, {"_id" : False, f"playlists.{playlist_name}" : True})
                        GMusicList = GMusicList[0]["playlists"]
                        response = Response(json.dumps(GMusicList), status=200, mimetype='application/json')
                    else:
                        # playlist not exists
                        response = Response(json.dumps({"status": False, "message": "Playlist not exists"}), status=400, mimetype='application/json')
                else:
                    response = Response(json.dumps({"status": False, "message": "Invalid API"}), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(e)
            response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


    elif request.method == "POST":
        try:
            if "api" in request.form:
                api_key = request.form["api"]
                api_check = GMusicUsers.count_documents({"api" : api_key})
                if api_check != 0:
                    # check that playlist is not already exist
                    user_id = GMusicUsers.find({"api" : api_key}, {"_id" : True})[0]['_id']
                    playlist_check = GMusicUsersData.count_documents({"user_id" : user_id, f"playlists.{playlist_name}" : {"$exists" : True}})
                    if playlist_check == 0:
                        # create new playlist
                        GMusicUsersData.update_one({"user_id" : user_id}, {"$set" : {f"playlists.{playlist_name}" : []}})
                        response = Response(json.dumps({"status": False, "message": "Playlist created"}), status=200, mimetype='application/json')
                    else:
                        # playlist already exists
                        response = Response(json.dumps({"status": False, "message": "Playlist already exists"}), status=400, mimetype='application/json')
                else:
                    response = Response(json.dumps({"status": False, "message": "Invalid API"}), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(e)
            response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


    elif request.method == "PUT":
        try:
            if "api" in request.form and "spotify_id" in request.form:
                api_key = request.form["api"]
                spotify_id = request.form["spotify_id"]
                api_check = GMusicUsers.count_documents({"api" : api_key})
                if api_check != 0:
                    # check that playlist is not already exist
                    user_id = GMusicUsers.find({"api" : api_key}, {"_id" : True})[0]['_id']
                    playlist_check = GMusicUsersData.count_documents({"user_id" : user_id, f"playlists.{playlist_name}" : {"$exists" : True}})

                    # edit playlist
                    if playlist_check == 1:
                        # check that spotify is available
                        spotify_check = GMusicDatabaseCollection.count_documents({"spotify_id" : spotify_id})
                        # spotify id is available
                        if spotify_check == 1:
                            GMusicUsersData.update_one({"user_id" : user_id}, {"$push" : {f"playlists.{playlist_name}" : spotify_id}})
                            response = Response(json.dumps({"status": False, "message": "Playlist edited"}), status=200, mimetype='application/json')
                        # spotify id is not valid
                        else:
                            response = Response(json.dumps({"status": False, "message": "Invalid spotify id"}), status=400, mimetype='application/json')


                    # playlist not exists
                    else:
                        response = Response(json.dumps({"status": False, "message": "Playlist already exists"}), status=400, mimetype='application/json')
                else:
                    response = Response(json.dumps({"status": False, "message": "Invalid API"}), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(e)
            response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


    elif request.method == "DELETE":
        try:
            if "api" in request.form:
                api_key = request.form["api"]
                # spotify_id = request.form["spotify_id"]
                api_check = GMusicUsers.count_documents({"api" : api_key})
                if api_check != 0:
                    # check that playlist is not already exist
                    user_id = GMusicUsers.find({"api" : api_key}, {"_id" : True})[0]['_id']
                    playlist_check = GMusicUsersData.count_documents({"user_id" : user_id, f"playlists.{playlist_name}" : {"$exists" : True}})
                    print(playlist_check)

                    # delete playlist
                    if playlist_check == 1:
                        # GMusicUsersData.update_one({"user_id" : user_id}, {"$pull" : {"playlists" : playlist_name}})
                        GMusicUsersData.find_one_and_delete({"user_id" : user_id}, {"playlists" : playlist_name})
                        # # check that spotify id is available
                        # spotify_check = GMusicUsersData.count_documents({"user_id" : user_id, "playlists" : {"$elemMatch" : {playlist_name : spotify_id}}})
                        # print(spotify_check)
                        # # spotify id is available
                        # if spotify_check == 1:
                        #     GMusicUsersData.update_one({"user_id" : user_id}, {"$pull" : {f"playlists.{playlist_name}" : spotify_id}})
                        #     response = Response(json.dumps({"status": False, "message": "Deleted Successfully"}), status=200, mimetype='application/json')
                        # # spotify id is not valid
                        # else:
                        #     response = Response(json.dumps({"status": False, "message": "Invalid spotify id"}), status=400, mimetype='application/json')

                        response = Response(json.dumps({"status": False, "message": "Playlist deleted"}), status=200, mimetype='application/json')

                    # playlist not exists
                    else:
                        response = Response(json.dumps({"status": False, "message": "Playlist already exists"}), status=400, mimetype='application/json')
                else:
                    response = Response(json.dumps({"status": False, "message": "Invalid API"}), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(e)
            response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response




    try:
        # if "api" in request.args:
        #     pass
        # else:
        #     response = Response(json.dumps({"status": False, "message": "Invalid API"}), status=401, mimetype='application/json')
        # GMusicList = GMusicDatabaseCollection.find({'spotify_id' : playlist_name}, {'_id': False})

        # Send Response
        # response = Response(json.dumps("hehe"), status=200, mimetype='application/json')
        # response = Response(json.dumps(GMusicList[0]), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except IndexError:
        response = Response(json.dumps({"status": False, "message": "Song not available"}), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps({"status": False, "message": "Bad Request"}), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps({"status" : False, "message" : "Internal Server Error"}), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response








# @app.route('/addMusic', methods=['POST'])
# def addMusicFunc():
#     if request.method == 'POST' and request.form.get('auth') == SETTING.AUTH:
#         try:
#             if request.form.get('spotify_id') != None:
#                 GMusicCheck = GMusicDatabaseCollection.count_documents({"spotify_id" : request.form.get('spotify_id')})
#                 if GMusicCheck == 0:
#                     newData = {
#                         "spotify_id": request.form.get('spotify_id'),
#                         "album": request.form.get('album'),
#                         "artist": request.form.get('artist').split(','),
#                         "name": request.form.get('name'),
#                         "music": request.form.get('music'),
#                         "poster": request.form.get('poster'),
#                     }
#                     MusicID = GMusicDatabaseCollection.insert_one(newData).inserted_id
#                     response = Response(json.dumps({"status": True, "id": str(MusicID), "message": "New Song has been added"}), status=200, mimetype='application/json')

#                 else:
#                     response = Response(json.dumps({"status": False, "message": "Music already available"}), status=404, mimetype='application/json')
#             else:
#                 response = Response(json.dumps({"status": False, "message": "Invalid Music ID"}), status=500, mimetype='application/json')
#                 response.headers['Access-Control-Allow-Origin'] = '*'
#                 return response
#             newData = {
#                 "spotify_id": request.form.get('spotify_id'),
#                 "album": request.form.get('album'),
#                 "artist": request.form.get('artist').split(','),
#                 # "duration": int(request.form.get('duration')),
#                 # "lyrics": request.form.get('lyrics'),
#                 "name": request.form.get('name'),
#                 "music": request.form.get('music'),
#                 "poster": request.form.get('poster'),
#             }
#             # GMusicDatabaseCollection.update_one({'_id': MusicID}, {'$set': {'music': str(MusicID), 'poster': str(MusicID), 'lyrics':str(MusicID)}})
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             return response
#         except:
#             response = Response(json.dumps({"status": False, "message": "Error while adding data"}), status=500, mimetype='application/json')
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             return response
#     else:
#         response = Response(json.dumps({"status": False, "message": "You are not authenticated"}), status=401, mimetype='application/json')
#         response.headers['Access-Control-Allow-Origin'] = '*'
#         return response


# @app.route('/deleteMusic', methods=['POST'])
# def deleteMusic():
#     if request.method == 'POST' and request.form.get('auth') == SETTING.AUTH:
#         try:
#             print(request.form.get('doc_id'))
#             GMusicDatabaseCollection.delete_one({"music" : request.form.get('doc_id')})
#             response = Response(json.dumps({"status": True, "message": "Music Successfully Deleted"}), status=200, mimetype='application/json')
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             return response
#         except:
#             response = Response(json.dumps({"status": False, "message": "Not able to delete"}), status=500, mimetype='application/json')
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             return response


@app.route('/check', methods=['POST'])
def checkMusic():
    if request.method == 'POST' and request.form.get('auth') == SETTING.AUTH:
        try:
            print(request.form.get('spotify_id'))
            if request.form.get('spotify_id') != None:
                GMusicCheck = GMusicDatabaseCollection.count_documents({"spotify_id" : request.form.get('spotify_id')})
                if GMusicCheck == 0:
                    response = Response(json.dumps({"status": True, "message": "Music Not Available"}), status=404, mimetype='application/json')
                else:
                    response = Response(json.dumps({"status": True, "message": "Music Available"}), status=200, mimetype='application/json')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                response = Response(json.dumps({"status": False, "message": "Invalid Music ID"}), status=500, mimetype='application/json')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        except:
            response = Response(json.dumps({"status": False, "message": "Not able to delete"}), status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response





# API Authentication
def api_unique(api_key):
    api_check = GMusicUsers.count_documents({"api" : api_key})
    if api_check != 0:
        return api_unique(secrets.token_urlsafe(32))
    else:
        return api_key


@app.route(f'/{SETTING.VERSION}/api/login', methods=['POST'])
def login_func():
    try:
        if "email" in request.form and "password" in request.form:
            email_check = GMusicUsers.count_documents({"email" : request.form['email'].lower()})
            if email_check != 0:
                user_api = GMusicUsers.find({"email" : request.form['email'].lower()}, {'_id' : False})[0]
                if sha256_crypt.verify(request.form["password"], user_api["password"]):
                    response = Response(json.dumps({'success' : True, 'data' : {'email' : user_api['email'], 'api' : user_api['api'], "firstName" : user_api["firstName"], "lastName" : user_api["lastName"]}}), status=200, mimetype='application/json')
                else:
                    response = Response(json.dumps({'success' : False, 'message' : 'Wrong password'}), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps({'success' : False, 'message' : 'User not found'}), status=404, mimetype='application/json')
        else:
            response = Response(json.dumps({'success' : False, 'message' : 'Bad Request'}), status=400, mimetype='application/json')
        
        # Send response
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = Response(json.dumps({'success' : False, 'message' : 'Internal Server Error'}), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{SETTING.VERSION}/api/signup', methods=['POST'])
def signup_func():
    try:
        if "email" in request.form and "password" in request.form and "confPassword" in request.form and "fname" in request.form and "lname" in request.form:
            if request.form['password'] == request.form['confPassword']:
                generated_api = api_unique(secrets.token_urlsafe(32))
                email_check = GMusicUsers.count_documents({"email" : request.form['email'].lower()})
                
                if email_check == 0:
                    new_user = {
                            "email" : request.form['email'].lower(),
                            "password" : sha256_crypt.hash(request.form['password']),
                            "firstName" : request.form['fname'],
                            "lastName" : request.form['lname'],
                            "ip" : request.remote_addr,
                            "country" : None,
                            "region" : None,
                            "city" : None,
                            "api" : generated_api,
                            "worker" : 0,
                            "admin" : 0,
                            "superuser" : 0
                        }
                    if SETTING.DEBUG == False:
                            ip_response = requests.get(f"{SETTING.IP_LOOKUP_WEBSITE}{request.environ['HTTP_X_FORWARDED_FOR']}").json()
                            if ip_response['status'] == "success":
                                new_user["ip"] = request.environ['HTTP_X_FORWARDED_FOR']
                                new_user["country"] = ip_response['country']
                                new_user["region"] = ip_response['regionName']
                                new_user["city"] = ip_response['city']

                    if "superuser" in request.form:
                        if request.form['superuser'] == SETTING.SUPER_USER:
                            new_user['admin'] = 1
                            new_user['superuser'] = 1
                            new_user['worker'] = 1
                    elif "admin" in request.form:
                        if request.form['admin'] == SETTING.ADMIN_USER:
                            new_user['admin'] = 1
                            new_user['worker'] = 1
                    elif "worker" in request.form:
                        if request.form['worker'] == SETTING.WORKER_USER:
                            new_user['worker'] = 1

                    user_id = GMusicUsers.insert_one(new_user).inserted_id
                    user_data = {
                        "user_id" : user_id,
                        "playlists" : {},
                        "private_music" : []
                    }
                    GMusicUsersData.insert_one(user_data)
                    response = Response(json.dumps({'success' : True, 'api' : generated_api}), status=201, mimetype='application/json')
                else:
                    response = Response(json.dumps({'success' : False, 'message' : 'User exists'}), status=409, mimetype='application/json')
            else:
                response = Response(json.dumps({'success' : False, 'message' : 'Password not same'}), status=401, mimetype='application/json')
            
            # Send response
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            raise ValueError
    except ValueError:
        response = Response(json.dumps({'success' : False, 'message' : 'Bad Request'}), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps({'success' : False, 'message' : 'Internal Server Error'}), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/x-icon')


if __name__ == "__main__":
    app.run(debug=SETTING.DEBUG)