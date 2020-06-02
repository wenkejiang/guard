# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/1   
# 修改时间: 3:33 下午   
# IDE: PyCharm
import json

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        data = str(response.data)
        response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = data

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.status_code = 200

            response.data['message'] = "Import Error"

        elif response.status_code == 401:
            response.status_code = 200
            response.data['message'] = "Auth failed"


        elif response.status_code >= 500:
            response.status_code = 200
            response.data['message'] =  "Internal service errors"


        elif response.status_code == 403:
            response.status_code = 200
            response.data['message'] = "Access denied"


        elif response.status_code == 405:
            response.status_code = 200
            response.data['message'] = 'Request method error'

    return response

#无需调用，报错的时候他自己会调用！！

