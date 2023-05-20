# from service.JsonResponse import JsonResponse
# from flask import g

# error_codes = {
#     1401: ["type_mismatch"],
#     1402: ["not_found", "metric_not_found"],
#     1403: ["no_data", "'NoneType' object is not iterable"],
#     1601: ["permission_denied"],
#     1602: ["extension_not_allowed"],
#     1202: ["exist"],
#     1501: ["not_able_to_convert"],
#     1502: ["database_connection_error", "connection_error"],
#     1503: ["transfer_data_error", "data_transfer"],
#     1404: ["token_expired"],
# }

# code_message = {
#     1500: "Internal Sever Error!",
#     1401: "Type Mismatch! Check the parameter and request body,required key pairs and their value format",
#     1601: "Permission Denied",
#     1402: "Not found",
#     1403: "Not Data",
#     1202: "Already Exist",
#     1502: "Database Connection Error",
#     1503: "Error occur while copying data",
#     1602: "File Extension not allowed.Please Check the file extension.",
#     1404: "Invalid Token.",
# }


# def StatusCode(error, message=None, data=None):
#     response = JsonResponse()
#     for i in error_codes:
#         if error in error_codes.get(i):
#             response.set_status(i)
#             response.set_message(
#                 ({True: code_message.get(i), False: message})[message is None]
#             )
#             response.set_data(data)
#             g.response = response.returnResponse()
#             return response.returnResponse()

#     response.set_status(1500)
#     response.set_message(
#         ({True: code_message.get(1500), False: message})[message is None]
#     )
#     response.set_data(data)
#     g.response = response.returnResponse()

#     return g.response


# def Done(data, message=None):
#     response = JsonResponse()
#     response.set_status(200)
#     response.set_data(data)
#     response.set_message(message)
#     g.response = response.returnResponse()

#     return g.response
