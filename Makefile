prod:
	@echo "Installing python & requirments... for Hasker installation"
	@sleep 2
	@mkdir -p /etc/nginx/site-available
	@cp -f conf/nginx/nginx-hasker.conf /etc/nginx/site-available
	@docker compose up -d
	@docker rm $(sudo docker stop $(sudo docker ps -a -q --filter="name=hasker_backend" --format="{{.ID}}")) || true
	@docker rmi $(sudo docker images -a -q --filter="reference=hasker_backend" --format="{{.ID}}") || true
	@docker build -t hasker_image .
	@docker run -d --restart on-failure --net stckvflw_vpcbr --ip 10.88.64.5 -p 8000:8000 -v /home/app/hasker/static/:/home/app/hasker/static/ --name hasker_backend hasker_image
	@sleep 2
	@echo 'whait a minute...'
