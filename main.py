# Imports
import pandas
import random
from tkinter import *

# Variables
BACKGROUND_COLOR = "#B1DDC6"
try:
    # Gets Data From Previous Turns
    words_csv = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # Uses French Word CSV if First Time Launching
    words_csv = pandas.read_csv("data/french_words.csv")
dict_of_words = {word.French:word.English for index, word in words_csv.iterrows()}
random_card = {}
tolearn = {'French':[French for French, English in dict_of_words.items()], 'English':[English for French, English in dict_of_words.items()]}

# New Flash Card Function
def nextCard():
    # Globals
    global random_card
    global timer
    global tolearn
    
    # Creating CSV File Out of Data
    new_csv = pandas.DataFrame.from_dict(tolearn)
    new_csv.to_csv("data/words_to_learn.csv", index=False)
    window.after_cancel(timer)
    
    # Checking If There Are Cards to Display
    if len(dict_of_words) > 0:
        random_card = random.choice(list(dict_of_words.items()))
    else:
        canvas.itemconfig(word_lb, text="Out Of Cards", fill="black")
        return
    
    # Changing Text/Image and Running Flipping Card Function
    canvas.itemconfig(language_lb, text="French", fill="black")
    canvas.itemconfig(word_lb, text=random_card[0], fill="black")
    canvas.itemconfig(image, image=front_img)
    timer = window.after(3000, flipCard)

def flipCard():
    # Flipping Card By Changing Text/Image
    canvas.itemconfig(language_lb, text="English", fill="white")
    canvas.itemconfig(word_lb, text=random_card[1], fill="white")
    canvas.itemconfig(image, image=back_img)

def knowCard():
    # Globals
    global dict_of_words
    global tolearn
    
    # Deleting Words Already Known
    del dict_of_words[random_card[0]]
    
    # Deleting Words If Learned
    if random_card[0] in tolearn["French"]:
        tolearn["French"].remove(random_card[0])
        tolearn["English"].remove(random_card[1])
    
    # Reseting Card
    nextCard()

# Creating Window
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setting Up Images
correct_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")

# Creating Canvas/Flash Card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
image = canvas.create_image(400, 263, image=front_img)
language_lb = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_lb = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Creating Buttons
wrong_btn = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=nextCard)
correct_btn = Button(image=correct_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=knowCard)
wrong_btn.grid(column=0, row=1)
correct_btn.grid(column=1, row=1)

# Running Function
timer = window.after(1, nextCard)
window.mainloop()