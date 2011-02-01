cd ..
echo off
echo --------------------------------------------------
echo Dump data in json format
echo --------------------------------------------------
python manage.py dumpdata --format=json --indent=4 > apps/website/fixtures/website.json