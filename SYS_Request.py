import os
import json
import urllib.parse
"""
this class represent the system format request object that we build for the api request
it get the request and the type(flask,fastapi) and built from them request in the system format 
"""
class SYS_Request:
    def __init__(self):
        self.request_headers = None
        self.request_line = None
        self.request_method = None
        self.request_uri = None
        self.args_names = None
        self.request_body = None
        self.request_headers_names = None
        self.files_names = None
        self.query_string = None
        self.request_protocol = None
        self.args = None
        self.request_basename = None
        self.request_cookies = None
        self.remote_addr = None
        self.unique_id = None
        self.files = None
        self.args_get_names = None
        self.request_filename = None
        self.request_cookies_names = None
        self.request_uri_raw = None
        self.args_get = None
        self.reqbody_processor = None


    async def fill(self,request,api_type,files=None):
        if api_type == "flask":
            self.flask_api_request(request)
        if api_type == "fastapi":
            await self.fastapi_api_request(request,files)

    # this function can extract the information from flask api request
    def flask_api_request(self, request):
        print("-------------------REQUEST----------------------")
        print(request)
        print("-------------------REQUEST----------------------")

        self.request_headers = {key.lower(): value for key, value in dict(request.headers).items()}
        if request.method and request.path and request.environ and request.environ.get('SERVER_PROTOCOL'):
            self.request_line = request.method + ' ' + request.path + ' ' + request.environ['SERVER_PROTOCOL']
        self.request_method = request.method
        self.request_uri = request.url
        self.request_body = request.get_data().decode('utf-8')
        if request.headers:
            self.request_headers_names = list(request.headers.keys())
        if request.files:
            self.files_names = list(request.files.keys())
            self.files = request.files.to_dict()
            files = request.files.getlist('file')
            self.request_filename = [file.filename for file in files]

        self.query_string = request.query_string.decode()
        if request.environ:
            self.request_protocol = request.environ.get('SERVER_PROTOCOL')
            self.unique_id = request.environ.get('UNIQUE_ID')
            self.reqbody_processor = request.environ.get('wsgi.input_terminated', '')
        self.request_cookies = {key.lower(): value for key, value in request.cookies.to_dict().items()}
        self.remote_addr = request.remote_addr
        if request.url:
            self.request_basename = os.path.basename(request.url)


        if self.request_method == "POST":
            self.args = urllib.parse.parse_qs(self.request_body)
            self.args_names = list(self.args.keys())
            for key, value in self.args.items():
                if isinstance(value,list):
                    self.args[key] = value[0]
        if self.request_method == "GET":
            self.args_get_names = request.args.to_dict()
            self.args_get = request.args.to_dict()

        if request.cookies:
            self.request_cookies_names = list(request.cookies.keys())
        self.request_uri_raw = request.full_path

        print(self)
    async def fastapi_api_request(self, request,files):
        self.request_headers = {key.lower(): value for key, value in dict(request.headers).items()}
        if request.method and request.url.path and request.scope and request.scope.get('http_version'):
            self.request_line = request.method + ' ' + request.url.path + ' ' + request.scope['http_version']
        self.request_method = request.method
        self.request_uri = request.url._url

        # get the request body as bytes
        body_bytes = await request.body()

        # decode the bytes to a string using utf-8 encoding
        self.request_body = body_bytes.decode('utf-8')

        # # parse the url-encoded string to a dictionary
        # self.REQUEST_BODY = urllib.parse.parse_qs(body_str)
        # if len(self.REQUEST_BODY) == 0:
        #     print(body_str)
        #     print(type(body_str))
        #     self.REQUEST_BODY = body_str
        # else:
        #     for key, value in self.REQUEST_BODY.items():
        #         if isinstance(value,list):
        #             self.REQUEST_BODY[key] = value[0]
        #
        #
        #     # # self.REQUEST_BODY = json.dumps(body_str)
        #     print("poopopopopopopopopopopopopopop")
        #     print(type(self.REQUEST_BODY))
        #     print(self.REQUEST_BODY)
        #     # temp_body_dict = self.REQUEST_BODY
        #     # self.REQUEST_BODY = "{ "
        #     # for key, value in temp_body_dict.items():
        #         # self.REQUEST_BODY += key
        #         # self.REQUEST_BODY += " : "
        #         # if not isinstance(value,list):
        #         #     self.REQUEST_BODY += value
        #         # else:
        #         #     for val in value:
        #         #         self.REQUEST_BODY += val +" "

        if request.headers:
            self.request_headers_names = list(request.headers.keys())
        if files:
            self.files_names = list(files.keys())
        self.query_string = request.query_params.__repr__()
        if request.scope:
            self.request_protocol = request.scope.get('http_version')
            self.unique_id = request.scope.get('client')
            self.reqbody_processor = request.scope.get('type')
        if request.url:
            self.request_basename = os.path.basename(request.url._url)
        self.request_cookies = {key.lower(): value for key, value in request.cookies.items()}
        self.remote_addr = request.client.host
        if self.request_method == "POST":
            self.args = urllib.parse.parse_qs(self.request_body)
            self.args_names = list(self.args.keys())
            for key, value in self.args.items():
                if isinstance(value,list):
                    self.args[key] = value[0]
        if self.request_method == "GET":
            self.args_get_names = list(request.query_params.keys())
            self.args_get = dict(request.query_params)
        if files:
            self.files = files
            self.request_filename = [file.filename for file in files]
        if request.cookies:
            self.request_cookies_names = list(request.cookies.keys())
        self.request_uri_raw = request.url.__repr__()

        print(self)


    # def flask_api_request_dict_backup(self, request):
    #     self.REQUEST_HEADERS = request.get("headers")
    #     if request.get("method") and request.get("path") and request.get("environ") and request.get("environ").get('SERVER_PROTOCOL'):
    #         self.REQUEST_LINE = request.get("method") + ' ' + request.get("path") + ' ' + request.get("environ")['SERVER_PROTOCOL']
    #     self.REQUEST_METHOD = request.get("method")
    #     self.REQUEST_URI = request.get("url")
    #     if request.get("args"):
    #         self.ARGS_NAMES = list(request.get("args").keys())
    #     self.REQUEST_BODY = request.get("data")
    #     if request.get("headers"):
    #         self.REQUEST_HEADERS_NAMES = list(request.get("headers").keys())
    #     if request.get("files"):
    #         self.FILES_NAMES = list(request.get("files").keys())
    #     self.QUERY_STRING = request.get("query_string")
    #     if request.get("environ"):
    #         self.REQUEST_PROTOCOL = request.get("environ").get('SERVER_PROTOCOL')
    #         self.UNIQUE_ID = request.get("environ").get('UNIQUE_ID')
    #         self.REQBODY_PROCESSOR = request.get("environ").get('wsgi.input_terminated', '')
    #     self.ARGS = request.get("args")
    #     if request.get("url"):
    #         self.REQUEST_BASENAME = os.path.basename(request.get("url"))
    #     self.REQUEST_COOKIES = request.get("cookies")
    #     self.REMOTE_ADDR = request.get("remote_addr")
    #     self.FILES = request.get("files")
    #     if self.REQUEST_METHOD == "GET":
    #         self.ARGS_GET_NAMES = request.get("args")
    #     self.REQUEST_FILENAME = request.get("filename")
    #     if request.get("cookies"):
    #         self.REQUEST_COOKIES_NAMES = list(request.get("cookies").keys())
    #     self.REQUEST_URI_RAW = request.get("full_path")
    #     self.ARGS_GET = request.get("args")



    # this function return the value of the match to the write field asked
    def get(self, var_name):
        try:
            return getattr(self, var_name)
        except:
            return None


    def __str__(self):
        return f"request_line: {self.request_line}\n" \
                f"request_headers: {self.request_headers}\n" \
                f"request_method: {self.request_method}\n" \
                f"request_uri: {self.request_uri}\n" \
                f"args_names: {self.args_names}\n" \
                f"request_body: {self.request_body}\n" \
                f"request_headers_names: {self.request_headers_names}\n" \
                f"files_names: {self.files_names}\n" \
                f"query_string: {self.query_string}\n" \
                f"request_protocol: {self.request_protocol}\n" \
                f"args: {self.args}\n" \
                f"request_basename: {self.request_basename}\n" \
                f"request_cookies: {self.request_cookies}\n" \
                f"remote_addr: {self.remote_addr}\n" \
                f"unique_id: {self.unique_id}\n" \
                f"files: {self.files}\n" \
                f"args_get_names: {self.args_get_names}\n" \
                f"request_filename: {self.request_filename}\n" \
                f"request_cookies_names: {self.request_cookies_names}\n" \
                f"request_uri_raw: {self.request_uri_raw}\n" \
                f"args_get: {self.args_get}\n" \
                f"reqbody_processor: {self.reqbody_processor}"



