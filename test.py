from API_Detector import API_Detector


waf = API_Detector("rules")
request_bad = {
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/api/v1/files?path=../../../etc/passwd',
    'ARGS': {'path': '../../../etc/passwd'},
    'REQUEST_HEADERS': {'Host': 'example.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer abc123', 'Connection': 'keep-alive', 'Cookie': 'sessionid=abc123'},
    '!REQUEST_HEADERS:Referer': None,
    'FILES': None,
    'XML:/*': None
}

request_bad2 = {
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/api/v1/files',
    'ARGS': None,
    'REQUEST_HEADERS': {
        'Host': 'example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer abc123',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=abc123',
        'Referer': 'https://example.com/dashboard',
        'file-path': '../../../../etc/passwd'
    },
    '!REQUEST_HEADERS:Referer': None,
    'FILES': None,
    'XML:/*': None,
    'data': None
}

request_good = {
    'REQUEST_METHOD': 'POST',
    'REQUEST_URI': '/api/v1/users',
    'ARGS': None,
    'REQUEST_HEADERS': {
        'Host': 'example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Content-Length': '76',
        'Authorization': 'Bearer abc123',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=abc123'
    },
    '!REQUEST_HEADERS:Referer': 'https://example.com/register',
    'FILES': None,
    'XML:/*': None,
    'data': {
        'username': 'johndoe',
        'password': 'mypassword',
        'email': 'johndoe@example.com'
    }
}

request_bad_sql = {
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/api/v1/products',
    'ARGS': {
        'id': '1 OR 1=1'
    },
    'REQUEST_HEADERS': {
        'Host': 'example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer abc123',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=abc123',
        'Referer': 'https://example.com/products'
    },
    '!REQUEST_HEADERS:Referer': None,
    'FILES': None,
    'XML:/*': None,
    'data': None
}

request_bad_protocol_enforcement = {
    'REQUEST_METHOD': 'POST',
    'REQUEST_URI': '/api/v1/users',
    'ARGS': None,
    'REQUEST_HEADERS': {
        'Host': 'example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'Referer': 'https://example.com/register',
        'Content-Type': 'application/json'
    },
    '!REQUEST_HEADERS:Referer': 'https://example.com/register',
    'FILES': None,
    'XML:/*': None,
    'data': '{"username": "admin", "password": "password", "email": "admin@example.com"}'
}

flask_request_bad_sql = {
    'method': 'GET',
    'url': 'http://localhost:5000/api/v1/products?id=1%20OR%201=1',
    'path': '/api/v1/products',
    'headers': {
        'Host': 'localhost:5000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer abc123',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=abc123',
        'Referer': 'http://localhost:5000/products'
    },
    'data': None,
    'form': None,
    'files': None,
    'args': {
        'id': '1 OR 1=1'
    },
    'json': None,
    'cookies': {
        'sessionid': 'abc123'
    },
    'is_json': False,
    'environ': {
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '5000',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/api/v1/products',
        'QUERY_STRING': 'id=1%20OR%201=1',
        'CONTENT_TYPE': '',
        'CONTENT_LENGTH': '',
        'HTTP_HOST': 'localhost:5000',
        'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'HTTP_ACCEPT': 'application/json',
        'HTTP_AUTHORIZATION': 'Bearer abc123',
        'HTTP_CONNECTION': 'keep-alive',
        'HTTP_COOKIE': 'sessionid=abc123',
        'HTTP_REFERER': 'http://localhost:5000/products',
    }
}


flask_req_all_features = {
    'method': 'GET',
    'url': 'http://localhost:5000/api/v1/products?id=1%20OR%201=1',
    'path': '/api/posts/123',
    'environ': {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.input_terminated': '',
        'UNIQUE_ID': 'abcd1234-5678-9012-3456-7890abcdef'
        # add any other environ keys you need
    },
    'args': {
        'sort': 'desc'
    },
    'data': 'eylon michael',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer some_access_token'
    },
    'files': {},
    'query_string': 'sort=desc',
    'cookies': {
        'session_id': 'abcd1234'
    },
    'remote_addr': '192.168.1.2'
}

print(waf.detect_malicious_request(flask_req_all_features))
print(waf.detect_malicious_request(flask_request_bad_sql))
