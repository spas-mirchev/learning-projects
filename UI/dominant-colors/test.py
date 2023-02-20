
import cv2
from PIL import Image
import numpy as np


# # image = Image.open('static/uploads/cinema.jpg')
# # image.thumbnail((90,90))
# # image.save('thumbnail.jpg')
# img = Image.open(r'static/uploads/sample.jpg')
# width, height = img.size
# pallet = img.getcolors(width*height)

# most = [color[0] for color in pallet if color[0] > 3]
# most.sort(reverse=True)
# print(most[ : 9])


# Set this to the number of colors that you want to classify the images to
number_of_colors = 8

# Verify that the number of colors chosen is between the minimum possible and maximum possible for an RGB image.
assert 8 <= number_of_colors <= 16777216

# Get the cube root of the number of colors to determine how many bins to split each channel into.
number_of_values_per_channel = number_of_colors ** (1 / 3)
print(number_of_values_per_channel)

# We will divide each pixel by its maximum value divided by the number of bins we want to divide the values into (minus one for the zero bin).
divisor = 255 / (number_of_values_per_channel - 1)

# load the image and convert it to float32 for greater precision. cv2 loads the image in BGR (as opposed to RGB) format.
image = cv2.imread("static/uploads/cinema.jpg",
                   cv2.IMREAD_COLOR).astype(np.float32)

# Divide each pixel by the divisor defined above, round to the nearest bin, then convert float32 back to uint8.
image = np.round(image / divisor).astype(np.uint8)

# Flatten the columns and rows into just one column per channel so that it will be easier to compare the columns across the channels.
image = image.reshape(-1, image.shape[2])

# Find and count matching rows (pixels), where each row consists of three values spread across three channels (Blue column, Red column, Green column).
uniques = np.unique(image, axis=0, return_counts=True)

# The first of the two arrays returned by np.unique is an array compromising all of the unique colors.
colors = uniques[0]

# The second of the two arrays returend by np.unique is an array compromising the counts of all of the unique colors.
color_counts = uniques[1]

# Get the index of the color with the greatest frequency
most_common_color_index = np.argmax(color_counts)
print(most_common_color_index)

# Get the color that was the most common
most_common_color = colors[most_common_color_index]

# Multiply the channel values by the divisor to return the values to a range between 0 and 255
most_common_color = most_common_color * divisor

# If you want to name each color, you could also provide a list sorted from lowest to highest BGR values comprising of
# the name of each possible color, and then use most_common_color_index to retrieve the name.
print(most_common_color)
