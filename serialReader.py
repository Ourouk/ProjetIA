import serial
import csv
import os
import time

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

            # File handlers for each infoType
            file_handlers = {}

            while True:
                if ser.in_waiting > 0:
                    # Read and decode one character
                    line = ser.readline().decode('utf-8', errors='ignore').strip()

                    if not line:
                        continue

                    # Parse the line
                    try:
                        info_type, timestamp, amplitude = line.split(',')

                        # Ensure CSV file exists for this infoType
                        if info_type not in file_handlers:
                            timestamp = time.strftime("%Y%m%d_%H%M%S")
                            filename = f"{info_type}_{timestamp}.csv"
                            new_file = not os.path.exists(filename)
                            file_handlers[info_type] = open(filename, mode='a', newline='')
                            csv_writer = csv.writer(file_handlers[info_type])

                            # Write headers if the file is new
                            if new_file:
                                csv_writer.writerow(["Timestamp", "Amplitude"])

                        # Write data row to the corresponding file
                        csv_writer = csv.writer(file_handlers[info_type])
                        csv_writer.writerow([timestamp, amplitude])

                        print(f"Data written to {info_type}.csv: {timestamp}, {amplitude}")

                    except ValueError:
                        print(f"Invalid data format: {line}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStream processing stopped.")
    finally:
        # Close all file handlers
        for fh in file_handlers.values():
            fh.close()
        print("All files closed.")

if __name__ == "__main__":
    # Specify your port and other parameters
    serial_port = "/dev/ttyACM0"
    baud_rate = 115200

    # Start processing
    parse_and_save_serial_data(serial_port, baudrate=baud_rate)