1. Main project to-do:

   - [] check that the application is running after having renamed the `Directory` class to `Folder` (and all the related naming has been changed from `directory` to `folder`), and changed the `Bookmark` type name to lowercase.
   - [/] Category list:

     - [x] Change highlight of selected category
     - [x] add bootstrap list
     - [x] Add divider between links/directories/categories
     - [x] Add Bold/colour for collabsible directories
     - [] Add badges to folders/categories (number of links)
     - [x] Change link colour on hover

- [x] Modify bookmarks_parser to parse html into models class and add to database
- [/] Modify bookmarks_parser.parse_url to get the icon and icon_uri (or get the icon from an outside source like google favicons) **NOTE** Very slow and unefficient
- [x] Modify main view/route to quiery db and put items in html
- [x] Javascript API/Route (maybe with modal) edit folders/categories/bookmarks
- [x] Javascript API/Route (maybe with modal) delete folders/categories/bookmarks
- [x] Alert when deleting folder/link
- [x] Javascript API/Route (maybe with modal) to add new folder/category/bookmark
- [x] Javascript API/Route (with modal) to import (and parse) bookmarks (HTML)
- [x] Javascript API/Route (with modal) to import (and parse) bookmarks (JSON)
- [x] Route to export Bookmarks as JSON/HTML
- [x] Javascript API/Route (modal) clear database (with warning alert/modal)
- [] Select multiple links/folders
- [] Javascript to drag and drop items to different folders and have the move reflected on the database
- [] reorder items inside categories/folders
- [] maybe add functionality to re-allocate folders/subfolders (if drag and drop doesn't work)
- [x] Change color of bootstrap Success/Danger colors.
- [x] get favicon.ico
- [] make sure correct file is provided for import in "/upload_bookmark" route, if not raise error
- [] fix location of import/export file conversion and filename
- [] Unittest for entire APP
- [] Documentation
- [] Video Demonstration

2. Create script to export:
   - [] Chrome standard HTML
   - [] Firefox standard HTML
3. Bookmarks Parser in Different Methods:

   - [/] Iteration/Stack
     - [] Regular Expressions
     - [x] XML
     - [x] Import HTML (Firefox/Chrome)
     - [x] Export HTML (Firefox)
     - [x] Import JSON (Firefox/Chrome/Bookmarkie)
     - [x] Export JSON (Bookmarkie)
     - [x] Import DB (Bookmarkie-SQLAlchemy)
     - [x] Export DB (Bookmarkie-SQLAlchemy)
   - [/] Recursion
     - [] Regular Expressions
     - [x] XML
     - [x] HTML
   - [] Serialize
     - [] BeautifulSoup Object
     - [] Boomarkie Database Model Object
     - [] lxml.etree Object
   - [] See how I can optimize the 2 versions I wrote (HTML Recursion/Iteration-Stack)

4. bookmarks_parser.py
   - [x] how to include chrome "Other Bookmarks"
5. Tweaks (for aesthetics/efficiency/better practice)
   - [] add **slots** to the model class to reduce memory usage (check Python Cookbook p.248 / 8.4)
   - [] refactor the edit/delete javascript (one function contains the modal call, then add listener to cancel and confirm, then another fetch function for the final api call (delete/edit))
   - [x] return an ordered list of directories (ordered by path) at /modal_create/ route
   - [x] create_modal folder list, `show path` but get `ID`

**NOTES**

- one could modify the HTML file to either remove all <DT> and <p> tags, take the inner title of <A> and <H3> and add it as a value="" attribute, and then move all the elements inside <DL> into <H3> instead. Then one could work with a proper object, maybe copy the object or create a mirroring class and use that to import the root object into the database, or output as JSON.
- look into beautifulsoup builder (tree builder) (more info inside the beautifulsoup class code)
