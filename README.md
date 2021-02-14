# Bookmarkie

Bookmarkie is a bookmarks manager web application using Flask (Python).
The Code for the application can be found here [Github-Bookmarkie](https://www.github.com/radam9/booky), while the API code for the application can be found here [Link](https://github.com/radam9/Udacity-Full-Stack-Developer-Nanodegree/tree/master/5.%20Capstone%20Project/Bookmarkie)

Link to [Live Demo](https://bookmarkie.herokuapp.com)

##### The App has the following functionality:
- Import a HTML/JSON bookmarks file from Firefox or Chrome (while keeping the hierarchy tree).
- Store the bookmarks in a SQLite3 database.
- Display the bookmarks as nested lists, which allows the user to see the full structure of his bookmarks.
- Create, edit and delete bookmarks and folders.
- Export the bookmarks as HTML/JSON (in Firefox format).

##### The App was built using the following technologies:
- Python
- Flask
- Flask-SQLAlchemy
- Requests
- Pillow
- BeautifulSoup4
- Javascript
- FontAwesome
- Bootstrap4

## Details

1. Parsing the HTML/JSON bookmarks was achieve using regular expressions, beautifulsoup4 and a recursive function.
2. Using a SQLAlchemy model, the bookmarks were inserted into a SQLite3 database.
3. The frontend uses javascript's Fetch (AJAX requests) to update the contents of the modals and the bookmarks.
