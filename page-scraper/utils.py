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


def write_to_file(content: str, filename: str) -> None:
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"Wrote to the file {filename}")
    except Exception as e:
        print(log(f"{e!r}"))
