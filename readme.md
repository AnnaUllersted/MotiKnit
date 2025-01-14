This app runs using flask.
In production mode it will redirect all calls from http to https.
In order to avoid this during local development create a ´.env´ file at root level and add ´FLASK_ENV=development´ to it.
This file will set a local enviroment variable indicating the development enviroment.
This file will be ignored by git.

Commands to use:
to push master branch to git ´git push´

to start on local machine ´python app.py´



