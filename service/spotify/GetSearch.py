# from models.dbconn import Session
from service.JsonResponse import JsonResponse
from external.spotify.Search import spotifySearch


def GetSearch(req_obj):
    response = JsonResponse()
    try:
        if req_obj.get("query") != None and req_obj.get("type") != None:
            result = spotifySearch(req_obj.get("query"), req_obj.get("type"), req_obj.get("market"))
        else:
            response.set_status(400)
            response.set_message("Bad Request")
            response.set_error("Bad Request")
            return response.returnResponse()

        data = result
        # print(data)
        response.set_data(data)
        response.set_status(200)

        # session.commit()
    except Exception as e:
        response.set_status(500)  # Internal error
        response.set_message("Internal Server Error")
        response.set_error("Error in  fetching a content => " + str(e))
        # logConfig.logError("Error in  fetching a content  => " + str(e))
    finally:
        # session.close()
        return response.returnResponse()