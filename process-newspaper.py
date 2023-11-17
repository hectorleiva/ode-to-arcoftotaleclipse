from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from PIL import ImageFont

# Read HTML content from a file
with open("newspapers/nytimes_direct_download.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# html_content = """
# <span class="css-nch2d">
#     LIVE
#     <time aria-hidden="true" class="css-16lxk39" datetime="2023-10-28T19:41:21.338Z">
#         <div class="css-ki347z">
#             <span class="css-1stvlmo" data-time="abs" style="visibility: hidden;">
#             Oct. 28, 2023, 3:41 p.m. ET
#             </span>
#             <span class="css-d2btor" data-time="rel" style="visibility: hidden;">
#             Just now
#             </span>
#         </div>
#     </time>
#     <span aria-live="polite" class="css-1dv1kvn" style="visibility: hidden;">
#         Just
#         now
#     </span>
# </span>
# """

# Load the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')


def addHiddenStyleToElement(element):
    # Check if the element already has a "style" attribute
    if 'style' in element.attrs:
        # Append the CSS rule to the existing styles
        element['style'] += '; visibility: hidden;'
    else:
        # Add the CSS rule "visibility: hidden" as a new style attribute
        element['style'] = 'visibility: hidden;'


def hide_english_text_recursive(element):
    # Function to check if a string contains English text (simple check for illustration)
    def has_english_text(s):
        # You may want to implement a more sophisticated check based on your requirements
        return any(char.isalpha() or char.isdigit() for char in s)

    if element.name:
        # Check if the element has English text directly inside (not in children)
        # Check if the tag is not a script or style tag and not an img tag (exclude code and images)
        if element.name.lower() not in ['script', 'style'] and element.name.lower() != 'img':
            if (has_english_text(element.get_text()) and not any(child.name for child in element.children if child.name)) or element.get_text().strip() == 'LIVE':
                addHiddenStyleToElement(element)

    # Recursively call the function for all child elements
    for child in element.children:
        if child.name:
            hide_english_text_recursive(child)


# Process the body element
hide_english_text_recursive(soup.body)


# The output is good, but we need to disable the Javascript from running which re-injects the text that we are hiding
with open("newspapers/output.html", "w") as output_file:
    output_file.write(soup.prettify())
