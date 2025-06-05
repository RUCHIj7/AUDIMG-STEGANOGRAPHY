# AUDIMG-STEGANOGRAPHY
Here is the same **detailed `README.md`** for your project, but **without the Table of Contents** section for a cleaner look:

---

### ✅ `README.md`

````markdown
# 🔐 Audio & Image Steganography Tool

A GUI-based Python application that allows users to **hide (encode)** and **reveal (decode)** secret messages in both **WAV audio** and **PNG image** files using steganography techniques. This is a simple yet effective tool for learning and demonstrating how steganography works in multimedia files.

---

## 🚀 Features

- ✅ Encode secret messages into `.wav` audio files
- ✅ Decode hidden messages from stego-audio
- ✅ Embed messages in `.png` image files by altering pixel data
- ✅ Extract messages from stego-images
- ✅ Simple and user-friendly GUI using Tkinter
- ✅ Visual feedback through dialogs and alerts

---
## 🔍 How It Works

### 🧠 Audio Steganography
- Each byte in a WAV file's frame data is slightly modified.
- The **Least Significant Bit (LSB)** of each byte is changed to match the bits of the message.
- A delimiter (`###`) is used to indicate the end of the message.

### 🖌️ Image Steganography
- The message is converted into binary.
- Each bit is embedded in the LSBs of the RGB values of image pixels.
- The process continues until the entire message is embedded, ending with a null character.

---

## 💻 Installation

**### 1. Clone the Repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

### 2. Install Dependencies

This project requires Python 3 and the `Pillow` library.

```bash
pip install Pillow
```

---

## 🛠️ Usage

### 1. Run the Application

```bash
python audimsteg.py
```

This launches the GUI with the following options:

### 2. GUI Options

* 🔊 **Encode Audio**
  Select an input `.wav` file, enter your message, and specify a name to save the output.

* 🔍 **Decode Audio**
  Select a `.wav` file previously encoded, and view the hidden message.

* 🖼️ **Encode Image**
  Enter the path to a `.png` image, your secret message, and a name to save the new image.

* 🔓 **Decode Image**
  Provide a `.png` file and extract the hidden message.

---

## 📁 File Structure

```
AUDIMG-STEGANOGRAPHY
├── audimsteg.py       # Main GUI and logic for audio/image steganography
├── README.md          # Project documentation
├── .gitignore         # Files to exclude from GitHub
```

---

## 🙋‍♂️ Contributing

Contributions, suggestions, and improvements are welcome!
Feel free to fork this repository and submit a pull request.

---


---

## ⚠️ Disclaimer

This tool is intended for educational and ethical purposes only.
**Do not use this tool to hide data or transmit messages unlawfully.**

```


