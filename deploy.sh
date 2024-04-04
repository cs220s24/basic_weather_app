if [ ! -f collector/.env ]; then
    echo "Create collector/.env before deploying"
    exit
fi

if [ ! -f server/.env ]; then
    echo "Create server/.env before deploying"
    exit
fi

sudo yum install -y redis6
sudo systemctl enable redis6
sudo systemctl start redis6
python3 -m venv collector/.venv
collector/.venv/bin/pip install -r collector/requirements.txt
sudo cp collector/weather_collector.service /etc/systemd/system
sudo systemctl enable weather_collector
sudo systemctl start weather_collector
python3 -m venv server/.venv
server/.venv/bin/pip install -r server/requirements.txt
sudo cp server/weather_server.service /etc/systemd/system
sudo systemctl enable weather_server
sudo systemctl start weather_server

