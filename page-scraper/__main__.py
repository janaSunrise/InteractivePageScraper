from .utils import get_website_content

from bs4 import BeautifulSoup
import inquirer

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

choice = answers["parse_object"]
if choice == choices[0]:
    headings = soup.find_all(["h1", "h2", "h3"])

    if not headings or len(headings) == 0:
        print("No headings found!")
    else:
        headings = [heading.text for heading in headings]
elif choice == choices[1]:
    links = soup.find_all("a")

    if not links or len(links) == 0:
        print("No links found!")
    else:
        links = [(link["href"], link.text) for link in soup.find_all("a")]
elif choice == choices[2]:
    images = soup.find_all("img")

    if not images or len(images) == 0:
        print("No images found!")
    else:
        images = [image["src"] for image in images]
else:
    print("Tables not implemented!")
