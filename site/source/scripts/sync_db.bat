cd ..
echo off
echo --------------------------------------------------
echo Sync DB
echo --------------------------------------------------
python manage.py syncdb --migrate

