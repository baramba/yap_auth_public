from typing import Optional

from flask.wrappers import Response


def ok20x(response: Optional[str] = None, http_code: int = 200, mimetype="application/json"):
    return Response(response, status=http_code, mimetype=mimetype)
