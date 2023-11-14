# Makefile for the django project.
#

prod:
	@echo "Installing python & requirments... for Hasker installation"
	@apt-get install -y build-essential \
		python3 \
		python3-dev \
		python3-pip
	@pip3 install --upgrade pip
	@pip3 install -r requirments.txt
	@mkdir -p /etc/nginx/site-available
	@cp -f nginx/nginx-hasker.conf /etc/nginx/site-available
	@docker-compose build -t hasker_image .
	@docker-compose run -d --restart on-failure 8000:8000 hasker_image
	@docker-compose up -d
	@docker-compose exec hasker_db python manage.py migrate
	@docker-compose exec hasker_db python manage.py runserver