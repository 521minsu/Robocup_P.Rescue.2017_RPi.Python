//++++++++++++++++++++++++++++++++++++++++++++++++++ Sonar Sensor +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
#include <NewPing.h>
#define TRIG_PIN     52
#define ECHO_PIN     53
#define MAX_DISTANCE 300
NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
//++++++++++++++++++++++++++++++++++++++++++++++ IR sensor & its LED Defs +++++++++++++++++++++++++++++++++++++++++++++++++++++++//
const int s1=A8, s2=A9, s3=A10, s4=A11, s5=A13, s6=A14, s7=A15;
//+++++++++++++++++++++++++++++++++++++++++ Motor pin Defs & other motor things +++++++++++++++++++++++++++++++++++++++++++++++++++//
const int MOTORLATCH=12,MOTORCLK=4,MOTORENABLE=7,MOTORDATA=8;
const int MOTOR1_A=2,MOTOR1_B=3,MOTOR2_A=1,MOTOR2_B=4,MOTOR3_A=5,MOTOR3_B=7,MOTOR4_A=0,MOTOR4_B=6;
const int MOTOR1_PWM=11,MOTOR2_PWM=3,MOTOR3_PWM=6,MOTOR4_PWM=5;
const int FORWARD=1,BACKWARD=2,BRAKE=3,RELEASE=4,dLEFT=5,dRIGHT=6;
const int MaxSpeed = 254;
//---------------------------------------------------------------------------------------------------------------------------------//
int cm = 300;
int sVal[8];
int binarray = 0, preval = 0;
int Lspeed,Rspeed;
//---------------------------------------------------------------------------------------------------------------------------------//
String inputString = "";         // a string to hold incoming data
int Gcoord,Rcoord,Vcoord,Ocoord,Bcoord;
String greenTurn="3",lastGreen,rescue,vx,ox,black;
boolean stringComplete = false;  // whether the string is complete
boolean finished = false;
//---------------------------------------------------------------------------------------------------------------------------------//
boolean DebugMode = false;
//---------------------------------------------------------------------------------------------------------------------------------//
int WTDone=0,WTLimit=1;
//---------------------------------------------------------------------------------------------------------------------------------//

//=============================================================== SETUP ============================================================================//
void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN,OUTPUT); pinMode(ECHO_PIN,INPUT);
  pinMode(s1,INPUT); pinMode(s2,INPUT); pinMode(s3,INPUT); pinMode(s4,INPUT); pinMode(s5,INPUT); pinMode(s6,INPUT); pinMode(s7,INPUT);
  inputString.reserve(200); inputString = "";
  lift(0,0);drive(0,0);
}

void loop() {
//  if(finished == false){
//    IR_sensor();
//    UltraSonic();
//    RPi_Emergency_Control();
//      
//    if(greenTurn!="3"){
//      MoveControl();
//      WaterTower();
//      RPiMovements();
//    }
//  } else drive(0,0);
  UltraSonic();
  Serial.println(cm);
}

void IR_sensor() {
  if (analogRead(s1) < 400) sVal[0] = 0; else sVal[0] = 1;
  if (analogRead(s2) < 400) sVal[1] = 0; else sVal[1] = 1;
  if (analogRead(s3) < 400) sVal[2] = 0; else sVal[2] = 1;
  if (analogRead(s4) < 400) sVal[3] = 0; else sVal[3] = 1;
  if (analogRead(s5) < 400) sVal[4] = 0; else sVal[4] = 1;
  if (analogRead(s6) < 400) sVal[5] = 0; else sVal[5] = 1;
  if (analogRead(s7) < 400) sVal[6] = 0; else sVal[6] = 1; 
//-----------------------------------------------------------------------------------------------------------------------
  binarray = (sVal[6] * 64) + (sVal[5] * 32) + (sVal[4] * 16) + (sVal[3] * 8) + (sVal[2] * 4) + (sVal[1] * 2) + sVal[0];
//-----------------------------------------------------------------------------------------------------------------------
}

