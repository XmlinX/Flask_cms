from flask import jsonify



class HttpCode(object):
    ok = 200
    auth_error = 401
    params_error = 400
    server_error = 500



def restful_result(code,message,data):
    return jsonify({"code":code,"message":message,"data":data})


def success(message="",data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)

def auth_error(message=""):
    return restful_result(code=HttpCode.auth_error,message=message,data=None)

def params_error(message=""):
    return restful_result(code=HttpCode.params_error,message=message,data=None)


def server_error(message=""):
    return restful_result(code=HttpCode.server_error,message=message or "服务器内部错误",data=None)