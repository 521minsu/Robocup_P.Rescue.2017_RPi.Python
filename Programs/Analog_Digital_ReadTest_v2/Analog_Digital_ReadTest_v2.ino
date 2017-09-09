const int AsensorPin = A2;
const int DsensorPin = 13;

int AsensorVal = 0;
int AsensorFinal = 0;
int DsensorVal = 0;

void setup() {
  Serial.begin(9600);
  pinMode(AsensorPin,INPUT);
  pinMode(DsensorPin,INPUT);
}

void loop() {
  AsensorVal = analogRead(AsensorPin);
  DsensorVal = digitalRead(DsensorPin);
  if(AsensorVal > 995) AsensorFinal = 0;
  else AsensorFinal = 1;
  
  Serial.print("Catched:");
  Serial.print(AsensorFinal);
  Serial.print(" \t ");
  Serial.print("Raw:");
  Serial.println(AsensorVal);
}
