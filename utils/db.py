from utils.exceptions import InvalidDatabaseURL

__all__ = ['construct_url']

def construct_url(provider, username, password, host, name, port=None):
    DEFAULT_PORT = 5432
    if not provider or not username or not password or not host or not name:
        raise InvalidDatabaseURL("Please provide valid arguments")
    return "{provider}://{username}:{password}@{host}:{port}/{name}".format(
        provider=provider,
        username=username,
        password=password,
        host=host,
        port=DEFAULT_PORT if not port else port,
        name=name)
