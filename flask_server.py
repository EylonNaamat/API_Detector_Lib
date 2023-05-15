import asyncio
from flask import Flask, request
from API_Detector_Package import API_Detector
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['MAX_CONTENT_LENGTH'] = None
app.config['MAX_CONTENT_PATH'] = None
app.url_map.strict_slashes = False
app.normalization = False
app.config['TRAP_BAD_REQUEST_ERRORS'] = False

api_detector = API_Detector("rules")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    api_request = request
    result = asyncio.run(api_detector.detect_malicious_request(api_request, "flask"))
    return {"answer": result}