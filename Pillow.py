# Basic pillow test
from PIL import Image, ImageDraw, ImageFont
width = 400
height = width
image = Image.new("RGB", (width, height))
fnt = ImageFont.load_default()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), fill=(153, 204, 255))

_2, _2, textWidth, textHeight = draw.textbbox((0, 0), "", font = fnt)
draw.text(((width - textWidth)/2, (height - textHeight) / 2  - textHeight), "hand\nStuff", font=fnt, fill = (255, 255, 255))

image.show()