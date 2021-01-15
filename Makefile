install:
	pip install -r requirements/dev.txt

test:
	PYTHONPATH=".:tests:$PYTHONPATH" django-admin.py test core --settings=settings