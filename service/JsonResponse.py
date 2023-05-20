from flask import g

class JsonResponse:
    def __init__(self, status=0, error="", message="", data=[]):
        self.__error = error
        self.__message = message
        self.__status = status
        self.__data = data

    def get_error(self):
        return self.__error

    def set_error(self, error):
        self.__error = error

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def returnResponse(self):
        response = {
            "status": self.__status,
            "message": self.__message,
            "error": self.__error,
            "data": self.__data,
        }
        g.response = response
        return response
