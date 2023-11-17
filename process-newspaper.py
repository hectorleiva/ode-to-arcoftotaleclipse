from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from PIL import ImageFont

# Read HTML content from a file
with open("newspapers/nytimes_direct_download.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# html_content = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Sample Page</title>
# </head>
# <body>
#     <div>
#         <p>This is some text.</p>
#         <img src="image.jpg" alt="An image">
#         <p>More text here.</p>
#         <span>Just text</span>
#         <div>
#             <p>Inner text</p>
#         </div>
#     </div>
#     <ul class="css-1xhq0o5"><li class="summary-class" style="width: 694px; height: 72px;">With Israeli troops now on the ground in Gaza, Prime Minister Benjamin Netanyahu said in a televised speech that it would be a “long and difficult” campaign.</li><li class="summary-class" style="width: 687px; height: 53px;">Hamas’s armed wing said its forces were fighting Israeli soldiers inside the enclave, but Israeli officials have not publicly called the push an invasion.</li></ul>
# </body>
# </html>
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
            if has_english_text(element.get_text()) and not any(child.name for child in element.children if child.name):
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
