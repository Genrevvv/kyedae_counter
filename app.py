
from comment_checker import check_kyedae_comment
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"

import asyncio
import pygame
import threading
import tkinter as tk


client = None
username = ""
connected = False

counter = 0 # Initialize counter

# Declare global variable for visual updates
input_entry = None
input_button = None
counter_label = None

message_frame = None
message_label = None

WIDTH = 303
HEIGHT = 260
BG_COLOR = "#c9c9c9"

pygame.mixer.init()
pygame.mixer.music.load("media_files/meow_sound_effect.mp3")


def main():
    print("Kyedae Counter has been launched.")
    root = tk.Tk()

    root.title("Kyedae Counter")
    root.resizable(False, False)
    root.attributes('-topmost', True)

    # Set window icon
    icon = tk.PhotoImage(file="media_files/kc_window_logo.png")
    root.iconphoto(True, icon)

    # Set x and y offset (center)
    x = (root.winfo_screenwidth() // 2) - (WIDTH // 2)
    y = (root.winfo_screenheight() // 2) - (HEIGHT // 2) - 25

    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    root.config(bg=BG_COLOR)

    # Main frame
    main_frame = tk.Frame(root, bg=BG_COLOR,)
    main_frame.pack()

    # Message
    global message_frame
    global message_label
    message_frame = tk.Frame(root)
    message_label = tk.Label(message_frame, text="", font=("Arial", 11), bg="#6979f5", fg="#ffffff", width=33, height=1)

    # Input username
    input_frame = tk.Frame(main_frame, bg="#c3c6db", pady=5, borderwidth=2, relief="solid")
    input_frame.pack()

    input_label = tk.Label(input_frame, text="Username:", font=("Arial", 10), bg="#c3c6db")
    input_label.grid(row=0, column=0, padx=1)

    global input_entry
    input_entry = tk.Entry(input_frame, font=("Arial", 11), width=19)
    input_entry.grid(row=0, column=1, padx=3)

    global input_button
    input_button = tk.Button(input_frame, text="connect", font=("Arial", 10), command=connect_username)
    input_button.grid(row=0, column=2, padx=1)

    # title Label
    title_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=0, pady=0)
    title_frame.pack()
    
    title_label = tk.Label(title_frame, text="Kyedae counter", font=("Arial", 22, "bold"), bg=BG_COLOR, padx=5, pady=5)
    title_label.pack()

    # Counter label
    counter_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=0, pady=10)
    counter_frame.pack()

    global counter
    global counter_label
    counter_label = tk.Label(counter_frame, text=str(counter), font=("Arial", 30), bg="white", width=5, height=1, pady=7,
                             highlightbackground="#000000", highlightthickness=2)
    counter_label.pack()

    # Buttons
    button_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10, pady=10)
    button_frame.pack()

    # Increment button
    increment_button = tk.Button(button_frame, text="+1", font=("Arial", 15), command=lambda : update_kyedae_counter("inc", False),
                                 bg="#969fe3", width=7, height=2, anchor="center", activebackground="#646ba3")
    increment_button.grid(row=0, column=1, padx=5)
 
    # Decrement button
    decrement_button = tk.Button(button_frame, text="-1", font=("Arial", 15), command=lambda : update_kyedae_counter("dec", False),
                                 bg="#969fe3", width=7, height=2, anchor="center", activebackground="#646ba3")
    decrement_button.grid(row=0, column=0, padx=5)
    
    root.mainloop()


# Connect usename
def connect_username():
    global client
    global username
    global input_button
    global input_entry
    global message_frame
    global message_label

    message_frame.place(x=0, y=0)

    message_label.config(text="Connecting")
    message_label.pack()

    username = "@" + input_entry.get()
    print(f"Connecting to {username}'s live.")

    input_button.config(state="disable")
    input_entry.config(state="disable")

    client = TikTokLiveClient(unique_id=username)
    client.on(CommentEvent)(on_comment)

    thread = threading.Thread(target=start_client, daemon=True)
    thread.start()


async def on_comment(event: CommentEvent):
    global connected
    
    if not connected:
        connected = True
        await connected_message()

    print(f"{event.user.nickname}: {event.comment}")

    if (check_kyedae_comment(event.comment)):
        update_kyedae_counter("inc", True)


# Update kyadae counter: Increment or decrement
def update_kyedae_counter(action, playSound):
    global counter 
    global counter_label

    if action == "inc":
        counter += 1
    elif action == "dec":
        if counter - 1 >= 0:
            counter -= 1

    if playSound:
        pygame.mixer.music.play()

    counter_label.config(text=str(counter))
    print(f"kyedae: {counter}")


async def connected_message():
    global message_frame
    global message_label

    message = "Connection Successful"

    message_label.config(text=message, bg="#02c265")
    print(message)

    await asyncio.sleep(2)

    message_label.pack_forget()
    message_frame.place_forget()


def start_client():
    asyncio.run(run_client())


# Run client: conncet to client stream
async def run_client():
    global message_frame
    global message_label

    attempt = 0
    
    while True:
        try:
            await client.connect() 
        except Exception as e:
            if attempt == 4:
                message_label.config(text="Connection Failed. Restart the program.", bg="#ff4545")
                await asyncio.sleep(30)

                message_label.pack_forget()
                message_frame.place_forget()
                break
                
            attempt += 1
            print(f"Error: {e}, reconnecting in 3 seconds...")
            await asyncio.sleep(3)


if __name__ == "__main__":
    main()
      