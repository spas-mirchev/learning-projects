# Cafe Workspace app

This is a simple cafe workspace app that shows coffee shops on an interactive map.

It uses SQLite database.

In order to add cafes or update them, the user would have to register then login.

The user can also select the following features of the cafes:
- has WiFi
- has sockets
- has toilet
- can take calls

When selected, an icon appears on the cafe card.

The application uses Flask, SQLAlchemy, Flask-Login, Flask-Bootstrap and Werkzeug for password hashing. It also uses [LeafletJS](https://leafletjs.com/) to handle the map interactivity. When clicking on the pins on the map, a preview of the cafe comes up in a pop-up.

  
## Installation

``` terminal
# Create an environment variable
python -m venv .env

python -m venv .env

source .env/bin/activate 

# Run the app

python app.py 
```


<div id="header" align="center">
  <img src="./../../Assets/cafes.gif"/>
</div>



