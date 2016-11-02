make= @$(MAKE) --no-print-directory

run:
	python manage.py runserver 0.0.0.0:8040