flake8 --ignore=E126 --ignore=W391 --statistics --exclude=submodules,migrations,build . &&
coverage run --source="server_status" manage.py test -v 2 --traceback --failfast --settings=server_status.tests.settings --pattern="*_tests.py" &&
coverage html -d coverage --omit="*__init__*,*/settings/*,*/migrations/*,*/tests/*,*admin*"
