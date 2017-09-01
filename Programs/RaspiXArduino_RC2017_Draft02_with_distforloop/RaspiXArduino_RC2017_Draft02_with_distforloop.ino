#include <SharpIR.h>
#define ir A0
#define secondary A1
#define model 1080
SharpIR SharpIR(ir, model);

int dist = 0, distsum = 0, distcal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(secondary, INPUT);
}

void loop() {
  int secondaryVal = analogRead(secondary);
  for(int i=0;i>=30;i++) {
      dist = SharpIR.distance();  // this returns the distance to the object you're measuring
      distsum += dist;
  } distcal = distsum/30; distsum = 0;
  
  Serial.print(secondaryVal);
  Serial.print(" , ");
  Serial.println(distcal);
}
