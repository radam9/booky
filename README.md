# Bookmarkie

Bookmarkie is a web application created for the `Udacity - Full Stack Web Developer Nanodegree` Capsone project.

---

## Motivation

This application is a first step towards a fully functional web-based bookmarks manager. The application demonstrates a proficiency in the following areas:

1. Data modeling
   - Architect relational database models in Python
   - Utilize SQLAlchemy to conduct database queries
2. API Architecture and Testing
   - Follow RESTful principles of API development using Flask
   - Structure endpoints to perform CRUD operations, as well as error handling
   - Demonstrate validity of API behavior using the unittest library
3. Third Party Authentication
   - Configure Role Based Authentication and roles-based access control (RBAC) in a Flask application utilizing Auth0
   - Decode and verify JWTs from Authorization headers
4. Deployment
   - API is hosted live via Heroku @ [Bookmarkie](https://bookmarkie.herokuapp.com/)

---

## Dependencies

The application is dependent on:

- Python 3.7

and the following tech stacks:

- [Flask](https://flask.palletsprojects.com/en/master/), and its extensions:
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/master/)
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
  - [Flask-Script](https://flask-script.readthedocs.io/en/latest/)
  - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
- [Jose](https://python-jose.readthedocs.io/en/latest/)

---

## Setup

### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/index.html).

### Virtual Enviornment

General information on how to set up a virtual envirinment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

```
python -m venv venv
venv\scripts\activate
```

### Install Dependencies

Once you have your virtual environment setup and running, install the dependencies:

```
pip install -r requirements.txt
```

### Database Setup

To setup the database run the `initialize_db.py` script using the following command:

```
python initialize_db.py
```

This will drop the old database if it exists, and will create a new database instance then populate it with initial data.

---

## Running the Server

To run the server, ensure you are running the virtual environment and that your terminal is located at the root folder, then run the following command:

```
flask run
```

this will load all the environmental variables from `.flaskenv` file and start the server on [http://localhost:5000](http://localhost:5000).

---

## Testing

To run the `unittest` suite, ensure you are running the virtual environment and that your terminal is located at the root folder, then run the following command:

```
python -m unittest test
```

this will run 30 tests that check every route for success and failure cases, it will also check for permissions for the Admin & User roles on every route.

---

## Using the application

To use the application locally or on heroku you will need to provide the authentication token for the role you are using (ADMIN or USER). To export the tokens as envionmental variables run the `setup.sh` bash file. Now you can use the tokens either with `curl` or copy it into `postman`.

| Role  | Environment Variable Name |
| :---- | :-----------------------: |
| Admin |        ADMIN_TOKEN        |
| User  |        USER_TOKEN         |

You can now use the application locally on [localhost:5000](http://localhost:5000) or live on [Bookmarkie-heroku](https://bookmarkie.herokuapp.com/).

Currently the application doesn't have a front-end, so visiting the root url will greet you with the following json message:

```json
{
  "Message": "Welcome to Bookmarkie!, go to [https://github.com/radam9/Bookmarkie] for further instruction on using the API",
  "Success": true
}
```

to use the application you will have to either use `curl` or `Postman`.

---

## API

All endpoints except for the root requires authentication. Below are the permissions allowed for each role.

#### Role permissions (RBAC)

1. Admin
   - view bookmarks & directories
   - create bookmarks & directories
   - modify bookmarks & directories
   - delete bookmarks & directories
2. User
   - view bookmarks & directories

### Error Handling

Errors are returned as JSON in the following format:

```json
{
  "Success": False,
  "Error": 400,
  "Message": "Bad Request"
}
```

The API will return the following types of errors:

- 400 – Bad Eequest
- 401 – Unauthorized
- 404 – Resource Not Found
- 405 – Method Not Allowed
- 422 – Unprocessable Entity

### Enpoints Overview

The following list shows the available endpoints:

1. Root
   - GET `/`
2. Bookmarks
   - GET `/bookmarks`
   - GET `/directories/<int:id>`
   - POST `/bookmarks/create`
   - PATCH `/bookmarks/<int:id>/modify`
   - DETELE `/bookmarks/<int:id>/delete`
3. Directories
   - GET `/directories`
   - POST `/directories/create`
   - PATCH `/directories/<int:id>/modify`
   - DETELE `/directories/<int:id>/delete`

### Endpoint Details

Below you can find a description of every endpoint as well as an example response.

**GET** `/`

- Index page, returns a greeting.
- Body: None
- Permissions: None
- Response:

```json
{
  "Message": "Welcome to Bookmarkie!, go to [https://github.com/radam9/Bookmarkie] for further instruction on using the API",
  "Success": true
}
```

**GET** `/bookmarks`

- Returns all the bookmarks.
- Body: None
- Permissions: `User`, `Admin`
- Response:

```json
{
  "bookmarks": [
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 1,
      "id": 1,
      "title": "Youtube",
      "url": "https://www.youtube.com"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 1,
      "id": 2,
      "title": "Veoh",
      "url": "https://www.veoh.com/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 2,
      "id": 3,
      "title": "Gmail",
      "url": "https://www.google.com/gmail/about/#"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 2,
      "id": 4,
      "title": "Outlook",
      "url": "https://outlook.live.com/owa/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 3,
      "id": 5,
      "title": "Unsplash",
      "url": "https://unsplash.com/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 3,
      "id": 6,
      "title": "ArtStation",
      "url": "https://www.artstation.com/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 4,
      "id": 7,
      "title": "Python",
      "url": "https://www.python.org/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 4,
      "id": 8,
      "title": "Udacity",
      "url": "https://www.udacity.com/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 5,
      "id": 9,
      "title": "Wikipedia",
      "url": "https://www.wikipedia.org/"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 5,
      "id": 10,
      "title": "Encyclopedia",
      "url": "https://www.encyclopedia.com/"
    }
  ]
}
```

**GET** `/directories`

- Returns all directories.
- Body: None
- Permissions: `User`, `Admin`
- Response:

```json
{
  "directories": [
    {
      "id": 1,
      "name": "Entertainment",
      "urls": [
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 1,
          "id": 2,
          "title": "Veoh",
          "url": "https://www.veoh.com/"
        },
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 1,
          "id": 1,
          "title": "Youtube",
          "url": "https://www.youtube.com"
        }
      ]
    },
    {
      "id": 2,
      "name": "Email",
      "urls": [
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 2,
          "id": 3,
          "title": "Gmail",
          "url": "https://www.google.com/gmail/about/#"
        },
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 2,
          "id": 4,
          "title": "Outlook",
          "url": "https://outlook.live.com/owa/"
        }
      ]
    },
    {
      "id": 3,
      "name": "Images",
      "urls": [
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 3,
          "id": 6,
          "title": "ArtStation",
          "url": "https://www.artstation.com/"
        },
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 3,
          "id": 5,
          "title": "Unsplash",
          "url": "https://unsplash.com/"
        }
      ]
    },
    {
      "id": 4,
      "name": "Programming",
      "urls": [
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 4,
          "id": 7,
          "title": "Python",
          "url": "https://www.python.org/"
        },
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 4,
          "id": 8,
          "title": "Udacity",
          "url": "https://www.udacity.com/"
        }
      ]
    },
    {
      "id": 5,
      "name": "Information",
      "urls": [
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 5,
          "id": 10,
          "title": "Encyclopedia",
          "url": "https://www.encyclopedia.com/"
        },
        {
          "date_add": "Sat, 02 May 2020 00:00:00 GMT",
          "directory_id": 5,
          "id": 9,
          "title": "Wikipedia",
          "url": "https://www.wikipedia.org/"
        }
      ]
    }
  ]
}
```

**GET** `/directories/<int:id>`

- Returns all bookmarks in a given directory.
- Body: None
- Permissions: `User`, `Admin`
- Response:

```json
{
  "bookmarks": [
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 1,
      "id": 1,
      "title": "Youtube",
      "url": "https://www.youtube.com"
    },
    {
      "date_add": "Sat, 02 May 2020 00:00:00 GMT",
      "directory_id": 1,
      "id": 2,
      "title": "Veoh",
      "url": "https://www.veoh.com/"
    }
  ]
}
```

**POST** `/bookmarks/create`

- Creates a new bookmark.
- Body: {"title": "title of bookmark", "url": "addres of bookmark", "directory_id" : #id of direcotry}
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "The Bookmark ('title') was created successfully!"
}
```

**POST** `/directories/create`

- Creates a new directory.
- Body: {"name": "name of directory"}
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "The Directory ('name') was created successfully!"
}
```

**PATCH** `/bookmarks/<int:id>/modify`

- Modify a bookmark using its `id`.
- Body: one or more of the following:
  - title
  - url
  - directory_id
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "Message": "The Bookmark ('url') was modified successfully!"
}
```

**PATCH** `/directories/<int:id>/modify`

- Modify a directory using its `id`.
- Body: name
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "The Directory ('name') was modified successfully!"
}
```

**DELETE** `/bookmarks/<int:id>/delete`

- Delete a bookmark using its `id`.
- Body: None
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "The Bookmark ('url') was deleted successfully!"
}
```

**DELETE** `/directories/<int:id>/delete`

- Delete a directory using its `id`. This will delete all its contained bookmarks.
- Body: None
- Permissions: `Admin`
- Response:

```json
{
  "Success": True,
  "Message": "The Directory ('name') was deleted successfully!"
}
```
