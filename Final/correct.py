#import imu
#import time

#while True:
#    x,y,z = imu.acceleration_mg()
#    print("Accel: (m/s^2): ", x, y, z)
#    time.sleep_ms(1000)

#import imu  # Make sure this is the correct module name for your sensor
#import time

# Example initialization (if needed; adjust according to your setup)
# imu.init()  # Uncomment and adjust if initialization is required

#while True:
#    try:
#        # Read acceleration data
#        x, y, z = imu.acceleration_mg()

#        # Ensure x, y, z are in the expected format (e.g., floats or integers)
#        print(f"Accel: (mg): x={x:.2f} mg, y={y:.2f} mg, z={z:.2f} mg")

#    except TypeError as e:
#        print(f"TypeError: {e}. Check if the imu.acceleration_mg() returns values in the correct format.")
#    except Exception as e:
#        print(f"An error occurred: {e}")

#    time.sleep_ms(1000)  # Delay for 1 second

#import imu
#import time

## Conversion factor from mg to m/s^2
#MG_TO_MS2 = 9.80665 / 1000

#while True:
#    x, y, z = imu.acceleration_mg()

#    # Convert from mg to m/s^2
#    x_ms2 = x * MG_TO_MS2
#    y_ms2 = y * MG_TO_MS2
#    z_ms2 = z * MG_TO_MS2

#    print('Accelerometer (m/s^2):', x_ms2, y_ms2, z_ms2)
#    time.sleep_ms(1000)


#import imu  # Import the module for accessing accelerometer data
#import time  # Import the time module for delays

## Conversion factor from milligrams (mg) to meters per second squared (m/s²)
#MG_TO_MS2 = 9.80665 / 1000

#while True:
#    try:
#        # Read acceleration data in milligrams
#        x, y, z = imu.acceleration_mg()

#        # Convert from mg to m/s²
#        x_ms2 = x * MG_TO_MS2
#        y_ms2 = y * MG_TO_MS2
#        z_ms2 = z * MG_TO_MS2

#        # Print acceleration data in m/s² with labels
#        print(f'x = {x_ms2:.2f} m/s², y = {y_ms2:.2f} m/s², z = {z_ms2:.2f} m/s²')

#    except Exception as e:
#        print(f"An error occurred: {e}")

#    # Delay for 1 second
#    time.sleep_ms(1000)


import imu  # Import the module for accessing accelerometer data
import time  # Import the time module for delays

# Conversion factor from milligrams (mg) to meters per second squared (m/s²)
MG_TO_MS2 = 9.80665 / 1000

def average_readings(num_samples=10):
    x_sum, y_sum, z_sum = 0, 0, 0
    for _ in range(num_samples):
        x, y, z = imu.acceleration_mg()
        x_sum += x
        y_sum += y
        z_sum += z
        time.sleep_ms(100)  # Short delay between samples
    return x_sum / num_samples, y_sum / num_samples, z_sum / num_samples

while True:
    try:
        # Average over a number of samples
        x_avg, y_avg, z_avg = average_readings()

        # Convert from mg to m/s²
        x_ms2 = x_avg * MG_TO_MS2
        y_ms2 = y_avg * MG_TO_MS2
        z_ms2 = z_avg * MG_TO_MS2

        # Print average acceleration data in m/s² with labels
        print(f'x = {x_ms2:.2f} m/s², y = {y_ms2:.2f} m/s², z = {z_ms2:.2f} m/s²')

    except Exception as e:
        print(f"An error occurred: {e}")

    # Delay for 1 second
    time.sleep_ms(1000)

#import imu
#import time

## Conversion factor from milligrams (mg) to meters per second squared (m/s²)
#MG_TO_MS2 = 9.80665 / 1000

## Smoothing factor (0 < alpha < 1)
#alpha = 0.1

## Initialize smoothed values
#x_smooth, y_smooth, z_smooth = 0, 0, 0

#while True:
#    try:
#        # Read acceleration data
#        x, y, z = imu.acceleration_mg()

#        # Convert from mg to m/s²
#        x_ms2 = x * MG_TO_MS2
#        y_ms2 = y * MG_TO_MS2
#        z_ms2 = z * MG_TO_MS2

#        # Smooth the readings
#        x_smooth = alpha * x_ms2 + (1 - alpha) * x_smooth
#        y_smooth = alpha * y_ms2 + (1 - alpha) * y_smooth
#        z_smooth = alpha * z_ms2 + (1 - alpha) * z_smooth

#        # Print smoothed acceleration data
#        print(f'x = {x_smooth:.2f} m/s², y = {y_smooth:.2f} m/s², z = {z_smooth:.2f} m/s²')

#    except Exception as e:
#        print(f"An error occurred: {e}")

#    # Delay for 1 second
#    time.sleep_ms(1000)

