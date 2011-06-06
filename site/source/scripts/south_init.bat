cd ..
echo off
echo --------------------------------------------------
echo Create south managed database (only at project start)
echo --------------------------------------------------
python manage.py schemamigration techblog --initial
