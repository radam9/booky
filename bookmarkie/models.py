import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, DateTime
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
    """ Model representing the URLs
    ...
    Attributes
    ----------
    id : int
        id of the url
    title : str
        title of url
    url : str
        url address
    date_added : datetime
        date url was added on
    icon : str
        html icon data
    icon_uri : str
        html icon_uri found in firefox bookmarks
    tags : str
        tags describing url
    position : int
        current position to remember order of urls in directory
    parent_id : int
        id of the directory the url is contained in"""

    __tablename__ = "Url"

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    url = Column(String(500), nullable=False)
    date_added = Column(DateTime, nullable=False, default=datetime.utcnow)
    icon = Column(String)
    icon_uri = Column(String)
    tags = Column(String(500))
    position = Column(Integer)
    parent_id = Column(Integer, db.ForeignKey("Directory.id"))

    def __init__(
        self,
        title,
        url,
        parent_id,
        date_added=None,
        icon=None,
        icon_uri=None,
        tags=None,
        position=None,
    ):
        if title == None:
            self.title = url
        else:
            self.title = title
        self.url = url
        self.date_added = date_added
        self.icon = icon
        self.icon_uri = icon_uri
        self.tags = tags
        self.position = position
        self.parent_id = parent_id

    def __repr__(self):
        return f"{self.url} -in- {self.parent_id}"

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
            "icon": self.icon,
            "icon_uri": self.icon_uri,
            "tags": self.tags,
            "position": self.position,
            "parent_id": self.parent_id,
        }

    @staticmethod
    def serialize_list(bookmarks):
        return [b.serialize() for b in bookmarks]


class Directory(db.Model):
    """ Model representing bookmark directories
    ...
    Attributes
    ----------
    id : int
        id of the directory
    title : str
        name of the directory
    date_added : datetime
        date directory was added on
    parent_id : int
        id of parent directory
    position : int
        current position in parent directory
    urls : db relationship
        urls contained in the directory"""

    __tablename__ = "Directory"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    date_added = Column(DateTime, nullable=False, default=datetime.utcnow)
    parent_id = Column(Integer, nullable=False)
    position = Column(Integer)
    urls = db.relationship(
        "Url",
        cascade="save-update, merge, delete, delete-orphan",
        backref="directory",
        lazy=False,
    )

    def __init__(self, title, parent_id, date_added=None, position=None):
        self.title = title
        self.date_added = date_added
        self.parent_id = parent_id
        self.position = position

    def __repr__(self):
        return f"{self.title} -at- {self.abs_path}"

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
            "parent_id": self.parent_id,
            "date_added": self.date_added,
            "position": self.position,
            "urls": [b.serialize() for b in self.urls],
        }

    @staticmethod
    def serialize_list(result):
        return [d.serialize() for d in result]
