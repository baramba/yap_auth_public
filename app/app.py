from flask import Response, abort, request
from flask_migrate import Migrate

from app import create_app, db

app = create_app()
migrate = Migrate(app, db)


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")

    # X-Request-ID header must be in request
    if not request_id:
        raise abort(Response(status=400, response="X-Request-ID header must be in request."))

    from opentelemetry import trace

    current_span = trace.get_current_span()
    current_span.set_attribute("http.request_id", request_id)
