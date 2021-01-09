import re

from .utils import get_website_content, write_to_file

from bs4 import BeautifulSoup
import inquirer
import pandas as pd

choices = [
    "Page title",
    "Headings and Subheadings",
    "All paragraphs",
    "Links",
    "Images",
    "Tables",
    "All text from page",
    "Whole source code"
]
questions = [
    inquirer.Text("site", message="Which site do you want to scrape"),
    inquirer.List(
        "parse_object",
        message="Which object do you want to parse",
        choices=choices
    ),
    inquirer.Confirm("write_to_file", message="Should the output be written to file", default=False)
]
answers = inquirer.prompt(questions)

# Get the site's content
site = "https://" + answers["site"] if not answers["site"].startswith("https://") else answers["site"]
content = get_website_content(site)

# Create the soup
soup = BeautifulSoup(content, "lxml")

# Match the choices
choice = answers["parse_object"]
file_write = answers["write_to_file"]

if choice == choices[0]:
    title = soup.find("title")

    if not title:
        print("No page title detected.")
    elif file_write:
        write_to_file(title.text, "title.txt")
    else:
        print(title.text)
elif choice == choices[1]:
    headings = soup.find_all(["h1", "h2", "h3"])

    if not headings or len(headings) == 0:
        print("No headings found!")
    else:
        headings = [heading.text for heading in headings]
        if file_write:
            write_to_file("\n".join(headings), "headings.txt")
        else:
            print("\n".join(headings))
elif choice == choices[2]:
    paragraphs = soup.find_all("p")

    if not paragraphs or len(paragraphs) == 0:
        print("No paragraphs found!")
    else:
        paragraphs = [
            paragraph.text.replace("\n", "").strip() for paragraph in paragraphs
        ]
        if file_write:
            write_to_file("\n".join(paragraphs), "paragraphs.txt")
        else:
            print("\n".join(paragraphs))
elif choice == choices[3]:
    links = soup.find_all("a")

    if not links or len(links) == 0:
        print("No links found!")
    else:
        links = [str((link["href"], link.text)) for link in soup.find_all("a")]
        if file_write:
            write_to_file("\n".join(links), "links.txt")
        else:
            print("\n".join(links))
elif choice == choices[4]:
    images = soup.find_all("img")

    if not images or len(images) == 0:
        print("No images found!")
    else:
        images = [image["src"] for image in images]
        if file_write:
            write_to_file("\n".join(images), "image_urls.txt")
        else:
            print("\n".join(images))
elif choice == choices[5]:
    tables = soup.find_all("table")

    if not tables or len(tables) == 0:
        print("No table found!")
    else:
        table_list = []

        for index, table in enumerate(tables):
            table_list.append([])
            body = table.find_all("tr")

            head = body[0]
            body_rows = body[1:]

            table_list[index].append(tuple([
                item.text.rstrip("\n") for item in head.find_all("th")
            ]))

            for row_num in range(len(body_rows)):
                row = []
                for row_item in body_rows[row_num].find_all("td"):
                    aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
                    row.append(aa)

                table_list[index].append(tuple(row))

        for index, table in enumerate(table_list):
            table = pd.DataFrame(table[1:], columns=table[0])

            print(f"Table #{index + 1}\n{table}\n")
elif choice == choices[6]:
    complete_text = soup.get_text()
    if file_write:
        write_to_file(complete_text, "page_content.txt")
    else:
        print(complete_text)
else:
    code = soup.prettify()
    if file_write:
        write_to_file(code, "index.html")
    else:
        print(code)
