from flask import render_template, Flask, request, redirect
from speedtest_cli import Speedtest
import os

speedtest = Speedtest()
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        create_env(request.form['server_name'], request.form['server_id'])
        restart_docker()
        return redirect(request.url)
    else:
        x = speedtest.get_closest_servers(100)
        servers_list = []
        for i in range(len(x)):
            servers_list.append(f"Operator: {x[i]['sponsor']} ----- ID Serwera: {x[i]['id']} ---- "
                                f"Dystans: {int(x[i]['d'])}km")
        return render_template('index.html', len=len(servers_list), servers=servers_list)

def create_env(server_name, server_id=None):
    os.remove('.env')
    text = f"GRAFANA_PORT=3000\nSPEEDTEST_SPEEDTEST_INTERVAL=15\nSPEEDTEST_HOST={server_name}\n" \
           f"SPEEDTEST_SERVER={server_id}"
    f = open('.env', 'w+')
    f.write(text)
    f.close()

def restart_docker():
    os.system("docker kill speedtest && docker kill grafana && docker kill influxdb")
    os.system("docker-compose up --build -d")