void UltraSonic() {
  delay(50);
  cm = sonar.ping_cm();
  if (cm > 200 || cm == 0) cm = 300;
}

void MoveControl() {
  int SSpeed = 170,Straight = SSpeed - 10;
  IR_sensor();
  
  switch (binarray) {   //1,2,4,8,16,32,64//
    //---------------------------- Turn Left ------------------------------------------------------------------------------------------------//
    case 1  : drive(-SSpeed - 50, SSpeed + 50);       break;   //(1,0,0,0,0,0,0);   //Left
    case 2  : drive(0, SSpeed);                       break;   //(0,1,0,0,0,0,0);   //Left
    case 3  : drive(-250, 250);                       break;   //(1,1,0,0,0,0,0);   //Left
    case 4  : drive(-30, SSpeed);                     break;   //(0,0,1,0,0,0,0);   //Left
    case 6  : drive(-70, SSpeed);                     break;   //(0,1,1,0,0,0,0);   //Left
    case 12 : drive(SSpeed - 40, SSpeed);             break;   //(0,0,1,1,0,0,0);   //Left
    case 13 : drive(SSpeed - 50, SSpeed);             break;   //(1,0,1,1,0,0,0);   //Left
    case 25 : drive(0, SSpeed);                       break;   //(1,0,0,1,1,0,0);   //Left
    case 35 : drive(-SSpeed, SSpeed);                 break;   //(1,1,0,0,0,1,0);   //Left
  //case 63 : drive(SSpeed - 50, SSpeed);             break;   //(1,1,1,1,1,1,0);   //Left //Was annotated
    case 67 : drive(-250, 250);                       break;   //(1,1,0,0,0,0,1);   //Left
    case 68 : drive(-SSpeed, SSpeed);                 break;   //(0,0,1,0,0,0,1);   //Left //Was annotated
    case 70 : drive(0, SSpeed);                       break;   //(0,1,1,0,0,0,1);   //Left //Was annotated
    //----------------------------- Turn Right ----------------------------------------------------------------------------------------------//
    case 16 : drive(SSpeed, -30);                     break;   //(0,0,0,0,1,0,0);   //Right
    case 17 : drive(SSpeed, 0);                       break;   //(1,0,0,0,1,0,0);   //Right
    case 24 : drive(SSpeed, SSpeed - 40);             break;   //(0,0,0,1,1,0,0);   //Right
    case 32 : drive(SSpeed, 0);                       break;   //(0,0,0,0,0,1,0);   //Right
    case 34 : drive(SSpeed, 0);                       break;   //(0,1,0,0,0,1,0);   //Right //Was annotated
    case 48 : drive(SSpeed, -70);                     break;   //(0,0,0,0,1,1,0);   //Right
    case 49 : drive(SSpeed, 0);                       break;   //(1,0,0,0,1,1,0);   //Right
    case 62 : drive(SSpeed, 0);                       break;   //(0,1,1,1,1,0,0);   //Right //Was annotated
    case 64 : drive(SSpeed + 50, -SSpeed - 50);       break;   //(0,0,0,0,0,0,1);   //Right
    case 96 : drive(250, -250);                       break;   //(0,0,0,0,0,1,1);   //Right
    case 97 : drive(250, -250);                       break;   //(1,0,0,0,0,1,1);   //Right
    case 107: drive(SSpeed, 0);                       break;   //(1,1,0,1,0,1,1);   //Right //Was annotated
    case 126: drive(SSpeed, 0);                       break;   //(0,1,1,1,1,1,1);   //Right //Was annotated
    //---------------------------- STRAIGHT -------------------------------------------------------------------------------------------------//
    case 8  : drive(Straight, Straight);              break;   //(0,0,0,1,0,0,0);   //Straight
    case 28 : drive(Straight, Straight);              break;   //(0,0,1,1,1,0,0);   //Straight
    case 9  : drive(Straight, Straight);              break;   //(1,0,0,1,0,0,0);   //Straight
    case 72 : drive(Straight, Straight);              break;   //(0,0,0,1,0,0,1);   //Straight
    case 80 : drive(Straight, Straight);              break;   //(0,0,0,0,1,0,1);   //Straight
    case 100: drive(Straight, Straight);              break;   //(1,0,0,1,0,0,0);   //Straight
    case 65 : drive(Straight, Straight);              break;   //(0,0,0,0,1,0,1);   //Straight
    //----------------------------- 90ºleft ------------------------------------------------------------------------------------------------//
    case 7  : drive(-250, 250);                       break;   //(1,1,1,0,0,0,0);   //90ºleft
    case 14 : drive(0, SSpeed);                       break;   //(0,1,1,1,0,0,0);   //90ºleft
    case 15 : drive(-250, 250);                       break;   //(1,1,1,1,0,0,0);   //90ºleft
    case 30 : drive(0, SSpeed);                       break;   //(0,1,1,1,1,0,0);   //90ºleft
    case 31 : drive(-250, 250);                       break;   //(1,1,1,1,1,0,0);   //90ºleft
    case 44 : drive(0, SSpeed);                       break;   //(0,1,1,1,0,0,0);   //90ºleft
    //---------------------------- 90ºright ------------------------------------------------------------------------------------------------//
    case 56 : drive(SSpeed, 0);                       break;   //(0,0,0,1,1,1,0);   //90ºright
    case 60 : drive(SSpeed-20, SSpeed);               break;   //(0,0,1,1,1,1,0);   //90ºright
    case 112: drive(SSpeed, -SSpeed);                 break;   //(0,0,0,0,1,1,1);   //90ºright
    case 88 : drive(250, -250);                       break;   //(0,0,0,0,1,1,1);   //90ºright
    //---------------------------- DEFAULT --------------------------------------------------------------------------------------------------//
    default :  PreVal();                              break;   //(0,0,0,0,0,0,0);   //Previous Action
    //----------------------------- END -----------------------------------------------------------------------------------------------------//
  }
  preval = binarray;
}

