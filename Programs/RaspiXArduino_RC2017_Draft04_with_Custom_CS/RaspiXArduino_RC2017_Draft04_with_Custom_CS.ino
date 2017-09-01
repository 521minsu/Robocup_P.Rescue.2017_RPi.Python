#include <SharpIR.h>
#define ir A1
#define left_CS A2
#define right_CS A0
#define model 1080
SharpIR SharpIR(ir, model);

int dist = 0, distsum = 0, distcal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(left_CS, INPUT);
  pinMode(right_CS,INPUT);
}

void loop() {
  int dist = SharpIR.distance();  // this returns the distance to the object you're measuring
  int left_CS_Val = analogRead(left_CS);
  int right_CS_Val = analogRead(right_CS);
  
//left_CS_Val += 0;  //Calibrate if required
  right_CS_Val += 60;  //Calibration to match both sensor's value
  
  Serial.print(dist);
  Serial.print(" , ");
  Serial.print(left_CS_Val);
  Serial.print(" , ");
  Serial.println(right_CS_Val);
}
