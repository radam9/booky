from bs4 import BeautifulSoup
from .models import Directory, Url
from datetime import datetime


def format_datetime(date):
    return datetime.fromtimestamp(int(date))


def indexer(item, index):
    """
    Add position index for urls and folders
    """
    if isinstance(item, Directory):
        item.position = index
        index += 1
        item.update()
    elif isinstance(item, Url):
        item.position = index
        index += 1
    return index


def parse_url(child, parent_id):
    """
    Function that parses a url tag <DT><A>, creates a url and returns the ID
    """
    date_added = format_datetime(child.get("add_date"))
    url = Url(
        title=child.text,
        url=child.get("href"),
        parent_id=parent_id,
        icon=child.get("icon"),
        date_added=date_added,
    )
    ## still need to parse Icon and Icon_URI, or run a different function that gets the icon for the url.

    # getting tags and icon_uri
    icon_uri = child.get("icon_uri")
    if icon_uri:
        url.icon_uri = icon_uri
    tags = child.get("tags")
    if tags:
        url.tags = tags.split(",")
    return url


def parse_folder(child, parent_id):
    """
    Function that parses a folder tag <DT><H3>
    """
    date_added = format_datetime(child.get("add_date"))
    folder = Directory(title=child.text, parent_id=parent_id, date_added=date_added,)
    # for Bookmarks Toolbar in Firefox and Bookmarks bar in Chrome
    if child.get("personal_toolbar_folder"):
        folder.special = "toolbar"
    # for Other Bookmarks in Firefox
    if child.get("unfiled_bookmarks_folder"):
        folder.special = "other_bookmarks"
    folder.insert()
    return folder


def recursive_parse(node, parent_id):
    """
    Function that recursively parses folders and lists <DL><p>
    """
    index = 0
    # case were node is a folder
    if node.name == "dt":
        folder = parse_folder(node.contents[0], parent_id)
        recursive_parse(node.contents[2], folder.id)
        return folder
    # case were node is a list
    elif node.name == "dl":
        for child in node:
            tag = child.contents[0].name
            if tag == "h3":
                folder = recursive_parse(child, parent_id)
                index = indexer(folder, index)
            elif tag == "a":
                url = parse_url(child.contents[0], parent_id)
                index = indexer(url, index)
                url.insert()


def parse_root_firefox(root):
    """
    Function to parse the root of the firefox bookmark tree
    """
    # create bookmark menu folder
    bookmarks = Directory(title="Bookmarks Menu", parent_id=0, position=0)
    bookmarks.insert()
    index = 0  # index for bookmarks/bookmarks menu
    main_index = 1  # index for root level
    for node in root:
        # skip node if not <DT>
        if node.name != "dt":
            continue
        # get tag of first node child
        tag = node.contents[0].name
        if tag == "a":
            url = parse_url(node.contents[0], bookmarks.id)
            index = indexer(url, index)
            url.insert()
        if tag == "h3":
            folder = recursive_parse(node, bookmarks.id)
            # check for special folders (Other Bookmarks / Toolbar)
            # add them to root level instead of inside bookmarks
            try:
                check = folder.special
            except AttributeError:
                check = None
            if check:
                folder.parent_id = 0
                main_index = indexer(folder, main_index)
            else:
                index = indexer(folder, index)


def parse_root_chrome(root):
    """
    Function to parse the root of the chrome bookmark tree
    """
    # Create "other bookmarks" folder
    other_bookmarks = Directory(title="Other Bookmarks", parent_id=0, position=1)
    other_bookmarks.insert()
    index = 0  # Index counter for position of Urls/Directories
    for node in root:
        if node.name != "dt":
            continue
        # get the first child element (<H3> or <A>)
        element = node.contents[0]
        tag = element.name
        # if an url tag is found at root level, add it to "Other Bookmarks"
        if tag == "a":
            url = parse_url(node.contents[0], other_bookmarks.id)
            index = indexer(url, index)
            url.insert()
        elif tag == "h3":
            # if a folder tag is found at root level, check if its the main "Bookmarks Bar", else append to "Other Bookmarks" children
            if element.get("personal_toolbar_folder"):
                folder = recursive_parse(node, 0)
                folder.position = 0
                folder.update()
            else:
                folder = recursive_parse(node, other_bookmarks.id)
                index = indexer(folder, index)


# Main function
def main(bookmarks_file):
    """
    Main function, takes in a HTML bookmarks file from Chrome/Firefox and returns a JSON nested tree of the bookmarks.
    """
    # Open HTML Bookmark file and pass contents into beautifulsoup
    with open(bookmarks_file, encoding="Utf-8") as f:
        soup = BeautifulSoup(markup=f, features="html5lib", from_encoding="Utf-8")
    # Check if HTML Bookmark version is Chrome or Firefox
    # Get the main DL list (root) out of the html file
    # Parse the root of the bookmarks tree
    heading = soup.find("h1")
    root = soup.find("dl")
    if heading.text == "Bookmarks":
        parse_root_chrome(root)
    elif heading.text == "Bookmarks Menu":
        parse_root_firefox(root)

