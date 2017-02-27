import uuid
from json import dumps
from falcon import HTTPBadRequest

__all__ = ['FileUploadResource']

class FileUploadResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        stream = req.stream.stream if hasattr(req.stream, 'stream') else req.stream
        filename = uuid.uuid4()
        with open("{name}.jpg".format(name=filename), 'wb+') as f:
            while True:
                f.write(stream.read(1024))
        resp.body = dumps({"status": True})
