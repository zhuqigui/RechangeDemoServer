from rest_framework.renderers import JSONRenderer


class PublicRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            obj = data.get('detail')
        except AttributeError:
            return super().render(data)

        if obj:
            code = obj.code
            msg = str(obj)
            res_data = {
                'errmsg': msg
            }
        else:
            code = data.pop('code',None)
            res_data = data.pop('data',None)

        data = {
            'code': code,
            'data': res_data
        }
        print(data)
        return super().render(data, accepted_media_type=None, renderer_context=None)
