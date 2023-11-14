# Makefile for the django project.
#

prod:
	@echo "Installing python & requirments... for Hasker installation"
	@sleep 2
	@mkdir -p /etc/nginx/site-available
	@cp -f nginx/nginx-hasker.conf /etc/nginx/site-available
	@docker-compose build -t hasker_image .
	@docker-compose run -d --restart on-failure --ip 10.99.0.5 -p 8000:8000 hasker_image
	@docker-compose up -d
	@docker-compose exec hasker_db python manage.py migrate
	@docker-compose exec hasker_db python manage.py runserver