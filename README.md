# WeatherStationSmartHomeServer
Backend server built with Flask and docker for a weather station (e.g., Pico W), integrated with the Apple HomeKit smart home system.

# To run this app:
1. git clone https://github.com/Fluorky/WeatherStationSmartHomeServer.git
2. Go to WeatherStationSmartHomeServer folder
3. Create and run virtual venv using these commands in cmd 

***Windows***

**py -3 -m venv venv**

**.\\venv\\Scripts\\activate**

***macOS or Linux***

**python3 -m venv venv**

**source ./venv/bin/activate**

4.  Use this command to install requirements packages:

**pip install -r requirements.txt**


5. To run app write in cmd

**python app.py**

6. Use this address yourIPAddress:8000 with url patch to integrate with API,for example: ***http://127.0.0.1:8000/update/***
If you want to check it before, you should use postman, curl or browser.


# Alternate you can use docker

1. Build a Docker image:
In the terminal, while in the project directory, run this command to build a Docker image:

docker-compose build

2. Start the application:
In the terminal, while in the project directory, run this command to run a Docker image:

docker-compose up