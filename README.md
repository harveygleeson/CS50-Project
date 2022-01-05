# EZ·DJ
#### Video Demo:  https://youtu.be/x90Kq50cqTc
#### Description:  

Reminder:
export SPOTIPY_CLIENT_ID='xxx'
export SPOTIPY_CLIENT_SECRET="xxx"
export FLASK_APP=application.py
flask run    


EZ·DJ is a web app that allows users to make song requests to a dj, or to host their own event
which can take on requests from other users

The web app is made using flask framework, with static and template folders, application and helpers python files,
a project.db sqlite3 database and a requirements file.

The static folder contains one javascript file and the stylesheet in css.
The js file posts the song id of the requested song from the search page to the host page for a specific location
The stylesheet contains all of the styles used for the html templates

The templates folder contains 10 HTML templates. The layout file contains layout information
with the desired conditions for all the templates except for the welcome page, which is kept quite plain,
with just a login and register button in the center of the page and a small link to the about section at the bottom

The remaining templates are the about template (which gives information on the web app),
the host and hosting templates (which allow the user to host an event or view songs requested to the event they are hosting),
the index page which simply displays what hosting locations are available to request a song at,
the login and register pages take user credentials and put them in the db or check if they are already in the db,
the search and search pages query the spotify api for songs and display a list of searched songs.

The helpers py file contains all the necessary functions to be used in the application file.
These are the search song functions by id and name, and the login required wrapper to define which routes can be
viewed

The application py file has all the routes for the web app, to each of the templates as described above.
The routes support get and post methods, for displaying html pages and for posting song, user and location information
to and from the spotify api and project database.

The requirements file has all the necessary imports
