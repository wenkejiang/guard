# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/2   
# 修改时间: 2:55 下午   
# IDE: PyCharm

'''
Response({
'status':0,
'msg':'ok',
'results':[],
'额外返回一些':''
},headers={},status=200,content_type='')

APIResponse(0,'ok',results,status,header,content_type)
'''

from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self,data_status,data_msg,results=None,
                 status=None,headers=None,content_type=None,**kwargs):
        data = {
            'code':data_status,
            'message':data_msg
        }
        if results is not None:
            data['data'] = results

        data.update(**kwargs)

        super().__init__(data=data,status=status,headers=headers,content_type=content_type)