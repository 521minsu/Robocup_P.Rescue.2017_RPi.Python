#include <NewPing.h>

#define TRIGGER_PIN  12  // 
#define ECHO_PIN     11  // 
#define MAX_DISTANCE 300 // Maximum distance
const int s1 = A1, s2 = A2, s3 = A3, s4 = A4, s5 = A5, s6 = A6, s7 = A7;

int sRaw[8];
int sVal[8];
int arraybinary = 0;
int distRaw = 0, dist = 0;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); 

void setup() {
  pinMode(s1,INPUT);
  pinMode(s2,INPUT);
  pinMode(s3,INPUT);
  pinMode(s4,INPUT);
  pinMode(s5,INPUT);
  pinMode(s6,INPUT);
  pinMode(s7,INPUT);
  Serial.begin(9600);
}

void loop() {
  sRaw[0]=analogRead(s1);
  sRaw[1]=analogRead(s2);
  sRaw[2]=analogRead(s3);
  sRaw[3]=analogRead(s4);
  sRaw[4]=analogRead(s5);
  sRaw[5]=analogRead(s6);
  sRaw[6]=analogRead(s7);
  distRaw = sonar.ping_cm();
  
  if (distRaw == 0) dist = 300;
  else dist = distRaw;
  
  int IRthresh = 400;
  if(sRaw[0] < IRthresh) sVal[0] = 0; else sVal[0] = 1;
  if(sRaw[1] < IRthresh) sVal[1] = 0; else sVal[1] = 1;
  if(sRaw[2] < IRthresh) sVal[2] = 0; else sVal[2] = 1;
  if(sRaw[3] < IRthresh) sVal[3] = 0; else sVal[3] = 1;
  if(sRaw[4] < IRthresh) sVal[4] = 0; else sVal[4] = 1;
  if(sRaw[5] < IRthresh) sVal[5] = 0; else sVal[5] = 1;
  if(sRaw[6] < IRthresh) sVal[6] = 0; else sVal[6] = 1;
   
  Serial.print(dist);
  Serial.print(" , ");
  Serial.print(sVal[2]);
  Serial.print(" , ");
  Serial.print(sVal[4]);
  Serial.print(" , ");
  Serial.print(sVal[1]);
  Serial.print(" , ");
  Serial.print(sVal[5]);
  Serial.print(" , ");
  Serial.print(sVal[0]);
  Serial.print(" , ");
  Serial.println(sVal[6]);
  delay(50); 
}
