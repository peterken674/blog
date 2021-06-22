# Blogg
## Description
A Flask personal blogging website where you can create and share your opinions and other users can read and comment on them. 

## Setup/Installation
On your terminal, clone the project.
    
    $ git clone git@github.com:peterken674/blog.git

Navigate into the cloned project.

    $ cd blog

Create a `start.sh` file.

    $ touch start.sh

Inside `start.sh`, addv the following. The email will be used to send welcome emails to new users who sign up, Gmail is recommended.

```bash
#!/bin/sh
export FLASK_ENV=development
export MAIL_USERNAME=<YOUR_EMAIL>
export MAIL_PASSWORD=<EMAIL_PASSWORD>
export SECRET_KEY=<SECRET_KEY>

python3 manage.py server
```

Create the virtual environment and install the requirements from `requirements.txt`

    $ python3 -m venv virtual
    $ . virtual/bin/activate
    $ pip install -r requirements.txt

Give the `start.sh` file execution permissions.

    $ chmod a+x start.sh

Run the program.

    $ ./start.sh
## Known Bugs
- Creating new post causes the app to crash even though the post is creaated. Working on it.
## Technologies Used
- Flask(Python)
- Jinja2
- Unittest
## Support and contact details
If you have any suggestions, questions or in case of a fire, you can reach the developer via [email](mailto:peterken.ngugi@gmail.com).
### License
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Copyright &copy; 2021 **[peterken674](www.github.com/peterken674)**