void PreVal() {
  int SSpeed = 170,Straight = SSpeed - 10;
  
  switch (preval) {   //1,2,4,8,16,32,64//
    case 1  : drive(-SSpeed - 50, SSpeed + 50);       break;   //(1,0,0,0,0,0,0);   //Left
    case 2  : drive(0, SSpeed);                       break;   //(0,1,0,0,0,0,0);   //Left
    case 3  : drive(-250, 250);                       break;   //(1,1,0,0,0,0,0);   //Left
    case 4  : drive(-30, SSpeed);                     break;   //(0,0,1,0,0,0,0);   //Left
    case 6  : drive(-70, SSpeed);                     break;   //(0,1,1,0,0,0,0);   //Left
    case 12 : drive(SSpeed - 40, SSpeed);             break;   //(0,0,1,1,0,0,0);   //Left
    case 13 : drive(SSpeed - 50, SSpeed);             break;   //(1,0,1,1,0,0,0);   //Left
    case 25 : drive(0, SSpeed);                       break;   //(1,0,0,1,1,0,0);   //Left
    case 35 : drive(-SSpeed, SSpeed);                 break;   //(1,1,0,0,0,1,0);   //Left
    case 63 : drive(SSpeed - 50, SSpeed);             break;   //(1,1,1,1,1,1,0);   //Left //Was annotated
    case 67 : drive(-250, 250);                       break;   //(1,1,0,0,0,0,1);   //Left
    case 68 : drive(-SSpeed, SSpeed);                 break;   //(0,0,1,0,0,0,1);   //Left //Was annotated
    case 70 : drive(0, SSpeed);                       break;   //(0,1,1,0,0,0,1);   //Left //Was annotated
    //----------------------------- Turn Right ----------------------------------------------------------------------------------------------//
    case 16 : drive(SSpeed, -30);                     break;   //(0,0,0,0,1,0,0);   //Right
    case 17 : drive(SSpeed, 0);                       break;   //(1,0,0,0,1,0,0);   //Right
    case 24 : drive(SSpeed, SSpeed - 40);             break;   //(0,0,0,1,1,0,0);   //Right
    case 32 : drive(SSpeed, 0);                       break;   //(0,0,0,0,0,1,0);   //Right
    case 34 : drive(SSpeed, 0);                       break;   //(0,1,0,0,0,1,0);   //Right //Was annotated
    case 48 : drive(SSpeed, -70);                     break;   //(0,0,0,0,1,1,0);   //Right
    case 49 : drive(SSpeed, 0);                       break;   //(1,0,0,0,1,1,0);   //Right
    case 62 : drive(SSpeed, 0);                       break;   //(0,1,1,1,1,0,0);   //Right //Was annotated
    case 64 : drive(SSpeed + 50, -SSpeed - 50);       break;   //(0,0,0,0,0,0,1);   //Right
    case 96 : drive(250, -250);                       break;   //(0,0,0,0,0,1,1);   //Right
    case 97 : drive(250, -250);                       break;   //(1,0,0,0,0,1,1);   //Right
    case 107: drive(SSpeed, 0);                       break;   //(1,1,0,1,0,1,1);   //Right //Was annotated
    case 126: drive(SSpeed, 0);                       break;   //(0,1,1,1,1,1,1);   //Right //Was annotated
    //---------------------------- STRAIGHT -------------------------------------------------------------------------------------------------//
    case 8  : drive(Straight, Straight);              break;   //(0,0,0,1,0,0,0);   //Straight
    case 9  : drive(Straight, Straight);              break;   //(1,0,0,1,0,0,0);   //Straight
    case 72 : drive(Straight, Straight);              break;   //(0,0,0,1,0,0,1);   //Straight
    case 80 : drive(Straight, Straight);              break;   //(0,0,0,0,1,0,1);   //Straight
    //----------------------------- 90ºleft ------------------------------------------------------------------------------------------------//
    case 7  : drive(-250, 250);                       break;   //(1,1,1,0,0,0,0);   //90ºleft
    case 14 : drive(0, SSpeed);                       break;   //(0,1,1,1,0,0,0);   //90ºleft
    case 15 : drive(-250, 250);                       break;   //(1,1,1,1,0,0,0);   //90ºleft
    case 30 : drive(0, SSpeed);                       break;   //(0,1,1,1,1,0,0);   //90ºleft
    case 31 : drive(-250, 250);                       break;   //(1,1,1,1,1,0,0);   //90ºleft
    case 44 : drive(0, SSpeed);                       break;   //(0,1,1,1,0,0,0);   //90ºleft
    //---------------------------- 90ºright ------------------------------------------------------------------------------------------------//
    case 56 : drive(SSpeed, 0);                       break;   //(0,0,0,1,1,1,0);   //90ºright
    case 60 : drive(SSpeed-20, SSpeed);               break;   //(0,0,1,1,1,1,0);   //90ºright
    case 112: drive(SSpeed, -SSpeed);                 break;   //(0,0,0,0,1,1,1);   //90ºright
    case 88 : drive(250, -250);                       break;   //(0,0,0,0,1,1,1);   //90ºright
    }
}

