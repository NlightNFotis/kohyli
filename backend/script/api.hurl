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

# And let's try to find an individual author by id
GET http://127.0.0.1:8000/authors/1
HTTP 200
[Asserts]
jsonpath "$.first_name" == "J.R.R."
jsonpath "$.last_name" == "Tolkien"

# And let's try to find an author that doesn't exist
GET http://127.0.0.1:8000/authors/9999
HTTP 404
[Asserts]
jsonpath "$.detail" == "Author not found."

# Now let's retrieve a book by a known author
GET http://127.0.0.1:8000/authors/1/books
HTTP 200
[Asserts]
jsonpath "$" count == 1
jsonpath "$.[0].title" == "The Hobbit"

# Let's try signing up a new user
POST http://127.0.0.1:8000/users/signup
{
    "first_name": "Fotis",
    "last_name": "Koutoulakis",
    "email": "fotis.koutoulakis@gmail.com",
    "password": "fotis is great!"
}
HTTP 200
[Asserts]
jsonpath "$.first_name" == "Fotis"

# And now login using our user
POST http://127.0.0.1:8000/users/login
Content-Type: application/x-www-form-urlencoded
[Form]
username: fotis.koutoulakis@gmail.com
password: fotis is great!
HTTP 200
