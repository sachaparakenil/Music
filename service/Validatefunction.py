import os, json, requests, sys
# from service.StatusCode import StatusCode, Done

# Validate Each and every keys in request data.
def validateParams(requestdata, checkdetail):
    for i in requestdata:
        requestdata[i] = requestdata[i] if i in checkdetail else None

    return requestdata


def validateParamsFromCheckList(requestdata, checkdetail):
    output_obj = {}
    for i in checkdetail:
        output_obj[i] = requestdata.get(i)

    return output_obj


def validateParamsFromCheckList1(requestdata, checkdetail):
    output_obj = {}
    for i in checkdetail:
        if isinstance(requestdata.get(i), checkdetail.get(i)):
            output_obj[i] = requestdata.get(i)
        else:
            raise Exception("type_mismatch")

    return output_obj
