import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def generate_qr_code(data, filename='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return img

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Title
        title_label = tk.Label(root, text="QR Code Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter text or URL:", font=("Arial", 12)).pack(anchor="w")
        self.entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
        self.entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        generate_btn = tk.Button(button_frame, text="Generate QR Code", command=self.generate_qr, bg="#4CAF50", fg="white", font=("Arial", 12))
        generate_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(button_frame, text="Save QR Code", command=self.save_qr, bg="#2196F3", fg="white", font=("Arial", 12))
        save_btn.pack(side=tk.LEFT, padx=5)

        # QR Code display
        self.canvas = tk.Canvas(root, width=250, height=250, bg="#f0f0f0", relief="sunken", bd=2)
        self.canvas.pack(pady=10)
        self.canvas.create_text(125, 125, text="QR Code will appear here", font=("Arial", 10), fill="gray")

        self.qr_image = None
        self.qr_filename = 'qrcode.png'

    def generate_qr(self):
        data = self.entry.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter some text or URL.")
            return

        try:
            img = generate_qr_code(data, self.qr_filename)
            # Resize for display
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            self.qr_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(125, 125, image=self.qr_image)
            messagebox.showinfo("Success", "QR Code generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code: {str(e)}")

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("Warning", "Generate a QR Code first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            try:
                img = Image.open(self.qr_filename)
                img.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved as {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR Code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()