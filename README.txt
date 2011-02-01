Requirements:
-------------
- Python 2.5+
- PIL
- pip
- virtualenv

Installation:
-------------
1. Create empty virtual environment:
   virtualenv --no-site-packages dworkin
2. Install all required libs via pip (use ./requirements.txt)
3. Copy apps static:
   env/dworkin/.../site-packages/admin_tools/media/admin_tools -> ./site/static/ext/admin_tools
   env/dworkin/.../site-packages/markitup/media/markitup -> ./site/static/ext/markitup
4. Activate dworkin virtualenv and run:
   cd ./site/source/
   python ./manage.py syncdb
   python ./manage.py migrate
5. Run server!