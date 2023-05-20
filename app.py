from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
# Replace with your DHT11 sensor pin number
DHT_PIN = 4
# MQTT broker details
MQTT_SERVER = "165.73.249.219"
MQTT_PORT = 1883
MQTT_TEMP_TOPIC = "nodemcu/temperature"
MQTT_HUMIDITY_TOPIC = "nodemcu/humidity"
LED_TOPIC = "nodemcu/led"

app = Flask(__name__)

# Define MQTT client and connect to the broker
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_SERVER, MQTT_PORT)
# Define global variables to store current temperature and humidity values
current_temperature = None
current_humidity = None

# Define a callback function to handle MQTT messages and update the temperature and humidity values
def on_message(client, userdata, message):
    global current_temperature, current_humidity
    if message.topic == MQTT_TEMP_TOPIC:
        current_temperature = float(message.payload)
    elif message.topic == MQTT_HUMIDITY_TOPIC:
        current_humidity = float(message.payload)

# Set the callback function and connect to the MQTT broker
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_SERVER, MQTT_PORT)
mqtt_client.subscribe([(MQTT_TEMP_TOPIC, 0), (MQTT_HUMIDITY_TOPIC, 0)])
mqtt_client.loop_start()

# Define the Flask route to handle button clicks
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the LED value from the button that was clicked
        led = request.form['led']
        # Publish the LED value to the MQTT broker
        mqtt_client.publish(LED_TOPIC, led)
    # Render the HTML template with the button
    return render_template('index.html')

# Define the route to get the current temperature and humidity values
@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify({'temperature': current_temperature, 'humidity': current_humidity})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
