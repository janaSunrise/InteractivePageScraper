"""
To Parse:
- Links
- Images
- Tables
- Heading and Subheadings
"""
import inquirer

questions = [
    inquirer.Text("site", message="Which site do you want to scrape"),
    inquirer.List(
        "parse_object",
        message="Which object do you want to parse",
        choices=["Headings and Subheadings", "Links", "Images", "Tables"]
    )
]
answers = inquirer.prompt(questions)

