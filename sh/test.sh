set -v

/usr/bin/env python ./manage.py test -v 2

pep8 ./trains/
