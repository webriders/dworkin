cd ..
cd apps/website
echo off
echo --------------------------------------------------
echo Make i18n messages
echo --------------------------------------------------
python ../../manage.py makemessages -l ru
python ../../manage.py makemessages -l en
python ../../manage.py makemessages -l uk

