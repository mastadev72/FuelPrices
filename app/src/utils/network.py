from flask import request


def get_remote_address() -> str:
    """
    Get the ip address for the current request.

    :return: the ip address for the current request (or 127.0.0.1 if none found)
    """
    return request.access_route[-1] or "127.0.0.1"
