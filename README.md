
# Base Weather App

The goal of this project is to demonstrate how to set up a simple application with three components:

1. A Python program using [`requests`](https://docs.python-requests.org/en/master/) to collect data.
2. The [redis](https://redis.io/) database to store data
3. A [Flask](https://flask.palletsprojects.com/en/2.0.x/) server launched via [gunicorn](https://gunicorn.org/) to server up the data.

The data used in this example is the current temperature in Bethlehem using data from the [WeatherAPI](https://www.weatherapi.com/).

The "application" modeled is intentionally minimal: Every 15 minutes, the collector obtains the current count and stores it in the redis database.  The Flask server has a single end point that allows a user to fetch this data.

## WeatherAPI Setup

To use this application you must [signup for a free WeatherAPI key](https://www.weatherapi.com/signup.aspx).

After you have signed up and confirmed your email, go to the [WeatherAPI Account page](https://www.weatherapi.com/my/) and copy your API key (near the top of the page).  To verify your API key, replace `<API_KEY>` in the following command:

```
curl "http://api.weatherapi.com/v1/current.json?q=18018&key=<API_KEY>"
```

If it succeeds, the output should be something like:

```
{"location":{"name":"Bethlehem","region":"Pennsylvania","country":"USA","lat":40.62,"lon":-75.41,"tz_id":"America/New_York","localtime_epoch":1710293264,"localtime":"2024-03-12 21:27"},"current":{"last_updated_epoch":1710292500,"last_updated":"2024-03-12 21:15","temp_c":12.2,"temp_f":54.0,"is_day":0,"condition":{"text":"Clear","icon":"//cdn.weatherapi.com/weather/64x64/night/113.png","code":1000},"wind_mph":5.6,"wind_kph":9.0,"wind_degree":240,"wind_dir":"WSW","pressure_mb":1010.0,"pressure_in":29.83,"precip_mm":0.0,"precip_in":0.0,"humidity":45,"cloud":0,"feelslike_c":11.7,"feelslike_f":53.1,"vis_km":16.0,"vis_miles":9.0,"uv":1.0,"gust_mph":9.4,"gust_kph":15.1}}
```


## System Architecture

![System Architecture](architecture.png)


# Setup

The following sections describe how to setup the system so it will
run *locally* (i.e. on your laptop).  For deployment on an EC2 
instance, see the sections in the [AWS section](#AWS) section.

## Collector Setup

In the `collector` folder:

* Create a virtual environment for the collector and install the required libraries:

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

* Create a file `.env` that contains the hostname and port number for Redis.  We will run Redis on our laptop (`localhost`) using the standard Redis port (6379).  Replace `<API_KEY>` with your WeatherAPI key:

  ```
  REDIS_HOST=localhost
  REDIS_PORT=6379
  API_KEY=<API_KEY>
  ```

## Redis Setup

* (If needed) Install [Homebrew](https://brew.sh/)

  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
  
* Install Redis on your system

  ```
  brew install redis
  ```
  
## Server Setup

In the `server` folder:

* Create a virtual environment for the collector and install the required libraries:

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

* Create a file `.env` that contains the hostname and port number for Redis.  We will run Redis on our laptop (`localhost`) using the standard Redis port (6379):

  ```
  REDIS_HOST=localhost
  REDIS_PORT=6379
  ```


## Launch the System (Local)

We will launch the system in three terminal windows:

* Terminal #1 (In the project root) Launch Redis:

  ```
  redis-server
  ```
  
* Terminal #2 (In the `collector` folder) Launch the collector:

  ```
  source .venv/bin/activate
  python collector.py
  ```
  
* Terminal #3 (In the `server` folder) Launch the server:

  ```
  source .venv/bin/activate
  python server.py
  ```
  
## Stop the System

In each terminal window, press ctrl-c to stop the program.


## AWS

Deploying on an EC2 instance is *mostly* the same.  The following sections document important differences.

### AWS Linux Version Issue

The collector uses the `requests` library which depends on the `urllib3` library, and the `urllib3` libraries utilizes the system-level SSL library.  AWS Linux 2 has an earlier version of SSL installed, which will cause the `urllib3` library to fail with a version error.  There are three solutions:

* Downgrade to an earlier version of `requests`, one that utilizes an earlier version of `urllib3` which, in turn, allow for an earlier version of SSL.  Version `2.25.0` is confirmed to work.
* Update SSL to version 1.1.1+ (as indicated in the error). TBD how to do this...
* Use AWS Linux 2023, which has a newer version of SSL.

### Redis

On Amazon Linux 2, `redis` is not available via `yum`.  Instead, you must install it with `amazon-linux-extras`

One Amazon Linux 2023, you can install Redis via `yum`, but you must use `redis6`.  Afterward, the commands are `redis6-server` and `redis6-cli`.


## SystemD Services

When you install Redis (whether via `yum` or `amazon-linux-extras`), the package manager installs a service file automatically.  You can start `redis6` using:

```
sudo systemctl enable redis6
sudo systemctl start redis6
```

(use `redis` in both commands on AWS Linux 2)

The files `collector/weather_collector.service` and `server/weather_server.service` can be used to launch the collector and server.  For each:

* Copy the file to `/etc/systemd/system`
* Call `systemctl enable` on the service
* Call `systemctl start` on the service

