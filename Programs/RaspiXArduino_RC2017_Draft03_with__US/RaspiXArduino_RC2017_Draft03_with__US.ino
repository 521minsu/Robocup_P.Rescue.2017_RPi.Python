#define secondary A1
#include <NewPing.h>

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(secondary, INPUT);
}

void loop() {
  delay(50);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  int dist = sonar.ping_cm();
  if(dist == 0){
    dist = 300;
  } else if(dist != 0) {
    int secondaryVal = analogRead(secondary);
  
    Serial.print(secondaryVal);
    Serial.print(" , ");
    Serial.println(dist);
  }
}
