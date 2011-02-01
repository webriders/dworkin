cd ..
echo off
echo --------------------------------------------------
echo Create migrations if they are 
echo --------------------------------------------------
python manage.py schemamigration investor --auto
python manage.py schemamigration blog --auto
python manage.py schemamigration production --auto
