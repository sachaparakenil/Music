from flask import request, jsonify
from swaggerConfig import api
from flask_restx import Resource, reqparse
from service.Validatefunction import validateParamsFromCheckList
from service.spotify.GetPopular import GetPopular
from service.spotify.GetSearch import GetSearch
from service.spotify.GetTrack import GetTrack

spotify = api.namespace("spotify", description="Spotify API")


get_popular = reqparse.RequestParser()
get_popular.add_argument("page", type=int, required=False, help="page", location="args")

get_search = reqparse.RequestParser()
get_search.add_argument("query", type=str, required=True, help="Query string", location="args")
get_search.add_argument("type", type=str, required=True, help="Type", location="args")
get_search.add_argument("market", type=str, required=False, help="Market", location="args")


@spotify.route("/popular")
class Popular(Resource):
    # @jwt_required()
    @api.doc(responses={200: "OK"})
    @api.expect(get_popular)
    def get(self):
        request_body = validateParamsFromCheckList(request.args, ["page"])
        output = GetPopular(request_body)
        return jsonify(output)

@spotify.route("/search")
class Search(Resource):
    # @jwt_required()
    @api.doc(responses={200: "OK", 400: "Bad Request"})
    @api.expect(get_search)
    def get(self):
        request_body = validateParamsFromCheckList(request.args, ["query", "type", "market"])
        output = GetSearch(request_body)
        return jsonify(output)

@spotify.route("/track/<string:id>")
class Track(Resource):
    # @jwt_required()
    @api.doc(responses={200: "OK"})
    def get(self, id):
        output = GetTrack(id)
        return jsonify(output)