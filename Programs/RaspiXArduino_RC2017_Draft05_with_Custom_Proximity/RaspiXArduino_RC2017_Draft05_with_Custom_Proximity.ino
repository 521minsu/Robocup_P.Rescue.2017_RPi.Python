#include <SharpIR.h>
#define ir A1
#define customproxPin A2
#define model 1080
SharpIR SharpIR(ir, model);

int dist = 0, distsum = 0, distcal;
int customprox = 0, proxVal = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(customproxPin, INPUT);
}

void loop() {
  dist = SharpIR.distance();  // this returns the distance to the object you're measuring
  customprox = analogRead(customproxPin);
  
  if (customprox > 995) proxVal = 0;
  else proxVal = 1;
  
  Serial.print(dist);
  Serial.print(" , ");
  Serial.println(proxVal);
}
