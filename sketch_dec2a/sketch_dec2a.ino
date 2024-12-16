#define MAX_MILLIS 1000  // Maximum value for millis before it resets (e.g., 100,000 ms)
#define baudrate 115200
#define max_serial_message_size 11


int delay_time = 0;
void setup() {
  // Initialize serial communication
  Serial.begin(baudrate);
  delay_time = max_serial_message_size / (baudrate/10);
}

void loop() {
  // Iterate through analog pins A0 to A3
  for (int pin = A1; pin <= A1; pin++) {
    // Calculate custom wrapped millis
    unsigned long wrappedMillis = millis() % MAX_MILLIS;

    int analogValue = analogRead(pin);

    // Print pin number, epoch time, and analog value
    Serial.print(pin - A0);  // A0 is pin 14, A1 is 15, etc.
    Serial.print(",");
    Serial.print(millis());
    Serial.print(",");
    Serial.println(analogValue);

    // Add a delay to prevent overwhelming the serial monitor
    delay(delay_time);  // Adjust as needed
  }

  
}
