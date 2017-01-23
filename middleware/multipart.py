from cgi import FieldStorage

class MultipartMiddleware(object):
    def __init__(self, parser=None):
        self.parser = parser or FieldStorage

    def parse(self, stream, environ):
        return self.parser(fp=stream, environ=environ)

    def process_request(self, req, resp, **kwargs):
        if 'multipart/form-data' not in (req.content_type or ''):
            return
        req.env.setdefault('QUERY_STRING', '')
        stream = req.stream.stream if hasattr(req.stream, 'stream') else req.stream
        form = self.parse(stream=stream, environ=req.env)
        for key in form:
            field = form[key]
            if not getattr(field, 'filename', False):
                field = form.getlist(key)
            req._files[key] = field
