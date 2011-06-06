cd ..
echo off
echo --------------------------------------------------
echo Create migrations if they are 
echo --------------------------------------------------
python manage.py schemamigration techblog --auto
