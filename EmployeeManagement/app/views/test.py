import tkinter as tk
from PIL import Image, ImageTk
import os

root = tk.Tk()
root.title("Test Gambar")

# Ganti path ini kalau kamu simpan di lokasi berbeda
image_path = os.path.join("app", "resources", "icon.jpg")
abs_path = os.path.abspath(image_path)
print("Coba load dari:", abs_path)

try:
    img = Image.open(abs_path).resize((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=img_tk)
    label.image = img_tk  # Simpan referensi biar gak kehapus
    label.pack(padx=20, pady=20)

    tk.Label(root, text="Ini gambar kamu 👆").pack()

except Exception as e:
    print("❌ Gagal load gambar:", e)

root.mainloop()
