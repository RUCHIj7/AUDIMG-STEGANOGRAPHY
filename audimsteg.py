import wave
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel, StringVar, Label, Entry, Button
from PIL import Image

# Audio Steganography Functions
def hide_message(audio_file, output_file, message):
    try:
        with wave.open(audio_file, mode='rb') as audio:
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

            message += '###'
            message_bits = ''.join(format(ord(char), '08b') for char in message)

            if len(message_bits) > len(frame_bytes):
                raise ValueError("Message is too large to hide in the provided audio file.")

            for i in range(len(message_bits)):
                frame_bytes[i] = (frame_bytes[i] & 254) | int(message_bits[i])

            with wave.open(output_file, 'wb') as modified_audio:
                modified_audio.setparams(audio.getparams())
                modified_audio.writeframes(bytes(frame_bytes))

        messagebox.showinfo("Success", f"Message hidden successfully in {output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def reveal_message(audio_file):
    try:
        with wave.open(audio_file, mode='rb') as audio:
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

            extracted_bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            message = ''.join(
                chr(int(''.join(map(str, extracted_bits[i:i+8])), 2))
                for i in range(0, len(extracted_bits), 8)
            )

            message = message.split('###')[0]
            return message

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Image Steganography Functions
def encryption(img, data):
    data_in_binary = ''.join([format(ord(char), '08b') for char in data])
    data_in_binary += '00000000'

    data_index = 0
    pixels = list(img.getdata())

    for i in range(len(pixels)):
        if data_index < len(data_in_binary):
            pixel = list(pixels[i])
            for j in range(3):
                if data_index < len(data_in_binary):
                    pixel[j] = pixel[j] & ~1 | int(data_in_binary[data_index])
                    data_index += 1
            pixels[i] = tuple(pixel)
        else:
            break

    img.putdata(pixels)

def main_encryption(img, text, new_image_name):
    try:
        image = Image.open(img, 'r')

        if not text or not new_image_name:
            messagebox.showerror("Error", "Please provide all inputs before encoding.")
            return

        new_image = image.copy()
        encryption(new_image, text)

        new_image_name += '.png'
        new_image.save(new_image_name, 'PNG')
        messagebox.showinfo("Success", f"Image successfully encoded and saved as {new_image_name}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Image file not found! Please check the file path.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main_decryption(img, strvar):
    try:
        image = Image.open(img, 'r')
        data = ''
        pixels = list(image.getdata())

        binary_data = ''
        for pixel in pixels:
            for value in pixel[:3]:
                binary_data += str(value & 1)

                if len(binary_data) % 8 == 0:
                    char = chr(int(binary_data[-8:], 2))
                    if char == '\x00':
                        strvar.set(data)
                        return
                    data += char

        strvar.set(data)
    except FileNotFoundError:
        messagebox.showerror("Error", "Image file not found! Please check the file path.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI Functions
def encode_audio():
    input_audio = filedialog.askopenfilename(title="Select Input WAV File", filetypes=[("WAV files", "*.wav")])
    if not input_audio:
        return

    output_audio = filedialog.asksaveasfilename(title="Save Encoded WAV File", defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if not output_audio:
        return

    secret_message = simpledialog.askstring("Secret Message", "Enter the message to hide:")
    if not secret_message:
        return

    hide_message(input_audio, output_audio, secret_message)

def decode_audio():
    input_audio = filedialog.askopenfilename(title="Select Encoded WAV File", filetypes=[("WAV files", "*.wav")])
    if not input_audio:
        return

    revealed_message = reveal_message(input_audio)
    if revealed_message:
        messagebox.showinfo("Revealed Message", f"Hidden message: {revealed_message}")

def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='#D8BFD8')

    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='#D8BFD8', fg='#4B0082').place(x=220, rely=0)
    Label(encode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 13), bg='#D8BFD8', fg='#4B0082').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='#D8BFD8', fg='#4B0082').place(x=10, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13), bg='#D8BFD8', fg='#4B0082').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)
    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)
    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='#E6E6FA', command=lambda:
           main_encryption(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=220, y=175)

def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='#D8BFD8')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='#D8BFD8', fg='#4B0082').place(x=220, rely=0)
    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12), bg='#D8BFD8', fg='#4B0082').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()
    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='#E6E6FA', command=lambda:
           main_decryption(img_entry.get(), text_strvar)).place(x=220, y=90)

    Label(decode_wn, text='Text that has been encoded in the image:', font=("Times New Roman", 12), bg='#D8BFD8',
          fg='#4B0082').place(x=180, y=130)

    text_entry = Entry(decode_wn, width=94, textvariable=text_strvar, state='disabled')
    text_entry.place(x=15, y=160, height=100)

# Main GUI
root = tk.Tk()
root.title('Steganography Tool')
root.geometry('400x300')
root.resizable(0, 0)
root.config(bg='#D8BFD8')

Label(root, text='Steganography Tool', font=('Arial black', 18), bg='#D8BFD8', fg='#4B0082').pack(pady=10)
Button(root, text='Encode Audio', width=25, font=('Times New Roman', 13), bg='#E6E6FA', command=encode_audio).pack(pady=5)
Button(root, text='Decode Audio', width=25, font=('Times New Roman', 13), bg='#E6E6FA', command=decode_audio).pack(pady=5)
Button(root, text='Encode Image', width=25, font=('Times New Roman', 13), bg='#E6E6FA', command=encode_image).pack(pady=5)
Button(root, text='Decode Image', width=25, font=('Times New Roman', 13), bg='#E6E6FA', command=decode_image).pack(pady=5)
Button(root, text='Exit', width=25, font=('Times New Roman', 13), bg='#E6E6FA', command=root.quit).pack(pady=10)

root.mainloop()
