from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from PIL import Image, ImageDraw, ImageFont
import re

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


def measure_text(text, font):
    image = Image.new('RGB', (1, 1), (255, 255, 255)
                      )  # Create a 1x1 white image
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font)
    return width, height


def process_element(element, font):
    if isinstance(element, NavigableString):
        # If it's a text element within an HTML tag, measure its text and record the width and height
        if (
            isinstance(element.parent, Tag)
        ):
            text = element.strip()
            if (len(text) > 0):
                width, height = measure_text(text, font)
                # Create a CSS rule to set the width and height for the element
                css_rule = f"width: {width}px; height: {height}px;"

                # Apply the CSS rule inline with the HTML tag
                if 'style' in element.parent.attrs:
                    current_styles = element.parent.attrs.get('style')
                    # Check if the style attribute do not already exist
                    if re.search(r'width.*:.*px', current_styles) is None:
                        existing_style = element.parent['style']
                        element.parent['style'] = f"{existing_style} {css_rule}"
                else:
                    # If not, set the new CSS rule as the style attribute
                    element.parent['style'] = css_rule

                element.replace_with('')  # Remove the text content
                print(f"Text: '{text}', Width: {width}px, Height: {height}px")
    elif isinstance(element, Tag):
        # If it's a tag (element)
        for child in element.contents:
            process_element(child, font)


# Create a Pillow font for text measurement (you can customize the font)
font = ImageFont.truetype("fonts/Arial.ttf", 16)

# Process the body element
body = soup.find('body')
process_element(body, font)

with open("newspapers/output.html", "w") as output_file:
    output_file.write(soup.prettify())
