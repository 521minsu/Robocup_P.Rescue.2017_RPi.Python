#include <SharpIR.h>
#define ir A1
#define customproxPin A2
#define model 1080
SharpIR SharpIR(ir, model);

int dist = 0, distsum = 0, distcal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(customproxPin, INPUT);
}

void loop() {
  int dist = SharpIR.distance();  // this returns the distance to the object you're measuring
  int customprox = analogRead(customproxPin);
  
  Serial.print(dist);
  Serial.print(" , ");
  Serial.println(customprox);
}
