from flask import Flask, g, request
from flask_restx import Api
import time, datetime, os, json, decimal
# from flask_jwt_extended import get_jwt_identity
import threading

# siteroot = os.path.realpath(os.path.dirname(__file__) + "/service/auth/")
# json_url = os.path.join(siteroot, "OAuth.json")
# OAuthJson = json.loads(open(json_url).read())

app = Flask(__name__)

# app.config["JWT_SECRET_KEY"] = "P+APugQ}&?cwwPXA]u+cEcfVnp8i]&"
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
# jwt = JWTManager(app)


# @app.before_request
# def before_request():
#     g.start_time = time.time()
#     g.response = {}


# def myconverter(o):
#     if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
#         return o.__str__()
#     elif isinstance(o, decimal.Decimal):
#         return float(o)


# @app.after_request
# def after_request(res):
#     body = (
#         (request.json if request.json is not None else dict(request.form))
#         if request.method != "GET"
#         else None
#     )
#     userid = None
#     try:
#         userid = get_jwt_identity()
#     except Exception as e:
#         pass

#     newObject = [
#         {
#             "userid": userid,
#             "path": request.path,
#             "method": request.method,
#             "browser": request.user_agent.browser,
#             "browser_version": request.user_agent.version,
#             "os": request.user_agent.platform,
#             "ip_address": request.remote_addr,
#             "params": dict(request.args),
#             "body": body,
#             "status": (g.response).get("status"),
#             "duration": int((time.time() - g.start_time) * 1000),
#         }
#     ]

#     threading.Thread(target=ServerLog, args=(newObject), daemon=True).start()
#     try:
#         if (res.get_data()).decode("utf-8") == "null\n":
#             res.set_data(json.dumps(g.response, default=myconverter))
#         return res
#     except Exception as e:
#         return res


# def ServerLog(logObject):
#     StoreLog().log(logObject)


# app.config.SWAGGER_UI_OAUTH_CLIENT_ID = OAuthJson["google"]["clientId"]
# app.config.SWAGGER_UI_OAUTH_CLIENT_SECRET = OAuthJson["google"]["clientSecret"]
# app.config.SWAGGER_UI_OAUTH_REALM = "-"
# app.config.SWAGGER_UI_OAUTH_APP_NAME = "IndiaConnects"


# authorizations = {
#     "api_key": {"type": "apiKey", "in": "header", "name": "AUTHORIZATION"}
# }

api = Api(
    app,
    version="1.0",
    title="GMusic",
    description="API  DOCUMENTATION",
    # security=["api_key"],
    # authorizations=authorizations,
)
