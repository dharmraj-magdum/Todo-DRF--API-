from rest_framework import renderers
import json

# this is for jsonizing respose for client with added info
# this convert raw/intermideate ugly response into well formated json


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""
        if "ErrorDetail" in str(data):
            response = json.dumps({"errors": data})
        else:
            response = json.dumps(data)
        return response


class TodoRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ""
        if "ErrorDetail" in str(data):
            response = json.dumps({"errors": data})
        else:
            response = json.dumps(data)
        return response
