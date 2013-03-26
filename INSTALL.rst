virtualenv . -no-site-packages
source bin/activate
python bootstrap.py
bin/buildout
cp bdpindex/settings_changeme.py bdpindex/settings.py # and edit as needed
bin/django syncdb
bin/django migrate
bin/django runserver
