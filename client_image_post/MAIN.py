import machine
import utime as time 
import network
from umqtt.simple import MQTTClient
from machine import UART

# MQTT Broker configuration
mqtt_broker = "test.mosquitto.org"
mqtt_topic = b"send_data" 
mqtt_client_id = "mqtt-explorer-3b39faf0zzzszzz" 

# GSM module configuration
uart = UART(1, baudrate=9600, tx=4, rx=5, timeout=10) # Assuming GSM module is connected to UART1
gsm_command_delay = 500
gps_uart = machine.UART(1, baudrate=9600, tx=8, rx=9)
# GSM module initialization commands
gsm_init_commands = [
    b'AT+CMGF=1\r\n',  # Set SMS text mode
    b'AT+CNMI=2,2,0,0,0\r\n',  # Set SMS receive mode
]
def read_gps():
    gps_uart.write(b'AT+CGNSINF\r\n')  # Command to get GPS info
    time.sleep(1)  # Wait for response
    response = gps_uart.read(1024)
    if response is not None:
        try:
            return response.decode()  # Read response
        except UnicodeError as e:
            print("Unicode error while decoding GPS response:", e)
            return None
    else:
        return None
# Function to send SMS
def extract_location(response):
    # Parse GPS data from response (Example, actual parsing depends on GPS module)
    # Extract latitude and longitude
    data = response.split(',')
    latitude = data[3]
    longitude = data[4]
    return latitude, longitude

def create_google_maps_link(latitude, longitude):
    return "https://maps.google.com/?q={},{}".format(latitude, longitude)
def send_sms(message):
    uart.write("AT+CMGS=\"+918667517648\"\r\n")  # Replace +1234567890 with your phone number
    time.sleep_ms(gsm_command_delay)
    uart.write(message)
    time.sleep_ms(gsm_command_delay)
    uart.write(bytes([26]))  # Ctrl+Z to send SMS
    time.sleep_ms(gsm_command_delay)
    print("message sent")
# Callback function for MQTT message received

def mqtt_callback(topic, msg):
    print("Received MQTT message:", msg)
    send_sms(msg)

# Connect to MQTT broker
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("madhavan", "madhavan27,64")

while not wifi.isconnected():
    pass

print("Connected to WiFi")

client = MQTTClient(mqtt_client_id, mqtt_broker)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(mqtt_topic)

print("Connected to MQTT Broker")

# Send initialization commands to GSM module
for cmd in gsm_init_commands:
    uart.write(cmd)
    time.sleep_ms(gsm_command_delay)

# Main loop to wait for MQTT messages
try:
    while True:
        client.check_msg()
        gps_data = read_gps()
    
        if gps_data is not None:
            latitude, longitude = extract_location(gps_data)
            location_link = create_google_maps_link(latitude, longitude)
            
            # Send the location link via SMS
            sms_message = "Check my location: {}".format(location_link)
            send_sms(sms_message)
        else:
            print("no  gps data")
        time.sleep(1)
finally:
    client.disconnect()

