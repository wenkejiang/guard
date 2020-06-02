# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/2   
# 修改时间: 9:45 上午   
# IDE: PyCharm

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'code':200,
        'data': {
            'token': token,
            'user_id': user.id,
            'username': user.username
        },
        'message':'登录成功'


    }