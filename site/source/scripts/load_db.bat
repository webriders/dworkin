cd ..
echo off
echo --------------------------------------------------
echo Load saved dump into db
echo --------------------------------------------------
REM python manage.py reset each_our_app
python manage.py loaddata website.json