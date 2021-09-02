# Code architecture of the web app

## General

The web app was programmed in Python using Flask as web framework.

```run.py```

The run.py is used and needed to execute and start the web app in the container. The ip is set to *0.0.0.0.* to allow
connections from outside the container network.

```config.py```

This file is used to enable the debug functionality integrated in flask.

## /app folder

The /app folder resembles the default structure advocated by flask for multipage applications with split "frontend"
and "backend".

- ```static/``` contains assets like the css files and all necessary Javascript applets.
- ```templates/``` contains the Jinja3 templates for the app. The template name corresponds to the name (url) of the
  webpage.

**python files:**

- ```legerible.py``` includes all functions of the backend which is mostly functions concerning database connection and
  access.
- ```views.py``` is the central control file which is responsible for the page navigation and the provisioning of the
  web pages. Each pages is described in a function that uses select queries to return the jinja template with all
  contents .
- ```book.py``` is an outsourced class which methods are used to interact with books.
- ```kafka_messaging.py``` is an outsourced class that has the needed functionality to send messages through kafka.

## /database folder

The database folder has 2 files.

- The ```init.sql``` is a text file with which the postgres database is initialised
- The ```isbn.txt``` is a text file that is used during the first time initialization to add more books to the database
  from within the web app.