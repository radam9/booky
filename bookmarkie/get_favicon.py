import favicon
import base64
import urllib3


def get_favicon(url):

    http = urllib3.PoolManager()

    icon_list = favicon.get(url)
    icon = icon_list[0]

    result = base64.b64encode(http.request("GET", icon.url).data)

    # this is the HTML format Icon data
    # icon = "data:image/" + icon.format + ";base64," + result.decode()

    icon_bytes = result.decode()

    return icon_bytes


def get_favicon_iconuri(url):

    http = urllib3.PoolManager()

    icon_list = favicon.get(url)
    icon = icon_list[0]

    result = base64.b64encode(http.request("GET", icon.url).data)

    # this is the HTML format Icon data
    # icon = "data:image/" + icon.format + ";base64," + result.decode()

    icon_bytes = result.decode()

    return icon_bytes, icon.url
