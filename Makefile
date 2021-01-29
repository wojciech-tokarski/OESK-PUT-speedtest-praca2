run:
	pip3 install -r requirements.txt
	docker-compose up --build -d
	export FLASK_APP=main.py
	flask run
kill:
	docker kill speedtest && docker kill grafana && docker kill influxdb
