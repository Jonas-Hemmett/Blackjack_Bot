Jonas Hemmett
jonasgordonhemmett@gmail.com - johannes.hemmett@uvm.edu
# Game Rules
The goal of blackjack is to get a higher combination of card values than the dealer without going bust (over 21). Number cards are worth their value, face cards count as 10, and aces are worth 1 or 11 depending on if they would make you go bust. If you get 21 as your starting hand (Blackjack) you win a payout of 150%. Other wins payout 100%. Players go clockwise and the dealer plays last.

Hitting deals you another card, this is repeated as many times as you like.

Standing ends your turn for the game.

Splitting can only be done as your first move, it lets you play your two cards as separate hands, but only if they have the same value.

Doubling down can only be done as your first move, it deals you another card then ends your turn.
		
Surrendering can only be done as your first move, it lets you 50% your original bet back and removes you from the round.

# Why?
I wanted to combine my interest in card games with computer science to create a more efficient playstyle. I was also interested in the practical applications of AI and this was a good opportunity to use it. I started this project in CS 2210: Computer Organization and I've continued to expand it independently using concepts from CS 3240: Algorithm Design & Analysis and CS 2510: Intro Artificial Intelligence. 

The bot itself is designed solely for entertainment, I play cards with my friends fairly frequently so it's always fun when the blackjack bot gets to make an appearance.

# About Me
I’m currently a Computer Science major at the University of Vermont. I love creative problem solving and exploring how technology can bring my ideas to life. I enjoy building projects that combine code, CAD, and hands-on experimentation to create practical and creative solutions.

Outside of school, I always try to stay busy. I like skiing, leatherworking & fashion design, and playing games, whether they be video, card, or board.


# Custom Housing
In order to combine features like a camera, screen, and buttons with  the Raspberry Pi, I made a custom housing that fits all of them. I used CAD (Computer aided design) to design it on my computer.  I created sketches of the parts, combining dimensions of the Pi with the ideas I had in my head. Designing the custom housing took many iterations to get right as I had to make sure all of the parts fit together, many of the intermediate versions were made of paper while I worked with the FabLab to laser cut the final design out of acrylic. My favorite feature is the angle gauge on the side of the camera mount. Other features include engraved text, cable management for the camera, recessing the camera and buttons for increased durability, and covering the exposed circuitry.

# My Game Strategy
The standard strategy in blackjack is to follow the basic strategy chart popularized by Edward O. Thorp. It’s a table of moves where your cards are listed in the rows and the dealer’s are in the columns.  The problem with basic strategy is that the table used is static, so it will tell you to make the same move no matter what cards are in the deck. (E.G. you are at 12, there it will tell you to hit even if there are only 10s left). My strategy improves on this using expectiminimax. It runs every possible move with every possible card combination, then picks the move with the highest chance of winning. This solves the problem in basic strategy as my strategy changes its answer based on the cards left in the deck. One thing I did to further improve the efficiency of this algorithm was incorporating memoization, storing hand information in a dictionary, so identical hands would not have to be recomputed.

# User Interface
On a regular computer, the UI (user interface) is printed in the Python terminal. It displays all relevant information and takes user input through the keyboard, although it’s a little clunky, it gets the job done.

# However due to the small size of the screen on the Raspberry Pi, displaying the game info via the terminal wouldn't have made for a good user experience, so I made my own UI. The screen came with basic graphical starter code using the Pillow module in Python, which helped me get started which I modified heavily. Features include a scrollable menu bar allowing for options to be quickly chosen while not taking up much space; a menu to modify the cards being present, which gives a visual preview of what the table looks like; a menu which lets you take and view pictures stored on the Pi, these pictures can be processed and the cards present on a table will be input into a new game; and my personal favorite, a loading screen which simulates a card spinning in “3D”, the illusion of 3D is achieved by applying trig functions to a card which makes it appear to rotate. 

# In addition to the buttons on the Pi itself I designed a shoe insole which maps foot movement to keyboard input, allowing for a hands free user experience. I was shopping for microelectronics and I saw conductive fabric and I immediately knew I could use it for my project, combining it with some leftover denim, the sewing skills I learned in THE 1330: Stagecraft: Costumes, and an old shoe insole,  I built the custom insole. The old insole serves as a structural base while the denim sits on top with pieces of conductive fabric inlaid into the big toe and heel areas.


# Simulations & Local Gameplay
In order to test the effectiveness of my bot, I coded the game of blackjack from the ground up. This lets me simulate games locally on the Pi. What would take hours to play in real life can be simulated in seconds. I modified the simulation program, letting you play games against the computer on the device (i.e. a blackjack video game).

I tried a variety of different game and card counting strategies and as expected, more advanced strategies on average were more profitable. Running these simulations further proved to me how much of an edge the dealer really has and how it impacts profitably over the course of many games.

# Coding
This project is largely coded in Python. I chose Python largely because the microelectronics used (E.G. screen and buttons) natively support it and it's fast to code. However Python is an interpreted language. Meaning it’s relatively slow. This is not really an issue as compute speed is not the bottleneck in real games, and running thousands of games to test my algorithms is still effectively instant.

Because this project is made up of so many parts, composition and inheritance really helped to keep things simple. Each part is essentially made out of a few building blocks. For instance the file that contains the game logic can either be run through the Raspberry Pi UI or through the terminal. This is also how I build the bot logic, each bot is made up of a card counting part, a strategy part, and an IO part which handles how game information is received and displayed. Setting it up like this lets me try a variety of game strategies very quickly both in simulations and in real games.

# Image Recognition
In order to determine what cards are present on the table, an image of the table has to be viewed. Although computers are far better at the analytical side of blackjack, image recognition remains deceptively challenging. Like many problems in life, this one can be solved with ChatGPT.  Using the OpenAI API for Python, I upload an image to their servers, ChatGPT analyzes the image and returns a list of the cards it sees and who has them. However input validation is needed as factors like blurry images and covered cards can lead to incorrect outputs.

Although letting the bot run autonomously is a relatively simple feature to add, just requiring the bot to scan every couple seconds until the cards change, the high cost of image processing makes this feature prohibitely expensive. 

This project was my step into integrating artificial intelligence into a coding project. I found the technical integration to be relatively simple, but getting AI to constantly do what I wanted it to was more difficult. It often felt like working with a kindergartener who understands the basic task but not the fine details. I will continue to use AI in my projects going forward as it is extremely useful for specific tasks and I think many of the issues I had will be ironed out as development in the field continues to advance. 

I was also able to apply many of the concepts from my Intro Artificial Intelligence course (e.g. expectiminimax) to develop my own decision making system for this project.

# Next Steps
The next feature I want to add is an improved version of card counting. Traditional card counting assigns a score to each card (count), the running count determines the optimal bet size. My method would be broken into 3 parts based on the size of the remaining deck. 

Large deck: Use standard card counting.

Medium deck: Precompute games with my improved strategy and store the data in a list. The list will hold the cards present and the chance of winning. To use it, map the list of cards currently remaining to a precomputed game. This would push the limits of Python, so I would code the precomputing part in C++.

Small deck: Simulate different game outcomes in real time.


