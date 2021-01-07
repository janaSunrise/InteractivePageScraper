import re

from .utils import get_website_content

from bs4 import BeautifulSoup
import inquirer
import pandas as pd

choices = ["Headings and Subheadings", "Links", "Images", "Tables"]
questions = [
    inquirer.Text("site", message="Which site do you want to scrape"),
    inquirer.List(
        "parse_object",
        message="Which object do you want to parse",
        choices=choices
    )
]
answers = inquirer.prompt(questions)

# Get the site's content
site = "https://" + answers["site"] if not answers["site"].startswith("https://") else answers["site"]
content = get_website_content(site)

# Create the soup
soup = BeautifulSoup(content, "lxml")

# Match the choices
choice = answers["parse_object"]
if choice == choices[0]:
    headings = soup.find_all(["h1", "h2", "h3"])

    if not headings or len(headings) == 0:
        print("No headings found!")
    else:
        headings = [heading.text for heading in headings]
        print(headings)
elif choice == choices[1]:
    links = soup.find_all("a")

    if not links or len(links) == 0:
        print("No links found!")
    else:
        links = [(link["href"], link.text) for link in soup.find_all("a")]
        print(links)
elif choice == choices[2]:
    images = soup.find_all("img")

    if not images or len(images) == 0:
        print("No images found!")
    else:
        images = [image["src"] for image in images]
        print(images)
else:
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