void RPi_Emergency_Control() { 
  serialEvent();
  if (stringComplete) {
    String G = "G";
    if(inputString.startsWith(G)){
      Gcoord     = inputString.indexOf('G');
      Rcoord     = inputString.indexOf('R');
      Vcoord     = inputString.indexOf('V');
      Ocoord     = inputString.indexOf('O');
      Bcoord     = inputString.indexOf('B');
      greenTurn  = inputString.substring(Gcoord+1,Gcoord+2); 
      rescue     = inputString.substring(Rcoord+1,Rcoord+2);
      vx         = inputString.substring(Vcoord+1,Vcoord+2); 
      ox         = inputString.substring(Ocoord+1,Ocoord+2);
      black      = inputString.substring(Bcoord+1,Bcoord+2);
    }
    Serial.print("Raw:");Serial.println(inputString);
    Gcoord=0;Rcoord=0;Vcoord=0;Ocoord=0;Bcoord=0;
    inputString = "";
    stringComplete = false;
  } 
  Serial.print("From EC...");Serial.print("\t");
  Serial.print("IR:");Serial.print(binarray);Serial.print("\t");
  Serial.print("Dist:");Serial.print(cm);Serial.print("\t");
  Serial.print("green:");Serial.print(greenTurn);Serial.print("\t");
  Serial.print("res:");Serial.print(rescue);Serial.print("\t");
  Serial.print("ox:");Serial.print(ox);Serial.print("\t");
  Serial.print("vx:");Serial.print(vx);Serial.print("\t");
  Serial.print("black:");Serial.println(black);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar; 
    
    if (inChar == '*') {
      stringComplete = true;
    } 
  }
} 

