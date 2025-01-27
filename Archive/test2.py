def settings():
    # messagebox.showinfo("Message", "*game begins*")
    T = tk.Text(root, height=2, width=30)
    w = Scale(root, from_=0, to=42, orient=HORIZONTAL)
    T.insert(tk.END, "GAME SETTINGS")
    T.pack()
    w.pack()
    w = Scale(root, from_=0, to=200, orient=HORIZONTAL)
    w.pack()

def start_game():
    T = tk.Text(root, height=2, width=30)
    T.insert(tk.END, "LOADING...")
    T.pack()



# Create a button
button = tk.Button(root, text="Play", command=start_game)
button.pack(pady=10)

button = tk.Button(root, text="Settings", command=settings)
button.pack(pady=10)