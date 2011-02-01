cd ..
echo off
echo --------------------------------------------------
echo Create south managed database (only at project start)
echo --------------------------------------------------
python manage.py schemamigration investor --initial
python manage.py schemamigration blog --initial
python manage.py schemamigration production --initial
python manage.py schemamigration products --initial
python manage.py schemamigration public_relations --initial
python manage.py syncdb --migrate
