import tkinter as tk
from tkinter import ttk

def update_difficulty_label(*args):
    mines_label.config(text=f"Number of Mines: {int(mines.get())}")
    lives_label.config(text=f"Number of Lives: {int(lives.get())}")

def update_size_label(*args):
    width_label.config(text=f"Width: {int(width_value.get())}")
    height_label.config(text=f"Height: {int(height_value.get())}")

def show_difficulty():
    print(df.get())

def show_size():
    print(sz.get())

def toggle_slider(*args):
    if sz.get() == "Custom":
        width_slider.config(state=tk.NORMAL)
        height_slider.config(state=tk.NORMAL)
        size_frame.pack(side=tk.LEFT)  # Pack the frame to the left of the sliders
        width_label.pack()
        height_label.pack()
        update_size_label()
    else:
        width_slider.config(state=tk.DISABLED)
        height_slider.config(state=tk.DISABLED)
        size_frame.pack_forget()

    if df.get() == "Custom":
        mines_slider.config(state=tk.NORMAL)
        lives_slider.config(state=tk.NORMAL)
        difficulty_frame.pack(side=tk.LEFT)  # Pack the frame to the left of the sliders
        mines_label.pack()
        lives_label.pack()
        update_difficulty_label()
    else:
        mines_slider.config(state=tk.DISABLED)
        lives_slider.config(state=tk.DISABLED)
        difficulty_frame.pack_forget()

    # Schedule toggle_slider to be called again after 100 milliseconds
    root.after(100, toggle_slider)

    # Update the maximum value for mines_slider based on height and width
    mines_slider.config(to=(width_value.get() * height_value.get()) - 1)
    lives_slider.config(to=(mines.get())-1)

root = tk.Tk()
root.title("MineSweeper Game")

label = tk.Label(root, text="MINESWEEPER")
label.pack(pady=10)
label = tk.Label(root, text="by chirp")
label.pack(pady=8)

difficulties = [("Easy", 0.1), ("Medium", 0.2), ("Difficult", 0.3), ("Extreme", 0.4), ("Custom", 0.5)]
sizes = [("Small", 0.1), ("Medium", 0.2), ("Large", 0.3), ("Massive", 0.4), ("Custom", 0.5)]

df = tk.StringVar()
df.set("Easy")
sz = tk.StringVar()
sz.set("Small")

mines = tk.DoubleVar()
lives = tk.DoubleVar()
width_value = tk.DoubleVar()
height_value = tk.DoubleVar()

# Size options
tk.Label(root,
         text="Set Game Size:",
         justify=tk.LEFT,
         padx=20).pack()

for size, val in sizes:
    tk.Radiobutton(root,
                   text=size,
                   padx=20,
                   variable=sz,
                   command=lambda: [show_size(), toggle_slider()],
                   value=size).pack(anchor=tk.W)

# Sliders and labels for size
width_label = tk.Label(root, text="Width:")
width_label.pack()
width_slider = ttk.Scale(root, from_=1, to=100, orient="horizontal", length=400, state=tk.DISABLED, variable=width_value, command=lambda v: [width_value.set(v), update_size_label(), toggle_slider()])
width_slider.pack()

height_label = tk.Label(root, text="Height:")
height_label.pack()
height_slider = ttk.Scale(root, from_=1, to=50, orient="horizontal", length=400, state=tk.DISABLED, variable=height_value, command=lambda v: [height_value.set(v), update_size_label(), toggle_slider()])
height_slider.pack()

# Frame for size labels
size_frame = tk.Frame(root)

label = tk.Label(root, text=" ")
label.pack(pady=8)

# Set Game Difficulty
tk.Label(root,
         text="Set Game Difficulty:",
         justify=tk.LEFT,
         padx=20).pack()

for difficulty, val in difficulties:
    tk.Radiobutton(root,
                   text=difficulty,
                   padx=20,
                   variable=df,
                   command=lambda: [show_difficulty(), toggle_slider()],
                   value=difficulty).pack(anchor=tk.W)

# Sliders and labels for difficulty
mines_label = tk.Label(root, text="Number of Mines:")
mines_label.pack()
mines_slider = ttk.Scale(root, from_=1, to=500, orient="horizontal", length=400, state=tk.DISABLED, variable=mines, command=lambda v: [mines.set(v), update_difficulty_label()])
mines_slider.pack()

lives_label = tk.Label(root, text="Number of Lives:")
lives_label.pack()
lives_slider = ttk.Scale(root, from_=1, to=500, orient="horizontal", length=400, state=tk.DISABLED, variable=lives, command=lambda v: [lives.set(v), update_difficulty_label()])
lives_slider.pack()

# Frame for difficulty labels
difficulty_frame = tk.Frame(root)

def start_game():
    T = tk.Text(root, height=2, width=30)
    T.insert(tk.END, "LOADING...")
    T.pack()



# Create a button
button = tk.Button(root, text="Play", command=start_game)
button.pack(pady=10)

# Run the main loop
root.mainloop()
