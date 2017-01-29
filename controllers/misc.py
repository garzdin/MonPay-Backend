from json import dumps
from falcon import HTTPBadRequest

__all__ = ['FileUploadResource']

class FileUploadResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        data = req._files
        if not 'image' in data:
            raise HTTPBadRequest(description="No image uploaded")
        image = data['image']
        resp.body = dumps({"description": "Image uploaded succeffully"})
