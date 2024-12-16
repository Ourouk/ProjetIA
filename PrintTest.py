import serial
import csv
import os

def parse_and_save_serial_data(port, baudrate=9600, timeout=1):

    """
    Reads a continuous stream of formatted data from the serial port, parses it,
    and writes it into separate CSV files based on the infoType.

    Format of data: infoType,timestamp,amplitude
    Example: "temperature,2023-12-04T10:00:00,23.5"

    :param port: Serial port (e.g., COM3 or /dev/ttyUSB0)
    :param baudrate: Baud rate for the serial connection
    :param timeout: Timeout for serial read
    """
 
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"Connected to {port} at {baudrate} baud.")
            print("Press Ctrl+C to stop.")

            a = 0
            while True:
                if ser.in_waiting > 0:
                    # Read and decode one character
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    #print(line)
                    if not line:
                        continue

                    # Parse the line
                    try:
                        info_type, timestamp, amplitude = line.split(',')
                        if(info_type == "2" or info_type == "3"):
                            a = a + 1
                            a = a % 2
                            if(a == 0):
                                print(f"{amplitude},",end="")
                            else:
                                print(f"{amplitude}")
                    except ValueError:
                        print(f"Invalid data format: {line}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStream processing stopped.")

if __name__ == "__main__":
    # Specify your port and other parameters
    serial_port = "/dev/ttyACM0"
    baud_rate = 115200

    # Start processing
    parse_and_save_serial_data(serial_port, baudrate=baud_rate)
    