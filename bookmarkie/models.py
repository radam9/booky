import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

# Set up database info
database_filename = "bookmarkie.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

# bind the flask appication and the SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Models
class Url(db.Model):
    """ Model representing the URLs, where:
    id-> id of the url
    title-> title of url
    url-> url address
    date_added-> date url was added on
    date_modified-> date url was last modified
    icon-> location to favicon.ico for the app, not standard html content
    tags-> tags describing url
    position-> current position to remember order of urls in directory
    directory_id-> id of the directory the url is contained in"""

    __tablename__ = "Url"

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    url = Column(String(500), nullable=False)
    date_added = Column(Date, nullable=False, default=datetime.utcnow)
    # date_modified = Column(Date)
    # icon = Column(String(256))
    # tags = Column(String(500))
    # position = Column(Integer)
    directory_id = Column(Integer, db.ForeignKey("Directory.id"))

    def __init__(self, title, url, directory_id):
        # self.title = if title = none use url
        self.title = title
        self.url = url
        self.directory_id = directory_id

    def __repr__(self):
        return f"{self.url} -in- {self.directory_id}"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "date_added": self.date_added,
            # "date_modified": self.date_modified,
            # "icon": self.icon,
            # "tags": self.tags,
            # "position": self.position,
            "directory_id": self.directory_id,
        }

    @staticmethod
    def serialize_list(bookmarks):
        return [b.serialize() for b in bookmarks]


class Directory(db.Model):
    """ Model representing bookmark directories, where:
    id-> id of the directory
    name-> name of the directory
    abs_path-> absolute path of the directory from the root (using directory id not name)
    parent_id-> id of parent directory
    urls-> urls contained in the directory"""

    __tablename__ = "Directory"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    # abs_path = Column(String(256), nullable=False)
    # parent_id = Column(Integer, nullable=False)
    urls = db.relationship(
        "Url",
        cascade="save-update, merge, delete, delete-orphan",
        backref="directory",
        lazy=False,
    )

    def __init__(self, name):
        self.name = name
        # self.abs_path = abs_path
        # self.parent_id = abs_path.split("/")[-1]

    def __repr__(self):
        return f"{self.name} -at- {self.abs_path}"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "abs_path": self.abs_path,
            # "parent_id": self.parent_id,
            "urls": [b.serialize() for b in self.urls],
        }

    @staticmethod
    def serialize_list(result):
        return [d.serialize() for d in result]
