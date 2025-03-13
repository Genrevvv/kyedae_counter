import subprocess
import time
import tkinter as tk


WIDTH = 300
HEIGHT = 270

def show_splash_screen():
    splash = tk.Tk()

    splash.overrideredirect(True) # Remove the title bar and control buttons

    splash.title("Loading...")
    splash.title("Kyedae Counter")
    splash.resizable(False, False)
    splash.attributes('-topmost', True)

    x = (splash.winfo_screenwidth() // 2) - (WIDTH // 2) + 10
    y = (splash.winfo_screenheight() // 2) - (HEIGHT // 2) - 20

    splash.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    logo = tk.PhotoImage(file="media_files/kc_loading_logo.png")
    
    label = tk.Label(splash, image=logo)
    label.photo = logo
    label.pack()

    # Run the main program after the splash screen
    #subprocess.Popen(["python", "app.py"])
    subprocess.Popen(["app.exe"])

    splash.after(4000, splash.destroy)  # Close after 4 seconds
    splash.mainloop()


if __name__ == "__main__":
    show_splash_screen()
