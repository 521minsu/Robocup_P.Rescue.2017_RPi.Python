#include <SharpIR.h>
#define ir A1
#define secondary A0
#define model 1080
SharpIR SharpIR(ir, model);

int dist = 0, distsum = 0, distcal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(secondary, INPUT);
}

void loop() {
  int dist = SharpIR.distance();  // this returns the distance to the object you're measuring
  int secondaryVal = analogRead(secondary);
  
  Serial.print(secondaryVal);
  Serial.print(" , ");
  Serial.println(dist);
}
