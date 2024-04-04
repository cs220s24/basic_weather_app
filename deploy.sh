sudo yum install redis6
sudo systemctl enable redis6
sudo systemctl start redis6
python3 -m venv collector/.venv
collector/.venv/bin/pip install -r collector/requirements.txt
sudo cp collector/weather_collector.service /etc/systemd/system
sudo systemctl enable weather_collector
sudo systemctl start weather_collector

