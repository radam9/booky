1. Main project to do list:
   - Change highlight of selected category
   - Modify bookmarks_parser to parse html into models class and add to database
   - Modify bookmarks_parser.parse_url to get the icon and icon_uri (or get the icon from an outside source like google favicons)
   - Modify main view/route to quiery db and put items in html
   - Add "right-click menu"/"menu-dropdown"/"modal window" to delete/edit links
   - Add "right-click menu"/"menu-dropdown"/"modal window" to delete/edit folders
   - Add "right-click menu"/"menu-dropdown"/"modal window" to delete/edit subfolders/categories
   - Alert when deleting folder/link
   - Select multiple links/folders
   - reorder items inside categories/folders
   - maybe add functionality to re-allocate folders/subfolders (if drag and drop doesn't work)
   - Javascript API/Route (maybe with modal) to add new folder/category/bookmark
   - Javascript to drag and drop items to different folders and have the move reflected on the database
   - Javascript API/Route (maybe with modal) edit folders/categories/bookmarks
   - get favicon.ico
   - create a portable psql file (like in udacity trivia project) containing test data.
2. Create script to export:
   - Chrome standard HTML
   - Chrome standard JSON
   - Firefox standard HTML
   - Firefox standard JSON
   - Different methods (RegExp/XML/HTML)
3. bookmarks_parser.py
   - how to include chrome "Other Bookmarks"
   - properly format the json to fit the firefox and chrome standard json format
