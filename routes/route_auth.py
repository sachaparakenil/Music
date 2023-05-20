from flask import request, jsonify
from flask_restx import Resource, fields
from service.auth.GenericAuth import GenericAuth
from service.Validatefunction import validateParamsFromCheckList
from swaggerConfig import api
from dataclasses import asdict


auth = api.namespace("auth", description="OAuth authentication Apis")

autherization_model = api.model(
    "Get autherization url",
    {
        "authType": fields.String(
            discriminator=True,
            required=True,
            description="Auth type mean type of authentication like google,github,facebook or linkedin",
            help="type is google,github,facebook or linkedin",
        ),
        "redirect_uri": fields.String(
            discriminator=True,
            required=True,
            description="Redirect uri",
            help="for local server is http://localhost:3000/get-response for online replace localhost:3000 with app.ask-data.com",
        ),
    },
)

fetchtoken_model = api.model(
    "Just verifing the given token",
    {
        "authType": fields.String(
            discriminator=True,
            required=True,
            description="Auth type mean type of authentication like google,github,facebook or linkedin",
            help="type is google,github,facebook or linkedin",
        ),
        "redirect_uri": fields.String(
            discriminator=True,
            required=True,
            description="Redirect uri",
            help="for local server is http://localhost:3000/get-response for online replace localhost:3000 with app.ask-data.com",
        ),
        "state": fields.String(
            discriminator=True,
            required=True,
            description="This state which you get after login",
            help="Copy the state from the url which you get after the login",
        ),
        "code": fields.String(
            discriminator=True,
            required=True,
            description="This code you get after the login",
            help="Copy the code from url which you get after the login",
        ),
    },
)


@auth.route("/authizationURL")
class authizationURL(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(autherization_model)
    def post(self):
        request_body = validateParamsFromCheckList(
            request.json, ["authType", "redirect_uri"]
        )
        output = GenericAuth().getAuthURL(request_body)
        return jsonify(output)


@auth.route("/fetchToken")
class fetchToken(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(fetchtoken_model)
    def post(self):
        request_body = validateParamsFromCheckList(
            request.json,
            ["authType", "state", "code", "access_token_obj", "redirect_uri"],
        )
        output = GenericAuth().fetchToken(request_body)
        return jsonify(output)

@auth.route("/get-response")
class getResponse(Resource):
    @api.doc(responses={200: "OK"})
    def get(self):
        print(request.args)
        output = request.args
        return jsonify(output)
