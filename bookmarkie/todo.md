1. Main project to-do:

   - Category list:

     - [] Change highlight of selected category
     - [x] add bootstrap list
     - [x] Add divider between links/directories/categories
     - [x] Add Bold/colour for collabsible directories
     - [] Add badges to folders/categories (number of links)
     - [x] Change link colour on hover

- [x] Modify bookmarks_parser to parse html into models class and add to database
- [] Modify bookmarks_parser.parse_url to get the icon and icon_uri (or get the icon from an outside source like google favicons)
- [x] Modify main view/route to quiery db and put items in html
- [] Javascript API/Route (maybe with modal) edit folders/categories/bookmarks
- [] Javascript API/Route (maybe with modal) delete folders/categories/bookmarks
- [] Alert when deleting folder/link
- [] Javascript API/Route (maybe with modal) to add new folder/category/bookmark
- [] Select multiple links/folders
- [] Javascript to drag and drop items to different folders and have the move reflected on the database
- [] reorder items inside categories/folders
- [] maybe add functionality to re-allocate folders/subfolders (if drag and drop doesn't work)
- [x] get favicon.ico

2. Create script to export:
   - [] Chrome standard HTML
   - [] Chrome standard JSON
   - [] Firefox standard HTML
   - [] Firefox standard JSON
   - [] Different methods (RegExp/XML/HTML)
3. bookmarks_parser.py
   - [x] how to include chrome "Other Bookmarks"
   - properly format the json to fit the firefox and chrome standard json format
