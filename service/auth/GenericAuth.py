import re
from service.JsonResponse import JsonResponse
from requests_oauthlib import OAuth2Session
from flask import jsonify
from flask_jwt_extended import create_access_token
import json
import os
# from service.auth.UserVerify import InsertUser


class GenericAuth:
    def __init__(self):
        siteroot = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(siteroot, "OAuth.json")
        self.OAuthJson = json.loads(open(json_url).read())

    def getAuthURL(self, req_body):
        authType = req_body.get("authType")
        authJson = self.OAuthJson.get(authType)

        oauth = OAuth2Session(
            authJson.get("clientId"),
            redirect_uri=req_body.get("redirect_uri"),
            scope=authJson.get("scope"),
        )
        authorization_base_url = authJson.get("authorize_url")
        authorization_url, state = oauth.authorization_url(
            authorization_base_url, access_type="offline"
        )
        data = {"redirectURI": authorization_url, "state": state}

        response = JsonResponse()
        response.set_status(200)
        response.set_data(data)
        # logConfig.logInfo("Login attempt")
        return response.returnResponse()

    def create_jwt_token(self, username):
        access_token = create_access_token(identity=username)
        return access_token

    def fetchToken(self, req_body):
        authType = req_body.get("authType")
        state = req_body.get("state")
        code = req_body.get("code")
        access_token_obj = req_body.get("access_token_obj")
        authJson = self.OAuthJson.get(authType)

        oauth = OAuth2Session(
            authJson.get("clientId"), redirect_uri=req_body.get("redirect_uri")
        )
        access_token_url = authJson.get("access_token_url")
        if access_token_obj is None:
            token = oauth.fetch_token(
                access_token_url, code=code, client_secret=authJson.get("clientSecret")
            )
            r = oauth.get(authJson.get("userInfo"))
        else:
            oauth = OAuth2Session(
                authJson.get("clientId"),
                redirect_uri=req_body.get("redirect_uri"),
                token=access_token_obj,
            )
            userInfo = authJson.get("userInfo")
            r = oauth.get(userInfo)

        profile_json = json.loads(r.content)
        status = 200
        print(profile_json)
        if profile_json.get("email") is not None:
            if authType == "google":
                create_obj = {
                    "user_name": profile_json.get("name"),
                    "email": profile_json.get("email"),
                    "picture": profile_json.get("picture"),
                    "user_status": "active",
                    "type": "google",
                }
            elif authType == "github":
                create_obj = {
                    "user_name": profile_json.get("first_name")
                    + " "
                    + profile_json.get("last_name"),
                    "email": profile_json.get("email"),
                    "picture": (profile_json["picture"]["data"]).get("url"),
                    "user_status": "active",
                    "type": "facebook",
                }

            # profile_info = InsertUser(create_obj)
            print(create_obj)

            response = JsonResponse()
            response.set_status(status)
            # logConfig.logInfo("Fetching Token")

            response.set_data(
                create_obj
            )

            return response.returnResponse()
        else:
             return None
