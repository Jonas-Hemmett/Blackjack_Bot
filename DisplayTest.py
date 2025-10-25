# from PIL import Image, ImageDraw, ImageFont
# image = Image.new("RGB", (400, 400))
# draw = ImageDraw.Draw(image)

# draw.rectangle((0, 0, 400, 400), fill = (0, 0, 0))
# camIn = Image.fromarray(frame).resize((int(width * (1 if camRatio > 1 else camRatio)), int(height * (1 if camRatio < 1 else 1 / camRatio))), Image.NEAREST)
# image.show()