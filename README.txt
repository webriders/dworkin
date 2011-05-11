Requirements:
-------------
- Python 2.5+
- PIL
- pip
- virtualenv

Installation:
-------------
1. Create empty virtual environment:

        virtualenv --no-site-packages --distribute dworkin

2. Install all required libs via pip (use ./requirements.txt)

3. We are using `django.contrib.staticfiles` so you should run (once):

        python manage.py collectstatic # just once

4. Activate your _dworkin virtualenv_ and sync your DB:

        cd ./site/source/
        python manage.py syncdb # without --migrate
        python manage.py migrate

5. Run server