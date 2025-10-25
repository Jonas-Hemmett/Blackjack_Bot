
import base64
from openai import OpenAI

def keyRead():
    try:
        with open("../key.txt", "r") as file:
            next(file)

            rawKey = file.read().strip()

            if (rawKey[0] != "s" or rawKey[1] != "k" or rawKey[2] != "-"):
                print("Key is missing!")
                
                raise Exception("Key error")
            
    except:
        rawKey = input("Type your API key here or any key to continue:")
    
    try:
        return OpenAI(api_key = rawKey)

    except Exception as e:
        return f"keyRead file error: {e}"


def analyzeImage(imagePath):
    try:
        with open(imagePath, "rb") as image_file:
            base64Image = base64.b64encode(image_file.read()).decode("utf-8")

        # Send image to GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "List the cards of a blackjack game for a Python program. List the cards each player and the dealer has in the following format: '[(role): (order which turn is played): [card 1 value, card 2, value ...]]'. status is either 'd' for dealer, 'p' for other player, or 's' for self. each entry is seperated by '\n'. the dealer always goes last. Only include the card value and not the suit, aces are worth 1. The picture is taken from the perspective of a player, the dealer is at the top. Do not include anything in your repsonse besides the specified information"},
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this game."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64Image}"}}
                ]}
            ],
            max_tokens = 300  # Adjust token limit for response length
        )

        # Extract and return response text
        return response.choices[0].message.content

    except Exception as e:
        return f"imgageAnalyzeError: {e}"

def chat(input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input}]
        )
    except Exception as e:
        return f"OpenAI Error: {e}"
    
    return response.choices[0].message.content

#print(analyzeImage("hand.jpg"))

client = keyRead()

print(chat("hi"))
