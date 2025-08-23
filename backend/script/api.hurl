# Make sure we're online and our root endpoint works
GET http://127.0.0.1:8000/
HTTP 200
[Asserts]
jsonpath "$.message" == "Welcome to Vivliopoleio Kohyli."