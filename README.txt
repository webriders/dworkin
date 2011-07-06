Requirements:
-------------
- Python 2.5+
- PIL
- distribute
- pip
- virtualenv

Install requirements:
- Python: http://www.python.org/download/
- PIL:
  - for Windows: http://www.pythonware.com/products/pil/
  - for Ubuntu/Debian: sudo apt-get install python-imaging
- distribute: http://pypi.python.org/pypi/distribute
- pip: http://pypi.python.org/pypi/pip
- virtualenv: http://pypi.python.org/pypi/virtualenv

Installation:
-------------
1. Create empty virtual environment:
   virtualenv --no-site-packages --distribute dworkin
   ... and activate it!
2. Activate it before going further!
   - for Windows: dworkin/Scripts/activate.bat
   - for Linux: . dworkin/bin/activate # space between "." and "dworkin" is not a mistake
3. Install all required libs via pip (use ./requirements.txt):
   pip install -r requirements.txt
4. Copy apps static:
   - env/dworkin/.../site-packages/admin_tools/media/admin_tools -> ./site/static/ext/admin_tools
   - env/dworkin/.../site-packages/markitup/media/markitup -> ./site/static/ext/markitup
5. Sync and migrate DB:
   python manage.py syncdb # don't create superuser yet! Because UserProfile DB is not created yet (because it's on South)
   python manage.py migrate
6. Create superuser:
   python manage.py createsuperuser # on Windows it may be broken. In this case you'll have to create superuser manually
7. Run server!
   - dev: python manage.py runserver
   - prod: you know how to do it
8. Goto http://%Your_site%/admin/sites/site/ and change 'example.com' to %Your_site%
