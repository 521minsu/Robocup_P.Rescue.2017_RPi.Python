#include <NewPing.h>

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int distRaw = 0, dist = 0;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(9600);
}

void loop() {
  distRaw = sonar.ping_cm();
  
  if (distRaw == 0) dist = 300;
  else dist = distRaw;
  
  Serial.println(dist); // Send ping, get distance in cm and print result (0 = outside set distance range)
  delay(50); 
}