void RPiMovements() {
  if(greenTurn != "2"){
    drive(0,0);      delay(100); 
    IR_sensor(); 
    while(sVal[1] != 1 && sVal[5] != 1) {
      drive(140,140);
      IR_sensor();
    } drive(0,0);delay(500); 
    if(greenTurn == "0"){       //Turn Left
      drive(-5,170);delay(1800);
    } else {                    //Turn Right
      drive(170,0);delay(1300);
    } drive(0,0);delay(100); 
      drive(0,0);
    while (Serial.available()) Serial.println(Serial.read()); 
    greenTurn="2";
  }
  if(rescue == "1") startRescue();
}

void WaterTower() {
int less = -30, more = 200;
if(cm < 30 && WTDone < WTLimit){
  Serial.println("Start");
  drive(0, 0);      //Left is 12 because of the speed correction
  delay(1000);        //Generalize the speed
//-----------------------------------------------------------------
  drive(more, less); //Right
  delay(1000);
  drive(more,more);
  delay(300);
  IR_sensor();
  while(sVal[3] != 1){
    drive(-less+15, more); //Left
    IR_sensor();
  } drive(more,less);
    delay(500);
  Serial.println("END");
//------------------------------------------------------------------
    WTDone++;
//------------------------------------------------------------------
  } IR_sensor();
}

void startRescue() {
  int searchPlatform = 0,mSpeed = 150;
  while(true){
    RPi_Emergency_Control();UltraSonic();
    if(vx == "1" && searchPlatform == 0) {
      drive(mSpeed,-mSpeed);
      delay(300);
      UltraSonic();
      while(cm > 6){
        drive(mSpeed,mSpeed);
        UltraSonic();
      }
      drive(0,0);
      lift(250,0);      delay(1500);
      lift(250,250);    delay(1500);
      drive(-mSpeed,-mSpeed); delay(500);
      drive(0,0);
      while (Serial.available()) Serial.println(Serial.read());
      searchPlatform = 1;
    } RPi_Emergency_Control();UltraSonic();
    if(ox == "1" && searchPlatform == 1){
      while (cm > 6){
        drive(mSpeed,mSpeed);
        UltraSonic();
      }
      drive(0,0);
      lift(0,-250);      delay(1000);
      lift(-250,0);      delay(1000);
      drive(-mSpeed,-mSpeed); delay(500);
      drive(0,0);
      finished = true;
      break;
      while (Serial.available()) Serial.println(Serial.read());
    } RPi_Emergency_Control();
    if(searchPlatform == 0) drive(-mSpeed,mSpeed);
    else drive(mSpeed,-mSpeed);
  }
}

//------------------------------------------------------------------Motor Stuff-------------------------------------------------------------------//
void drive(int LeftS, int RightS) {
  int LM_Dir = FORWARD;
  int RM_Dir = FORWARD;
  
  if (LeftS  < 0) {
    LM_Dir = BACKWARD;
    LeftS  = abs(LeftS);
  }  else LM_Dir = FORWARD;
  if (RightS < 0) {
    RM_Dir = BACKWARD;
    RightS = abs(RightS);
  } else RM_Dir = FORWARD;
  
  //if (LeftS != 0) motor(3,  LM_Dir, LeftS-10 );
  motor(3,  LM_Dir, LeftS );
  motor(4, RM_Dir, RightS );

}

