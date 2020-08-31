import os
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from .models import setup_db, Url, Directory, Bookmark
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from .get_favicon import get_favicon_iconuri
from sqlalchemy.exc import OperationalError
from . import bookmarks_parser

# Raise error if no query results
def check_query(result):
    if not result:
        abort(404)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SuperAwsomeSecretKey"
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(app_dir, "static/uploads/")
    app.config["DOWNLOAD_FOLDER"] = os.path.join(app_dir, "static/downloads/")
    # Initialize the database
    db = SQLAlchemy()
    setup_db(app)

    # Welcome home route
    @app.route("/")
    def index():
        try:
            root = Directory.query.get("1")
            return render_template("index.html", context={"root": root, "master": root})
        except OperationalError:
            return render_template("index_empty.html")

    # Route to return url/directory edit modal
    @app.route("/modal_edit/<string:item_id>")
    def modal_edit(item_id):
        item = Bookmark.query.get(item_id)
        return render_template("modal_edit.html", item=item)

    # Route to return url/directory/database delete modal
    @app.route("/modal_delete/<string:item_id>")
    def modal_delete(item_id):
        if item_id == "Database":
            return render_template("modal_delete.html", item="Database")
        item = Bookmark.query.get(item_id)
        return render_template("modal_delete.html", item=item)

    # Route to return url/directory create modal
    @app.route("/modal_create/<string:bk_type>")
    def modal_create(bk_type):
        directories = (
            Directory.query.filter_by(type="Directory").order_by(Directory.id).all()
        )
        for d in directories:
            if d.parent_id == None:
                d.path = "/" + d.title + "/"
            else:
                d.path = d.parent.path + d.title + "/"
        directories.sort(key=lambda x: x.path)
        return render_template(
            "modal_create.html", context={"directories": directories, "type": bk_type}
        )

    # Route to delete entire database
    @app.route("/drop_database")
    def drop_database():
        Bookmark.__table__.drop(db.engine)
        return redirect(url_for("index"))

    # Route to upload Bookmarks file
    @app.route("/upload_bookmark", methods=["GET", "POST"])
    def upload_bookmark():
        if request.method == "GET":
            return render_template("modal_upload.html")
        else:
            if request.files:
                bookmark_file = request.files["the_bookmark"]
                filename = secure_filename(bookmark_file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                bookmark_file.save(file_path)
                Bookmark.__table__.create(db.engine)
                bookmarks_parser.main(file_path)
                os.remove(file_path)
            return redirect(url_for("index"))

    # Route to download Bookmarks file
    @app.route("/download_bookmark/<string:filetype>")
    def download_bookmark(filetype):
        filename = "HTML Filename" if filetype == "HTML" else "JSON Filename"
        return send_from_directory(
            app.config["DOWNLOAD_FOLDER"], filename=filename, as_attachment=True,
        )

    # Route to display selected directory
    @app.route("/d/<int:dir_id>")
    def display_directory(dir_id):
        root = Directory.query.get("1")
        directory = Directory.query.get(str(dir_id))
        master = {
            "title": directory.title,
            "id": directory.id,
            "links": [],
            "folders": [],
        }
        for bookmark in directory.children:
            if bookmark.type == "Url":
                master["links"].append(bookmark)
            elif bookmark.type == "Directory":
                master["folders"].append(bookmark)

        return render_template(
            "display_directory.html", context={"root": root, "master": master}
        )

    # Route to get all bookmarks
    @app.route("/bookmarks")
    def get_bookmarks():
        # Get all bookmarks
        result = Url.query.all()

        # Raise 404 if not bookmarks where found
        check_query(result)

        # Format the bookmarks
        bookmarks = Url.serialize_list(result)

        return jsonify({"bookmarks": bookmarks}), 200

    # Route to get all directories
    @app.route("/directories")
    def get_directories():
        # Get all directories
        result = Directory.query.all()

        # Raise 404 if no directories found
        check_query(result)

        # Format the directories
        directories = Directory.serialize_list(result)

        return jsonify({"directories": directories}), 200

    # Route to get all bookmarks in a given directory id
    @app.route("/directories/<int:id>")
    def get_bookmarks_by_directory(id):
        try:
            # Get all bookmarks in directory with given id
            result = Directory.query.get(id).urls

            # Raise 404 if not bookmarks found
            check_query(result)

            # Format the bookmarks
            bookmarks = Url.serialize_list(result)

            return jsonify({"bookmarks": bookmarks}), 200
        except Exception:
            abort(404)

    # Route to create a bookmark
    @app.route("/bookmarks/create", methods=["POST"])
    def create_bookmark():
        # Attempt to create bookmark
        try:
            # Get request body
            body = request.get_json()
            title = body.get("title")
            url = body.get("url")
            parent_id = str(body.get("parent_id"))
            icon_uri, icon = get_favicon_iconuri(url)
            # Create bookmark
            bookmark = Url(
                title=title, url=url, parent_id=parent_id, icon=icon, icon_uri=icon_uri,
            )
            bookmark.insert()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.title}) was created successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if not body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to create a directory
    @app.route("/directories/create", methods=["POST"])
    def create_directory():
        # Attempt to create a directory
        try:
            # Get request body
            body = request.get_json()
            title = body.get("title")
            parent_id = str(body.get("parent_id"))
            # Create directory
            directory = Directory(title=title, parent_id=parent_id)
            directory.insert()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Directory ({directory.title} was created successfully!)",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to modify a bookmark
    @app.route("/bookmarks/<int:id>/modify", methods=["PATCH"])
    def modify_bookmark(id):
        # Get the bookmark to modify
        bookmark = Url.query.get(id)

        # Raise 404 if bookmark doesn't exit
        check_query(bookmark)

        # Attempt to modify the bookmark
        try:
            # Get request body
            body = request.get_json()
            # list of attributes to search for inside the request body.
            attrs = ["title", "url", "tags", "position", "parent_id"]
            for attr in attrs:
                value = body.get(attr)
                if value:
                    # Modify bookmark if attr exists
                    setattr(bookmark, attr, value)
            bookmark.update()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.url}) was modified successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to modify a directory
    @app.route("/directories/<int:id>/modify", methods=["PATCH"])
    def modify_directory(id):
        # Get the directory to modify
        directory = Directory.query.get(id)

        # Raise 404 if directory doesn't exit
        check_query(directory)

        # Attempt to modify the directory
        try:
            # Get request body
            body = request.get_json()
            # list of attributes to search for inside the request body.
            attrs = ["title", "parent_id", "position"]
            for attr in attrs:
                value = body.get(attr)
                if value:
                    # Modify directory if attr exists
                    setattr(directory, attr, value)
            directory.update()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The directory ({directory.title}) was modified successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to delete a bookmark
    @app.route("/bookmarks/<int:id>/delete", methods=["DELETE"])
    def delete_bookmark(id):
        # Get the bookmark to delete
        bookmark = Url.query.get(id)
        # Raise 404 if bookmark doesn't exit
        check_query(bookmark)
        # Attempt to delete bookmark
        try:
            bookmark.delete()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.url}) was deleted successfully!",
                    }
                ),
                200,
            )
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to delete a directory
    @app.route("/directories/<int:id>/delete", methods=["DELETE"])
    def delete_directory(id):
        # Get the directory to delete
        directory = Directory.query.get(id)
        # Raise 404 if directory doesn't exit
        check_query(directory)
        # Attempt to delete directory
        try:
            directory.delete()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Directory ({directory.title}) was deleted successfully!",
                    }
                ),
                200,
            )
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # 400 error handler
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"Success": False, "Error": 400, "Message": "Bad Request"}),
            400,
        )

    # 401 error handler
    @app.errorhandler(401)
    def unauthorized(error):
        return (
            jsonify({"Success": False, "Error": 401, "Message": "Unauthorized"}),
            401,
        )

    # 404 error handler
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"Success": False, "Error": 404, "Message": "Resource Not Found"}),
            404,
        )

    # 405 error handler
    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"Success": False, "Error": 405, "Message": "Method Not Allowed"}),
            405,
        )

    # 422 error handler
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"Success": False, "Error": 422, "Message": "Unprocessable Entity"}
            ),
            422,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
