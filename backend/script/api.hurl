# Make sure we're online and our root endpoint works
GET http://127.0.0.1:8000/
HTTP 200
[Asserts]
jsonpath "$.message" == "Welcome to Vivliopoleio Kohyli."

# Let's make sure we can get a specific book
GET http://127.0.0.1:8000/books/1001
HTTP 200
[Asserts]
jsonpath "$.isbn" exists
jsonpath "$.title" == "The Hobbit"

# And that we get an error for a book that doesn't exist
GET http://127.0.0.1:8000/books/9999
HTTP 404
[Asserts]
jsonpath "$.detail" == "Book not found."

# Cool, let's get a list of all books (2 expected currently).
GET http://127.0.0.1:8000/books
HTTP 200
[Asserts]
jsonpath "$" count == 2

# Let's now get a list of all the authors available in our store
GET http://127.0.0.1:8000/authors
HTTP 200
[Asserts]
jsonpath "$" count == 2