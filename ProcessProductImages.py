# This script will process all product images inside a folder and subfolders as follows:
# remove the image background.
# Crop the image size to fit the product dimensions only.
# resize the cropped product image to a specific size.
# create a new canvas with a specific size and color and paste the product image into it

from PIL import Image
import math
import os
from pathlib import Path
from rembg import remove

# Change output image name and format


def append_id(filename):
    p = Path(filename)
    return "{0}_{2}{1}".format(Path.joinpath(p.parent, p.stem), ".png", "Processed")


# crop image
# https://gist.github.com/odyniec/3470977.js


def autocrop_image(img, border=0):
    # Get the bounding box
    bbox = img.getbbox()

    # Crop the image to the contents of the bounding box
    img = img.crop(bbox)

    # Determine the scale and height of the cropped image
    (scale, height) = img.size

    # Add border
    scale += border * 2
    height += border * 2

    # Create a new image object for the output image
    cropped_image = Image.new("RGBA", (scale, height), (0, 0, 0, 0))

    # Paste the cropped image onto the new image
    cropped_image.paste(img, (border, border))

    # Done!
    return cropped_image


# resize cropped image and maintain the ratio
# https://gist.github.com/tomvon/ae288482869b495201a0.js


def resize_image(img, myScale):

    img_width, img_height = img.size

    # check if the image is aportrait
    if img_height > img_width:

        hpercent = (myScale/float(img_height))
        wsize = int((float(img_width)*float(hpercent)))
        resized_img = img.resize((wsize, myScale), Image.Resampling.LANCZOS)

    # check if the image is landscape
    if img_width > img_height:

        wpercent = (myScale/float(img_width))
        hsize = int((float(img_height)*float(wpercent)))
        resized_img = img.resize((myScale, hsize), Image.Resampling.LANCZOS)

    return resized_img

# Place and center the image on the new canvas
# https://stackoverflow.com/questions/2563822/how-do-you-composite-an-image-onto-another-image-with-pil-in-python


def resize_canvas(img, canvas_width, canvas_height):

    old_width, old_height = img.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    mode = img.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.alpha_composite(
        img, ((canvas_width - old_width) // 2, (canvas_height - old_height) // 2))

    return newImage


image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


# Process images inside folders and subfolders


def process_files(folder_dir):
    for entry in os.scandir(folder_dir):
        if entry.is_file() and entry.name.lower().endswith(image_extensions):
          # Process the image
            image_path = entry.path
            img = Image.open(image_path)
            output_path = append_id(image_path)
            removedBGimage = remove(img, True)
            croppedImage = autocrop_image(removedBGimage, 0)
            resizedImage = resize_image(croppedImage, 700)
            compinedImage = resize_canvas(resizedImage, 1000, 1000)
            compinedImage.save(output_path)

        elif entry.is_dir():
            process_files(entry.path)  # Recursively process subdirectory

# Path to images
folder_dir = "YOUR/IMAGES/PATH"
process_files(folder_dir)
