# Makefile for the django project.
#

prod:
	@echo "Installing python & requirments... for Hasker installation"
	@sleep 2
	@mkdir -p /etc/nginx/site-available
	@cp -f conf/nginx/nginx-hasker.conf /etc/nginx/site-available
	@docker build -t hasker_image .
	@docker run -d --restart always --ip 10.88.64.5 -p 8000:8000 --name hasker_backend hasker_image
	@docker compose up -d
	@docker compose exec hasker_db python manage.py migrate
	@docker compose exec hasker_db python manage.py runserver