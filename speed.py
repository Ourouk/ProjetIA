import csv
import statistics
import matplotlib.pyplot as plt
import argparse

# Hall sensor threshold
hallsensor_treshold = 150

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process a CSV file of hall sensor readings.")
parser.add_argument('csv_file_path', type=str, help="Path to the CSV file")
args = parser.parse_args()

# Path to the CSV file
csv_file_path = args.csv_file_path

# Open the CSV file
try:
    with open(csv_file_path, 'r') as csv_file:
        print(f"Opening CSV file: {csv_file_path}")

        # Create a CSV reader object
        csv_reader = csv.reader(csv_file)

        # Skip the header line
        header = next(csv_reader, None)
        print(f"CSV header: {header}")

        hall_ping_delta_time = []
        last_hall_sensor_reading = 0

        # Loop through each line in the CSV file
        for line in csv_reader:
            if len(line) < 2:
                print(f"Skipping malformed line: {line}")
                continue

            try:
                timestamp = line[0]
                hall_sensor_reading = line[1]

                if int(hall_sensor_reading) < hallsensor_treshold:
                    print(f"Hall sensor reading below threshold ({hallsensor_treshold}): {hall_sensor_reading} at timestamp {timestamp}")

                    if last_hall_sensor_reading != 0:
                        # Calculate the time difference
                        delta_time = int(timestamp) - int(last_hall_sensor_reading)
                        hall_ping_delta_time.append(delta_time)
                        print(f"Added time difference: {delta_time}")

                    last_hall_sensor_reading = int(timestamp)  # Update the last reading

            except ValueError as e:
                print(f"Error processing line {line}: {e}")

        # Remove outliers and double readings
        if hall_ping_delta_time:
            print("Calculating interquartile range (IQR) to remove outliers...")
            q1 = statistics.quantiles(hall_ping_delta_time, n=4)[0]
            q3 = statistics.quantiles(hall_ping_delta_time, n=4)[2]
            iqr = q3 - q1
            lower_bound = q1 - 1.25 * iqr
            if lower_bound <= 2:
                lower_bound = 2
            upper_bound = q3 + 1.25 * iqr
            print(f"IQR calculated. Q1: {q1}, Q3: {q3}, Lower bound: {lower_bound}, Upper bound: {upper_bound}")

            hall_ping_delta_time = [x for x in hall_ping_delta_time if lower_bound <= x <= upper_bound]
            print(f"Filtered delta times: {len(hall_ping_delta_time)} valid entries remain.")

            # Calculate and print statistics
            if hall_ping_delta_time:
                median_value = statistics.median(hall_ping_delta_time)
                mean_value = statistics.mean(hall_ping_delta_time)
                stdev_value = statistics.stdev(hall_ping_delta_time)
                min_value = min(hall_ping_delta_time)
                max_value = max(hall_ping_delta_time)

                print(f"Median time difference: {median_value}")
                print(f"Mean time difference: {mean_value}")
                print(f"Standard deviation time difference: {stdev_value}")
                print(f"Min time difference: {min_value}")
                print(f"Max time difference: {max_value}")

                # Plot the histogram
                plt.hist(hall_ping_delta_time, bins=100)
                plt.title("Histogram of Hall Ping Delta Times")
                plt.xlabel("Time Difference")
                plt.ylabel("Frequency")

                plt.show()

            else:
                print("No valid hall ping delta time values found after processing.")

except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
