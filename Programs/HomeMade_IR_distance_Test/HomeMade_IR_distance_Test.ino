int a,b,c;

void setup() {
  Serial.begin(9600);
  pinMode(6,OUTPUT);
}

void loop() {
  digitalWrite(6,HIGH);
  delayMicroseconds(500);
  a = analogRead(A1);
  digitalWrite(6,LOW);
  delayMicroseconds(500);
  b = analogRead(A1);
  c = a-b;
  
  Serial.print("Noise+Signal: ");
  Serial.print(a);
  Serial.print("\t");
  Serial.print("Noise: ");
  Serial.print(b);
  Serial.print("\t");
  Serial.print("Denoised Signal: ");
  Serial.println(c);
  delay(500);
}
