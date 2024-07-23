import sensor, image, time, os, tf, math, uos, gc, json
import network, urequests
import pyb
import ubinascii
import random
import ntptime
from machine import Pin
import imu
ledBlue = pyb.LED(3)
# Wi-Fi connection details
SSID = ""
PASSWORD = ""
MAX_WIFI_RETRIES = 6  # Maximum number of retries for Wi-Fi connection
RETRY_DELAY = 1  # Delay between retries in seconds

SIMULATION_MODE = False

# Initialize the NIC (network interface controller)
nic = network.WLAN(network.STA_IF)
nic.active(True)

# Attempt Wi-Fi connection
def connect_wifi(SSID, PASSWORD, max_retries=MAX_WIFI_RETRIES):
    nic.connect(SSID, PASSWORD)
    retries = 0
    while not nic.isconnected() and retries < max_retries:
        print("Connecting to Wi-Fi...")
        time.sleep(RETRY_DELAY)
        retries += 1
    return nic.isconnected()

if connect_wifi(SSID, PASSWORD):
    ledBlue.on()
    pyb.delay(5)
    ledBlue.off()
    print("Connected to Wi-Fi")
    print(nic.ifconfig())

    try:
        ntptime.settime()
        print("Time synchronized with NTP server")
    except Exception as e:
        print("Failed to synchronize time with NTP server:", e)
else:
    print("Failed to connect to Wi-Fi within the maximum retry period.")

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.skip_frames(time=2000)

net = None
labels = None
min_confidence = 0.5
#ledRed = Pin("D3", Pin.OUT_PP, Pin.PULL_NONE)
ledRed=pyb.LED(1)
ledGreen = pyb.LED(2)
buzzer = Pin('D2', Pin.OUT_PP)

try:
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

last_five_predictions = []

def generate_unique_car_id():
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    random_number = random.randint(1000, 9999)
    return f"{mac}-{random_number}"

def format_time(time_tuple):
    return f"{time_tuple[0]:04}-{time_tuple[1]:02}-{time_tuple[2]:02} {time_tuple[3]:02}:{time_tuple[4]:02}:{time_tuple[5]:02}"

def save_data_locally(data):
    try:
        with open('drowsiness_log.txt', 'a') as f:
            f.write(json.dumps(data) + '\n')
        print("Data saved locally")
    except Exception as e:
        print(f"Failed to save data locally: {e}")

def send_data(data, retry_count=1, delay_seconds=1):
    while retry_count > 0:
        try:
            response = urequests.post('http://4.221.193.165:5000/data', json=data)
            if response.status_code == 200:
                print("Data sent to backend successfully")
                return True
            else:
                print(f"Failed to send data. Response code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send data: {e}")

        retry_count -= 1

    # Save data locally if sending failed
    save_data_locally(data)
    print("Failed to send data after retries, saved locally")
    return False

def send_locally_stored_data():
    try:
        with open('drowsiness_log.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line.strip())
                if not send_data(data):
                    print("Failed to send locally stored data")
                    return False
        print("All locally stored data sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send locally stored data: {e}")
        return False

def clear_local_storage():
    try:
        with open('drowsiness_log.txt', 'w') as f:
            f.write("")
        print("Local storage cleared")
    except Exception as e:
        print(f"Failed to clear local storage: {e}")

def check_internet_connection():
    try:
        urequests.get('http://www.google.com', timeout=1)
        return True
    except Exception:
        return False

# Generate car_id once
car_id = generate_unique_car_id()

# Track the uptime
start_time = time.time()

drowsy_start_time = None
buzzer_delay = 5

clock = time.clock()

MG_TO_MS2 = 9.80665 / 1000

# Threshold for determining if the vehicle is moving (adjust as needed)
MOVEMENT_THRESHOLD = 0.5

# Function to calculate the total acceleration
def get_total_acceleration(x, y, z):
    return (x**2 + y**2 + z**2) ** 0.5

def get_simulated_acceleration():
    # Simulate acceleration values for a moving car
    return random.uniform(0.5, 1.5), random.uniform(0.5, 1.5), random.uniform(9.2, 10.2)

while True:
    clock.tick()
    img = sensor.snapshot()
    current_prediction = None
    current_confidence = 0

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if i == 0:
            continue
        if len(detection_list) == 0:
            continue

        print(labels[i])
        current_prediction = labels[i]
        for d in detection_list:
            [x, y, w, h] = d.rect()
            img.draw_rectangle(x, y, w, h, color=colors[i], thickness=2)

    if current_prediction:
        last_five_predictions.append(current_prediction)
        if len(last_five_predictions) > 1:
            last_five_predictions.pop(0)

        # Read acceleration data in milligrams
        if SIMULATION_MODE:
            x_ms2, y_ms2, z_ms2 = get_simulated_acceleration()
        else:
            x, y, z = imu.acceleration_mg()
            # Convert from mg to m/s²
            x_ms2 = x * MG_TO_MS2
            y_ms2 = y * MG_TO_MS2
            z_ms2 = z * MG_TO_MS2

        # Calculate total acceleration
        total_acceleration = get_total_acceleration(x_ms2, y_ms2, z_ms2)

        # Check if the vehicle is moving or stationary
        if abs(total_acceleration - 9.8) > MOVEMENT_THRESHOLD:
            vehicle_moving = True
        else:
            vehicle_moving = False

        if all(pred == "Closed_Eye" for pred in last_five_predictions) and vehicle_moving:
            ledRed.on
            ledGreen.off()
            buzzer.value(1)
            pyb.delay(5)

            if not drowsy_start_time:
                drowsy_start_time = time.time()
            drowsiness_duration_seconds = time.time() - drowsy_start_time
            uptime_seconds = time.time() - start_time

            # Convert seconds to minutes
            drowsiness_duration_minutes = drowsiness_duration_seconds / 60
            uptime_minutes = uptime_seconds / 60

            data = {
                "car_id": car_id,
                "time_detected": format_time(time.localtime()),
                "drowsiness_state": "Drowsy",
                "contact": "0244567890",
                "drowsiness_duration_minutes": f"{drowsiness_duration_minutes:.2f}",
                "uptime_minutes": f"{uptime_minutes:.2f}"
            }
            print(data)
            send_data(data)
        else:
            ledGreen.on()
            ledRed.off()
            buzzer.value(0)
            print("non_drowsy")
            drowsy_start_time = None

    if check_internet_connection():
        if send_locally_stored_data():
            clear_local_storage()
