prod:
	@echo "Installing python & requirments... for Hasker installation"
	@sleep 2
	@mkdir -p /etc/nginx/site-available
	@mkdir -p /home/hasker/uwsgi
	@cp -f conf/nginx/nginx-hasker.conf /etc/nginx/site-available
	@cp -f conf/uwsgi/* /home/hasker/uwsgi
	@docker compose up -d
	@docker rm $(sudo docker stop $(sudo docker ps -a -q --filter="name=hasker_backend" --format="{{.ID}}")) || true
	@docker rmi $(sudo docker images -a -q --filter="reference=hasker_backend" --format="{{.ID}}") || true
	@docker build -t hasker_image .
	@docker run -d --restart on-failure --net hasker --ip 10.88.64.5 -p 8000:8000 -v /var/log/hasker/:/var/log/hasker/ -v /home/hasker/media/:/home/hasker/hasker/media/ -v /home/hasker/uwsgi:/home/hasker/uwsgi  --name hasker_backend hasker_image
	@sleep 2
	@echo 'whait a minute...'
