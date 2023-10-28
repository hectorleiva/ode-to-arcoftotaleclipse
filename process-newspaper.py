from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

# Read HTML content from a file
with open("newspapers/nytimes_direct_download.html", "r") as file:
    html_content = file.read()

# Load the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Define a function to process and modify the HTML


def process_element(element):
    if isinstance(element, NavigableString):
        # If it's a text element, measure its text and record the width and height in pixels
        text = element.strip()
        width = len(text) * 10  # For example, assume 10 pixels per character
        height = 20  # Example height in pixels
        # You can use a more accurate method to measure the text size
        # Create a CSS rule to set the width and height for the element
        css_rule = f"width: {width}px; height: {height}px;"
        # Apply the CSS rule inline with the HTML tag
        element.parent['style'] = css_rule
        element.replace_with('')  # Remove the text content

        print(f"Text: '{text}', Width: {width}px, Height: {height}px")
    elif isinstance(element, Tag):
        # If it's a tag (element)
        for child in element.contents:
            process_element(child)


# Process the body element
body = soup.find('body')
process_element(body)

with open("newspapers/output.html", "w") as output_file:
    output_file.write(soup.prettify())
