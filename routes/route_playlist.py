from flask import request, jsonify
from swaggerConfig import api
from flask_restx import Resource, reqparse
from service.playlist.GetPlaylist import GetPlaylist

playlist = api.namespace("playlist", description="Playlist API")

@playlist.route("/<string:playlist_id>")
class Playlist(Resource):
    # @jwt_required()
    @api.doc(responses={200: "OK"})
    # @api.expect(get_service)
    def get(self, playlist_id):
        # request_body = validateParamsFromCheckList(request.args, ["page"])
        output = GetPlaylist(playlist_id)
        return jsonify(output)

    # @jwt_required()
    @api.doc(responses={200: "OK"})
    # @api.expect(get_service)
    def post(self, playlist_id):
        # request_body = validateParamsFromCheckList(request.args, ["page"])
        output = GetPlaylist(playlist_id)
        return jsonify(output)