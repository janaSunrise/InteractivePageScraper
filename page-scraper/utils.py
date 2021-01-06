import sys
import typing as t

import requests


def log(message: str, msg_type: str = "ERROR") -> str:
    return f"[{msg_type.upper()}] {message}"


def get_website_content(site: str) -> t.Optional[bytes]:
    req = requests.get(site)

    if req.status_code != 200:
        print(log(f"Could not establish connection to the site specified ({site})"))
        sys.exit(1)

    return req.content
