# Handles OpenAI API usage
import base64
from openai import OpenAI
import io
def keyRead():
    try:
        try:
            with open("../key.txt", "r") as file:
                next(file)

                rawKey = file.read().strip()
                
                assert rawKey[0] == "s" and rawKey[1] == "k" and rawKey[2] == "-"
        except:
            with open("/home/pi/CS2210/Blackjack/key.txt", "r") as file:
                next(file)

                rawKey = file.read().strip()
                
                assert rawKey[0] == "s" and rawKey[1] == "k" and rawKey[2] == "-"
    
    # If an API key can't be read from file the user can input one
    except Exception as e:
        print(f"keyRead file error: {e}")
        rawKey = input("Type your API key here or any key to continue: ")
    
    try:
        return OpenAI(api_key = rawKey)

    except Exception as e:
        return f"keyRead file error: {e}"

# Code below is mostly from OpenAI (Not Mine)
def analyzeImage(imagePath):
    try:
        with open(imagePath, "rb") as image_file:
            base64Image = base64.b64encode(image_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize a game of blackjack for a Python program. List the cards each player and the dealer has in the following format: '(role): card 1 value, card 2, value ...'. status is either 'd' for dealer, 'p' for other player, or 'u' for self. each entry is seperated by '\n'. the person on the left goes first but the dealer always goes last. Always add the dealer to the end of the string. The picture is from a players perspective so the dealer is at the top of the image and the players are at the bottom. Only include the card value and not the suit; Face cards are 10 and ace is 1. Do not include anything in your repsonse besides the specified information. Avoid at all costs but if an image can't be read return E. If only one player's cards are visible return u:[cards]"},
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this game."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64Image}"}}
                ]}
            ],
            max_tokens = 300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"imgageAnalyzeError: {e}"

def analyzeImagePIL(imageIn):
    try:
        img_bytes = io.BytesIO()
        imageIn.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        base64Image = base64.b64encode(img_bytes.read()).decode("utf-8")


        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize a game of blackjack for a Python program. List the cards each player and the dealer has in the following format: '(role): card 1 value, card 2, value ...'. status is either 'd' for dealer, 'p' for other player, or 'u' for self. each entry is seperated by '\n'. the person on the left goes first but the dealer always goes last. Always add the dealer to the end of the string. The picture is from a players perspective so the dealer is at the top of the image and the players are at the bottom. Only include the card value and not the suit; Face cards are 10 and ace is 1. Do not include anything in your repsonse besides the specified information. If only one player's cards are visible return u:[cards]"},
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this game."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64Image}"}}
                ]}
            ],
            max_tokens = 300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"imgageAnalyzeError: {e}"


# Used for testing, analyzeImage is slow and expensive 
def chat(input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input}]
        )
    except Exception as e:
        return f"OpenAI Error: {e}"
    
    return response.choices[0].message.content
# Code above is mostly from OpenAI (Not Mine)


if __name__ == "__main__":
    input("test?")
    client = keyRead()
    print(analyzeImage("hand2.jpg"))