void lift(int Catch, int Lift) {
  int LIFT_Dir = BACKWARD;
  int CATCH_Dir = BACKWARD;

  if (Lift  < 0) {
    LIFT_Dir = FORWARD;
    Lift  = abs(Lift);
  }  else LIFT_Dir = BACKWARD;
  if (Catch < 0) {
    CATCH_Dir = FORWARD;
    Catch = abs(Catch);
  } else CATCH_Dir = BACKWARD;

  motor(2,  LIFT_Dir, Lift);// ADD speed correction as robot never moves straight when the speed is same
  motor(1, CATCH_Dir, Catch );
}

void motor(int nMotor, int command, int speed)
{
  int motorA, motorB;

  if (nMotor >= 1 && nMotor <= 4)
  {
    switch (nMotor)
    {
      case 1:
        motorA   = MOTOR1_A;
        motorB   = MOTOR1_B;
        break;
      case 2:
        motorA   = MOTOR2_A;
        motorB   = MOTOR2_B;
        break;
      case 3:
        motorA   = MOTOR3_A;
        motorB   = MOTOR3_B;
        break;
      case 4:
        motorA   = MOTOR4_A;
        motorB   = MOTOR4_B;
        break;
      default:
        break;
    }

    switch (command)
    {
      case FORWARD:
        motor_output (motorA, HIGH, speed);
        motor_output (motorB, LOW, -1);     // -1: no PWM set
        break;
      case BACKWARD:
        motor_output (motorA, LOW, speed);
        motor_output (motorB, HIGH, -1);    // -1: no PWM set
        break;
      case BRAKE:
        motor_output (motorA, LOW, 255); // 255: fully on.
        motor_output (motorB, LOW, -1);  // -1: no PWM set
        break;
      case RELEASE:
        motor_output (motorA, LOW, 0);  // 0: output floating.
        motor_output (motorB, LOW, -1); // -1: no PWM set
        break;
      default:
        break;
    }
  }
}

void motor_output (int output, int high_low, int speed)
{
  int motorPWM;

  switch (output)
  {
    case MOTOR1_A:
    case MOTOR1_B:
      motorPWM = MOTOR1_PWM;
      break;
    case MOTOR2_A:
    case MOTOR2_B:
      motorPWM = MOTOR2_PWM;
      break;
    case MOTOR3_A:
    case MOTOR3_B:
      motorPWM = MOTOR3_PWM;
      break;
    case MOTOR4_A:
    case MOTOR4_B:
      motorPWM = MOTOR4_PWM;
      break;
    default:
      speed = -3333;
      break;
  }

  if (speed != -3333)
  {
    shiftWrite(output, high_low);

    if (speed >= 0 && speed <= 255)
    {
      analogWrite(motorPWM, speed);
    }
  }
}

void shiftWrite(int output, int high_low)
{
  static int latch_copy;
  static int shift_register_initialized = false;

  if (!shift_register_initialized)
  {
    pinMode(MOTORLATCH, OUTPUT);
    pinMode(MOTORENABLE, OUTPUT);
    pinMode(MOTORDATA, OUTPUT);
    pinMode(MOTORCLK, OUTPUT);

    digitalWrite(MOTORDATA, LOW);
    digitalWrite(MOTORLATCH, LOW);
    digitalWrite(MOTORCLK, LOW);
    digitalWrite(MOTORENABLE, LOW);

    latch_copy = 0;

    shift_register_initialized = true;
  }

  bitWrite(latch_copy, output, high_low);

  shiftOut(MOTORDATA, MOTORCLK, MSBFIRST, latch_copy);
  delayMicroseconds(5);
  digitalWrite(MOTORLATCH, HIGH);
  delayMicroseconds(5);
  digitalWrite(MOTORLATCH, LOW);
}

