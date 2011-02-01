cd ..
echo off
echo --------------------------------------------------
echo Migrate database
echo --------------------------------------------------
python manage.py schemamigration website --auto --settings=settings
python manage.py migrate website --settings=settings
