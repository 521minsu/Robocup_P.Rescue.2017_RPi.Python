const int AsensorPin = A2;
const int DsensorPin = 13;

int AsensorVal = 0;
int AsensorFinal = 0;
int AsensorFinLast = 0;
boolean Asensorboolean = false;
int DsensorVal = 0;

void setup() {
  Serial.begin(9600);
  pinMode(AsensorPin,INPUT);
  pinMode(DsensorPin,INPUT);
}

void loop() {
  AsensorVal = analogRead(AsensorPin);
  DsensorVal = digitalRead(DsensorPin);
  if(AsensorVal > 999) AsensorFinal = 0;
  else AsensorFinal = 1;
  
  if(AsensorFinal != AsensorFinLast) {
    AsensorFinLast = AsensorFinal;
    Asensorboolean = false;
  } else Asensorboolean = true;
  
  Serial.print("Catched:");
  Serial.print(AsensorFinal);
  Serial.print(" \t ");
  Serial.print("Boolean:");
  Serial.print(Asensorboolean);
  Serial.print(" \t ");
  Serial.print("Raw:");
  Serial.println(AsensorVal);
}
