from PIL import Image, ImageDraw, ImageFont
width = 240
height = 240
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
fnt = ImageFont.truetype("../DejaVuSans.ttf", 20)
fnt2 = ImageFont.truetype("../DejaVuSans.ttf", 30)

# Setup above
draw.rectangle((0, 0, width, height - 60), fill = (92, 155, 51))
draw.rectangle((0, height - 60, width, height), fill = (100, 100, 100))


def dispHands(hands):
    cardDim = (30, 40)
    splitNum = len(hands)

    for split in range(splitNum):
        hidden = len(hands[split]) <= 1

        splitCenter = ((width - 30) * (1 / (splitNum + 1)) * split) + 15 +  (width - 30) * (1 / (splitNum + 1))
        # draw.rectangle((splitCenter - 2, 0, splitCenter + 2, 180), fill = (0, 0, 0))
        for num in range(len(hands[split]) + hidden):
            draw.rectangle((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0], (-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90, splitCenter + 0.5 * cardDim[0] + num * 0.35 * cardDim[0], (0.5 * cardDim[1]) - num * 0.75 * cardDim[1] + height - 90), fill = (100, 0, 0))
            
            if num < len(hands[split]):
                draw.rectangle((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0] + 2, (-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90 + 2, splitCenter + 0.5 * cardDim[0] + num * 0.35 * cardDim[0] - 2, (0.5 * cardDim[1]) - num * 0.75 * cardDim[1] + height - 90 - 2), fill = (255, 255, 255))
                _, _, textWidth, textHeight = draw.textbbox((0, 0), str(hands[split][num]), font=fnt)

                draw.text((((splitCenter - 0.5 * cardDim[0] + num * 0.35 * cardDim[0]) + 0.5 * (cardDim[0] - textWidth)), ((-0.5 * cardDim[1]) - num * 0.75 *  cardDim[1] + height - 90) + 0.5 * (cardDim[1] - textHeight)), str(hands[split][num]), font=fnt, fill = (0, 0, 0))
        
            
        # for card in range(splitNum):
        #     draw.rectangle((splitCenter - 0.5 * cardDim[0], (80 - 0.5 * cardDim[1]) + card * cardDim[1], splitCenter + 0.5 * cardDim[0], (80 + 0.5 * cardDim[1]) + card * cardDim[1]), fill = (255, 255, 255))

    # draw.text(((width-textWidth)/2, (height-textHeight - 20) / 2), str(hands), font=fnt, fill = (255, 255, 255))


hands = [[10, 11], [10, 2, 7]]
dispHands(hands)

_, _, textWidth, textHeight = draw.textbbox((0, 0), "Continue", font=fnt)

draw.text(((width-textWidth)/2, height-textHeight - 20), "Continue", font=fnt, fill = (255, 255, 255))
image.show()
