# Used to test and built UI
from DisplayBase import *

z = 50

col = (255, 255, 255)

while True:
    fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", z)
    
    textWidth, textHeight = draw.textbbox((0, 0), str(z), font=fnt2)[2:4]

    x = (width - textWidth) / 2

    y = (height - textHeight) / 2

    draw.text((x, y), str(z), font=fnt2, fill= col)

    disp.image(image)

    while True:
        if not button_C.value:
            break
        if not button_L.value:
            col = (255, 0, 0)
            break

        elif not button_U.value:
            col = (0, 255, 0)
            break
        
        elif not button_R.value:
            col = (0, 0, 255)
            break

        elif not button_D.value:
            col = (255, 255, 255)
            break
        
        if not button_A.value:
            if z > 5:
                z -= 5
            break

        if not button_B.value:
            if z < 100:
                z += 5
            break

        # Display the Image

        time.sleep(0.01)
    
    draw.rectangle((0, 0, width, height), outline = 0, fill = (0, 0, 0))
