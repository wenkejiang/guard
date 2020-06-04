# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/4   
# 修改时间: 11:24 上午   
# IDE: PyCharm
from rest_framework.renderers import JSONRenderer

class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):

        print(data)
        """
        格式{
            'code':xxx,
            'msg':请求成功，
            'data':{返回数据}
        }
        """
        #如果返回的data为字典 中有msg的key 则将内容改为请求成功 code 为0
        # 如果不是字典则将msg 定义为返回成功 code为0
        # 再将完整的res数据传入
        if renderer_context:
            if isinstance(data,dict):
                if renderer_context["response"].status_code < 400:
                    code = data.pop('code', 0)
                    msg = data.pop('msg', '请求成功')
                else:
                    code = data.pop('code', renderer_context["response"].status_code)
                    msg =  data.pop('msg', '请求成功')

            else:
                msg = '返回成功'
                if renderer_context["response"].status_code < 400:
                    code = 0
                else:
                    code = renderer_context["response"].status_code

            response = renderer_context['response']
            response.status_code = 200
            res={
                'code':code,
                'message':msg,
                'data':data
            }
            return super().render(res,accepted_media_type,renderer_context)
        else:
            return  super().render(data,accepted_media_type,renderer_context)