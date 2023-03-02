# Watermark project

This program allows the user to open one or more images and create a proportionally scaled watermark on all of them simultaneously with some text and a logo image.

The user can adjust the opacity of both the text and the logo.

When saving all the images, a mask is applied to maintain the adjusted settings of both the text and the logo.

The [Pillow python package](https://pypi.org/project/Pillow/) is used for dynamic text of the user text input. One of the biggest challenges was using both Tkinter and Pillow to achieve this dynamic text functionality.

<br>

<div id="header" align="center">
  <img src="examples/watermark.gif"/>
</div>

<br>

### How to run

```
python main.py
```
