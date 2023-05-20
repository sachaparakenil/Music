# from models.dbconn import Session
from service.JsonResponse import JsonResponse

def GetPopular(req_obj):
    response = JsonResponse()
    # session = Session()
    try:
        # res_obj = (
        #     session.query(
        #         GrographicalData.taluka,
        #     )
        #     .filter(
        #         GrographicalData.state == state,
        #         GrographicalData.district == district,
        #     )
        #     .distinct()
        # )
        data = [
            "popular songs"
        ]
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