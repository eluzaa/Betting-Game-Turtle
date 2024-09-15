import customtkinter as ctk
from turtle import Turtle, Screen
import random

# Tkinter setup for user input with CustomTkinter
def start_race():
    global num_players, user_bet, bet_amount
    try:
        num_players = int(entry_players.get())
        user_bet = int(entry_bet.get())
        bet_amount = int(entry_money.get())
        
        if num_players < 2 or num_players > 8:
            raise ValueError("Players should be between 2 and 8.")
        
        if user_bet < 1 or user_bet > num_players:
            raise ValueError(f"Bet should be on a turtle between 1 and {num_players}.")
        
        root.destroy()  # Close the Tkinter window after getting the input
        turtle_race()
    
    except ValueError as e:
        error_label.config(text=str(e))

# Function to handle the turtle race
def turtle_race():
    screen = Screen()
    screen.setup(width=1.0, height=1.0)  # Fullscreen mode
    screen.bgcolor("black")

    # Set up the finish line with three strips (white-black-white)
    finish_line = screen.window_width() // 2 - 100
    for i in range(3):
        line = Turtle()
        line.shape("square")
        line.shapesize(stretch_wid=0.2, stretch_len=30)  # Making line thick
        line.color("white" if i != 1 else "black")
        line.penup()
        line.goto(finish_line + (i - 1) * 10, screen.window_height() // 2)
        line.pendown()
        line.right(90)
        line.forward(screen.window_height())
        line.hideturtle()

    # Create turtles and evenly space them
    turtles = []
    colors = ["coral2", "DarkGreen", "aquamarine2", "DarkOliveGreen2", "DarkGoldenrod1", "bisque2", "purple", "cyan"]
    for i in range(num_players):
        new_turtle = Turtle(shape="turtle")
        new_turtle.shapesize(stretch_wid=2, stretch_len=2)  # Increase turtle size
        new_turtle.speed(0)
        new_turtle.color(colors[i % len(colors)])
        new_turtle.penup()
        new_turtle.goto(-screen.window_width() // 2 + 50, (i - num_players // 2) * 100)  # Evenly spaced turtles
        turtles.append(new_turtle)
        
        # Label each turtle with its number
        label = Turtle()
        label.hideturtle()
        label.penup()
        label.goto(new_turtle.xcor(), new_turtle.ycor() + 30)
        label.write(f"Turtle {i+1}", align="center", font=("Arial", 12, "bold"))

    # Race logic
    winner = None
    while winner is None:
        for i in turtles:
            i.forward(random.randint(1, 10))
            if i.xcor() > finish_line:
                winner = i
                break

    # Announce winner
    screen.bye()  # Close the Turtle screen
    announce_winner(turtles.index(winner) + 1)

# Function to announce the winner
def announce_winner(winner_num):
    winner_screen = ctk.CTk()
    winner_screen.title("Winner Announcement")

    result = f"Player {winner_num} Wins!\n"
    if winner_num == user_bet:
        result += f"Congratulations! You won the bet and earned ${bet_amount * 2}!"
    else:
        result += f"Sorry, you lost the bet of ${bet_amount}."

    label = ctk.CTkLabel(winner_screen, text=result, font=("Arial", 24))
    label.pack(pady=20)

    button = ctk.CTkButton(winner_screen, text="Exit", command=winner_screen.destroy, font=("Arial", 14))
    button.pack(pady=10)

    winner_screen.mainloop()

# Main Tkinter window for user input using CustomTkinter
root = ctk.CTk()
root.title("Turtle Betting Game")
root.geometry("400x400")

# Game description label
description = "Welcome to the betting game! \nHere you can select how many players you want to play with.\nMax 8 players can play, minimum 2 players.\nPlease enter the input properly. \nYou can bet on the turtles numbered 1 to (number of players).\n\nNote: Players must be in the range 2 to 8."
description_label = ctk.CTkLabel(root, text=description, font=("Arial", 14), wraplength=380)
description_label.pack(pady=10)

# Input fields
label = ctk.CTkLabel(root, text="Enter number of players (2-8):", font=("Arial", 14))
label.pack(pady=10)

entry_players = ctk.CTkEntry(root, font=("Arial", 14))
entry_players.pack(pady=10)

label_bet = ctk.CTkLabel(root, text="Enter your bet (choose turtle 1-8):", font=("Arial", 14))
label_bet.pack(pady=10)

entry_bet = ctk.CTkEntry(root, font=("Arial", 14))
entry_bet.pack(pady=10)

label_money = ctk.CTkLabel(root, text="Enter your bet amount ($):", font=("Arial", 14))
label_money.pack(pady=10)

entry_money = ctk.CTkEntry(root, font=("Arial", 14))
entry_money.pack(pady=10)

# Error label
error_label = ctk.CTkLabel(root, text="", font=("Arial", 12), text_color="red")
error_label.pack(pady=10)

# Continue button
button = ctk.CTkButton(root, text="Continue", command=start_race, font=("Arial", 14))
button.pack(pady=10)

root.mainloop()
