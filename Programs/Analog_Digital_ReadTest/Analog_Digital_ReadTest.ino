const int AsensorPin = A2;
const int DsensorPin = 13;

int AsensorVal = 0;
int DsensorVal = 0;

void setup() {
  Serial.begin(9600);
  pinMode(AsensorPin,INPUT);
  pinMode(DsensorPin,INPUT);
}

void loop() {
  AsensorVal = analogRead(AsensorPin);
  DsensorVal = digitalRead(DsensorPin);
  
  Serial.print("Digital:");
  Serial.print(DsensorVal);
  Serial.print(" \t ");
  Serial.print("Analog:");
  Serial.println(AsensorVal);
}
