import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from bookmarkie import create_app
from bookmarkie.models import setup_db, Url, Directory
from initialize_db import empty_db, main as test_db
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".flaskenv")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
DATABASE_FILENAME = "bookmarkie_test.db"
DATABASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(DATABASE_DIRECTORY, DATABASE_FILENAME)


class BookmarkieTestCase(unittest.TestCase):
    """
    Class to test the Bookmarkie endpoints
    """

    def setUp(self):
        """Define test variable and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = f"sqlite:///{DATABASE_PATH}"
        self.header = {"Content-Type": "application/json"}

        # Initialize test database
        test_db(env="test")

        # binds the app to the current context and creates a new test database
        with self.app.app_context():
            self.db = SQLAlchemy()
            setup_db(self.app, self.database_path)
            self.db.init_app(self.app)

        # Initiate variables
        self.bookmarks = Url.query.all()
        self.directories = Directory.query.all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_bookmarks_success(self):
        """Test to check "/bookmarks" route success case"""
        response = self.client().get("/bookmarks", headers=self.header)
        data = json.loads(response.data)
        bookmarks = data["bookmarks"]
        bookmark = bookmarks[0]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(bookmarks, list)
        self.assertIsInstance(bookmark, dict)
        self.assertEqual(bookmark["id"], 1)
        self.assertEqual(bookmark["title"], "Youtube")
        self.assertEqual(bookmark["url"], "https://www.youtube.com")
        self.assertEqual(bookmark["directory_id"], 1)

    def test_get_bookmarks_failure(self):
        """Test to check "/bookmarks" route failure case"""
        # Empty the database
        empty_db()
        response = self.client().get("/bookmarks", headers=self.header)
        self.assertEqual(response.status_code, 404)

    def test_get_directories_success(self):
        """Test to check "/directories" route success case"""
        response = self.client().get("/directories", headers=self.header)
        data = json.loads(response.data)
        directories = data["directories"]
        directory = directories[0]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(directories, list)
        self.assertIsInstance(directory, dict)
        self.assertEqual(directory["id"], 1)

    def test_get_directories_failure(self):
        """Test to check "/directories" route failure case"""
        # Empty the database
        empty_db()
        response = self.client().get("/directories", headers=self.header)
        self.assertEqual(response.status_code, 404)

    def test_get_bookmarks_by_directory_success(self):
        """Test to check "/directories/<int:id>" route success case"""
        id = 1
        response = self.client().get(f"/directories/{id}", headers=self.header)
        data = json.loads(response.data)
        bookmarks = data["bookmarks"]
        bookmark = bookmarks[0]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(bookmarks, list)
        self.assertEqual(len(bookmarks), 2)
        self.assertIsInstance(bookmark, dict)
        self.assertEqual(bookmark["id"], 2)
        self.assertEqual(bookmark["title"], "Veoh")
        self.assertEqual(bookmark["url"], "https://www.veoh.com/")
        self.assertEqual(bookmark["directory_id"], 1)

    def test_get_bookmarks_by_directory_failure(self):
        """Test to check "/directories/<int:id>" route failure case"""
        id = 9001
        response = self.client().get(f"/directories/{id}", headers=self.header)
        self.assertEqual(response.status_code, 404)

    def test_create_bookmark_success(self):
        """Test to check "/bookmarks/create" route success case"""
        test_bookmark = {
            "title": "Flickr",
            "url": "https://www.flickr.com/",
            "directory_id": 3,
        }
        number_of_bookmarks = len(self.bookmarks)
        response = self.client().post(
            "/bookmarks/create", data=json.dumps(test_bookmark), headers=self.header,
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Url.query.all()), number_of_bookmarks + 1)
        self.assertEqual(
            len(Directory.query.get(test_bookmark["directory_id"]).urls), 3
        )

    def test_create_bookmark_failure(self):
        """Test to check "/bookmarks/create" route failure case"""
        response = self.client().post("/bookmarks/create", headers=self.header)
        self.assertEqual(response.status_code, 400)

    def test_create_directory_success(self):
        """Test to check "/directories/create" route success case"""
        test_directory = {"name": "Languages"}
        number_of_directories = len(self.directories)
        response = self.client().post(
            "/directories/create", data=json.dumps(test_directory), headers=self.header,
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Directory.query.all()), number_of_directories + 1)

    def test_create_directory_failure(self):
        """Test to check "/directories/create" route failure case"""
        response = self.client().post("/directories/create", headers=self.header)
        self.assertEqual(response.status_code, 400)

    def test_modify_bookmark_success(self):
        """Test to check "/bookmarks/<int:id>/modify" route success case"""
        id = 3
        title = {"title": "The Gmail"}
        response = self.client().patch(
            f"/bookmarks/{id}/modify", data=json.dumps(title), headers=self.header,
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_modify_bookmark_failure(self):
        """Test to check "/bookmarks/<int:id>/modify" route failure case"""
        id = 3
        response = self.client().patch(f"/bookmarks/{id}/modify", headers=self.header)
        self.assertEqual(response.status_code, 400)

    def test_modify_directory_success(self):
        """Test to check "/directories/<int:id>/modify" route success case"""
        id = 4
        name = {"name": "The Programming"}
        response = self.client().patch(
            f"/directories/{id}/modify", data=json.dumps(name), headers=self.header,
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_modify_directory_failure(self):
        """Test to check "/directories/<int:id>/modify" route failure case"""
        id = 4
        response = self.client().patch(f"/directories/{id}/modify", headers=self.header)
        self.assertEqual(response.status_code, 400)

    def test_delete_bookmark_success(self):
        """Test to check "/bookmarks/<int:id>/delete" route success case"""
        id = 9
        response = self.client().delete(f"/bookmarks/{id}/delete", headers=self.header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_bookmark_failure(self):
        """Test to check "/bookmarks/<int:id>/delete" route failure case"""
        id = 9001
        response = self.client().delete(f"/bookmarks/{id}/delete", headers=self.header)
        self.assertEqual(response.status_code, 404)

    def test_delete_directory_success(self):
        """Test to check "/directories/<int:id>/delete" route success case"""
        id = 5
        response = self.client().delete(
            f"/directories/{id}/delete", headers=self.header
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_directory_failure(self):
        """Test to check "/directories/<int:id>/delete" route failure case"""
        id = 9001
        response = self.client().delete(
            f"/directories/{id}/delete", headers=self.header
        )
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        """Delete the test database after finishing the test"""
        os.remove(DATABASE_PATH)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
