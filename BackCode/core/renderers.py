from rest_framework.renderers import JSONRenderer
from datetime import datetime


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response = renderer_context["response"]
        status_code = response.status_code

        success = 200 <= status_code < 300

        formatted = {
            "success": success,
            "code": status_code,
            "data": data if success else None,
            "errors": None if success else data,
            "timestamp": datetime.utcnow().isoformat()
        }

        return super().render(formatted, accepted_media_type, renderer_context)
