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
                
  arraybinary = sVal[0] + (sVal[1]*2) + (sVal[2]*4) + (sVal[3]*8) + (sVal[4]*16)
                + (sVal[5]*32) + (sVal[6]*64);

  int Lspeed = 0, Rspeed = 0;
  //Sensor 1, 7 //
  if (sVal[0] == 1){
    Lspeed = -100;
    Rspeed = 100;
  } else if (sVal[0] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  } if (sVal[6] == 1) {
    Lspeed = 100;
    Rspeed = -100;
  } else if (sVal[6] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  }
  //Sensor 2,6 //
  if (sVal[1] == 1){
    Lspeed = -50;
    Rspeed = 90;
  } else if (sVal[1] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  } if (sVal[5] == 1) {
    Lspeed = 90;
    Rspeed = -50;
  } else if (sVal[5] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  }
  //Sensor 3, 5 // 
  if (sVal[2] == 1){
    Lspeed = -30;
    Rspeed = 100;
  } else if (sVal[2] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  } if (sVal[4] == 1) {
    Lspeed = 100;
    Rspeed = -30;
  } else if (sVal[4] == 0) {
    Lspeed = 0;
    Rspeed = 0;
  }
    
    //  int SSpeed = 85,Straight = 100;
//  switch(arraybinary) {
//    case 1  : Lspeed = -100;        Rspeed = 100;            break;   //(1,0,0,0,0,0,0);   //Left
//    case 2  : Lspeed = -SSpeed;     Rspeed = SSpeed;                 break;   //(0,1,0,0,0,0,0);   //Left
//    case 3  : Lspeed = -100;        Rspeed = 100;                    break;   //(1,1,0,0,0,0,0);   //Left
//    case 4  : Lspeed = -30;         Rspeed = SSpeed;                 break;   //(0,0,1,0,0,0,0);   //Left
//    case 6  : Lspeed = -80;         Rspeed = SSpeed;                 break;   //(0,1,1,0,0,0,0);   //Left
//    case 12 : Lspeed = 50; Rspeed = SSpeed;                 break;   //(0,0,1,1,0,0,0);   //Left
//    case 13 : Lspeed = SSpeed - 20; Rspeed = SSpeed;                 break;   //(1,0,1,1,0,0,0);   //Left
//    case 25 : Lspeed = -20;           Rspeed = SSpeed;                 break;   //(1,0,0,1,1,0,0);   //Left
//    case 35 : Lspeed = -SSpeed;     Rspeed = SSpeed;                 break;   //(1,1,0,0,0,1,0);   //Left
//    //case 63 : Lspeed = SSpeed - 20; Rspeed = SSpeed;                 break;   //(1,1,1,1,1,1,0);   //Left
//    case 67 : Lspeed = -100;        Rspeed = 100;                    break;   //(1,1,0,0,0,0,1);   //Left
//    case 68 : Lspeed = -SSpeed;     Rspeed = SSpeed;                 break;   //(0,0,1,0,0,0,1);   //Left
//    case 70 : Lspeed = -20;           Rspeed = SSpeed;                 break;   //(0,1,1,0,0,0,1);   //Left
//    //----------------------------- Turn Right ----------------------------------------------------------------------------------------------//
//    case 16 : Lspeed = SSpeed;      Rspeed = 40;                    break;   //(0,0,0,0,1,0,0);   //Right
//    case 17 : Lspeed = SSpeed;      Rspeed = 0;                      break;   //(1,0,0,0,1,0,0);   //Right
//    case 24 : Lspeed = SSpeed;      Rspeed = 50;                     break;   //(0,0,0,1,1,0,0);   //Right
//    case 32 : Lspeed = SSpeed;      Rspeed = -50;                     break;   //(0,0,0,0,0,1,0);   //Right
//    case 34 : Lspeed = SSpeed;      Rspeed = -SSpeed;                      break;   //(0,1,0,0,0,1,0);   //Right
//    case 48 : Lspeed = SSpeed;      Rspeed = -50;                    break;   //(0,0,0,0,1,1,0);   //Right
//    case 49 : Lspeed = SSpeed;      Rspeed = -70;                      break;   //(1,0,0,0,1,1,0);   //Right
//    case 62 : Lspeed = SSpeed;      Rspeed = -30;                      break;   //(0,1,1,1,1,0,0);   //Right
//    case 64 : Lspeed = 100; Rspeed = -100;           break;   //(0,0,0,0,0,0,1);   //Right
//    case 96 : Lspeed = SSpeed;      Rspeed = -80;                      break;   //(0,0,0,0,0,1,1);   //Right
//    case 97 : Lspeed = 100;         Rspeed = -100;                   break;   //(1,0,0,0,0,1,1);   //Right
//    case 107: Lspeed = SSpeed;      Rspeed = -30;                      break;   //(1,1,0,1,0,1,1);   //Right
//    //case 126: Lspeed = SSpeed;      Rspeed = 0;                      break;   //(0,1,1,1,1,1,1);   //Right
//    //---------------------------- STRAIGHT -------------------------------------------------------------------------------------------------//
//    case 8  : Lspeed = Straight;    Rspeed = Straight;               break;   //(0,0,0,1,0,0,0);   //Straight
//    case 28 : Lspeed = Straight;    Rspeed = Straight;               break;   //(0,0,1,1,1,0,0);   //Straight
//    //----------------------------- 90ºleft ------------------------------------------------------------------------------------------------//
//    case 7  : Lspeed = -100;        Rspeed = 100;                    break;   //(1,1,1,0,0,0,0);   //90ºleft
//    case 14 : Lspeed = -80;           Rspeed = SSpeed;                 break;   //(0,1,1,1,0,0,0);   //90ºleft
//    case 15 : Lspeed = -100;        Rspeed = 100;                    break;   //(1,1,1,1,0,0,0);   //90ºleft
//    case 30 : Lspeed = 0;           Rspeed = SSpeed;                 break;   //(0,1,1,1,1,0,0);   //90ºleft
//    case 44 : Lspeed = 0;           Rspeed = SSpeed;                 break;   //(0,1,1,1,0,0,0);   //90ºleft
//    //---------------------------- 90ºright ------------------------------------------------------------------------------------------------//
//    case 56 : Lspeed = 100;      Rspeed = -100;                      break;   //(0,0,0,1,1,1,0);   //90ºright
//    case 60 : Lspeed = 80;   Rspeed = -SSpeed;                 break;   //(0,0,1,1,1,1,0);   //90ºright
//    case 112: Lspeed = 100;      Rspeed = -100;                break;   //(0,0,0,0,1,1,1);   //90ºright
//    case 88 : Lspeed = 100;         Rspeed = -100;                   break;   //(0,0,0,0,1,1,1);   //90ºright
//  }

  Serial.print(dist);
  Serial.print(" , ");
  Serial.print(Lspeed);
  Serial.print(" , ");
  Serial.println(Rspeed);
  delay(50); 
}
