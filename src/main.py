import tkinter as tk
from tkinter import filedialog
import pygame
from PIL import Image
import numpy as np
import cv2

# Initialize Tkinter root, but don't show any window
root = tk.Tk()
root.withdraw()

# User input for selecting the bit depth
print("Select the bit depth:")
print("1. 8-bit")
print("2. 16-bit")
option = input("Enter the option number: ")

# Validate the user input and set the bit depth
if option == "1":
    bit_depth = 8
elif option == "2":
    bit_depth = 16
else:
    print("Invalid option selected. Using default 8-bit conversion.")
    bit_depth = 8

# Open a file dialog to select an image
file_path = filedialog.askopenfilename()

# Ensure that a file was selected
if file_path:
    # Load and process the image
    image = Image.open(file_path)
    image.thumbnail((16, 16), Image.LANCZOS)  # Resize for 16x16 sprite use

    # Convert image to the selected bit depth
    if bit_depth == 8:
        # Convert to 8-bit palette image
        image = image.convert("RGBA")  # Convert to a format compatible with Pygame
    elif bit_depth == 16:
        # Convert to grayscale and then to 16-bit
        grayscale_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        image = Image.fromarray(np.uint16(grayscale_image)).convert("RGBA")

    # Initialize Pygame and set up the window
    pygame.init()
    screen = pygame.display.set_mode(image.size)

    # Convert image for Pygame use
    mode = "RGBA"  # Set mode directly for Pygame compatibility
    data = image.tobytes("raw", mode)
    sprite = pygame.image.fromstring(data, image.size, mode)

    # Main loop to display the sprite
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(sprite, (0, 0))
        pygame.display.flip()

    pygame.quit()

    # Save the processed image as a PNG file
    output_file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if output_file_path:
        image.save(output_file_path)
        print("Image saved successfully.")
    else:
        print("Image not saved.")
else:
    print("No file selected.")
