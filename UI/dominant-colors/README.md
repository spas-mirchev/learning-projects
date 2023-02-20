# Dominant colors

A Flask based web app, which shows the dominant colours in a picture

[dominant-colours.webm](https://user-images.githubusercontent.com/33859135/220184001-df0fba9c-99d9-496f-aede-736d1a70a18b.webm)

### Usage

User uploads a picture, and the app returns N number of most dominant colours in it.

Can be controlled with 2 parameters:

1. Number of colours
2. Delta - the colour difference

### Algorithm

I'm using the k-means clustering algorithm for color quantization from the OpenCV library.

### Credits

- [Color Quantization with OpenCV using K-Means Clustering
  ](https://pyimagesearch.com/2014/07/07/color-quantization-opencv-using-k-means-clustering/)
