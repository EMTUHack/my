
# My Hack the Campus
Simple dashboard that provides tools to manage teams and hackers for hackathons

# Setup
### Quick deploy with Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploying locally
Install python 3.x

Create a venv

Install requirements
```
pip install -r requirements.txt
```

Create a copy of `.env.config` called `.env` and edit your variables

Build your database
```
python manage.py migrate
```

Create a superuser
```
python manage.py createsuperuser
```

Compile the SCSS
```
python manage.py compilescss
```

Start your server
```
python manage.py runserver
```

Your server will be available at
```
http://localhost:8000
```

# License
Released under AGPLv3. See [`LICENSE.txt`][license] for details.


# Credits
This app was extended upon [ehzhang's](https://github.com/ehzhang) [quill](https://github.com/techx/quill) by [maronato](https://github.com/maronato).

The original copyright remains for the modified files:
Copyright (c) 2015-2016 Edwin Zhang (https://github.com/ehzhang).
