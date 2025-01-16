import logging
import random
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_SENSOR
from flask import Flask, request, jsonify
from threading import Thread
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Initialize the global accessory variable
accessory = None
random_sensor = None  # Direct reference to the random temperature sensor

def get_cpu_temperature():
    """Reads the CPU temperature on a Linux system."""
    try:
        # Path to the file where the CPU temperature is stored
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read()) / 1000.0  # Convert millikelvins to Celsius
        return temp
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

class TemperatureSensor(Accessory):
    """Implementation of a mock temperature sensor accessory."""

    category = CATEGORY_SENSOR  # Set category for iOS Home app icon

    def __init__(self, driver, name):
        """Initialize the accessory and add the TemperatureSensor service."""
        super().__init__(driver, name)

        # Add TemperatureSensor service
        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        self.current_temperature = 0 # Inital temperature

    def temperature_changed(self, value):
        """Callback for temperature changes."""
        print('Temperature changed to: ', value)

    @Accessory.run_at_interval(3)  # Run this method every 3 seconds
    async def run(self):
        """Update the temperature every 3 seconds."""
        self.char_temp.set_value(self.current_temperature)

    def update_temperature(self, value):
        """Update the stored temperature."""
        self.current_temperature = value

    def stop(self):
        """Clean up resources when stopping the accessory."""
        print('Stopping accessory.')

@app.route('/update', methods=['POST'])
def update():
    """Endpoint to update the temperature from the Flask app."""
    global accessory
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        if temperature is not None and accessory:
            accessory.update_temperature(temperature)  # Update the stored temperature
            return jsonify(success=True), 200
        return jsonify(success=False, error="Temperature value is missing or accessory not initialized"), 400
    except Exception as e:
        app.logger.error(f'Error processing request: {e}')
        return jsonify(success=False, error="Internal server error"), 500

def get_accessory(driver):
    """Create and return a standalone TemperatureSensor accessory."""
    return TemperatureSensor(driver, 'MyTempSensor')

def get_bridge(driver):
    """Create and return a Bridge with multiple accessories."""
    bridge = Bridge(driver, 'Bridge')
    temp_sensor1 = TemperatureSensor(driver, 'Sensor 1')
    temp_sensor2 = TemperatureSensor(driver, 'Sensor 2')
    bridge.add_accessory(temp_sensor1)
    bridge.add_accessory(temp_sensor2)
    return bridge

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

    # Retrieve PIN code from .env file
    pincode = os.getenv('HAP_PIN')
    if not pincode:
        logging.error("HAP_PIN not found in .env file. Please set it before running the program.")
        sys.exit(1)  # Exit if PIN is not set

    driver = AccessoryDriver(port=51826, pincode=pincode.encode())

    # Create and add the accessory or bridge to the driver
    accessory_instance = get_accessory(driver)  # Use `get_bridge(driver)` if you want to use a Bridge
    driver.add_accessory(accessory_instance)

    # Set the global accessory variable
    accessory = accessory_instance

    # Start Flask server in a separate thread without debug mode
    def run_flask_app():
        app.run(host='0.0.0.0', port=8080, debug=False)  # Disable debug mode

    Thread(target=run_flask_app).start()

    # Start the accessory driver
    driver.start()
