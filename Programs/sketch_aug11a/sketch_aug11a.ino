const byte npulse = 3;
const bool sound = true, debug = false;

const byte pin_pulse = A0, pin_cap = A1;
const int FirstLED = 11, SecondLED = 12;

void setup() {
    Serial.begin(9600);
    pinMode(FirstLED, OUTPUT);
    pinMode(SecondLED, OUTPUT);
    pinMode(pin_pulse, OUTPUT);
    digitalWrite(pin_pulse, LOW);
    pinMode(pin_cap, INPUT);
}

const int nmeas = 256; //no. of measurements to take
long int sumsum = 0;   //running sum of 64 sums
long int skip   = 0;   //no. of skipped sums
long int diff   = 0;   // difference between sum and avgsum

long int flash_period = 0;
long unsigned int prev_flash = 0;

void loop() {
    int minval = 1023;
    int maxval = 0;

    //Performing the measurement
    long unsigned int sum = 0;
    for (int imeas = 0; imeas < nmeas + 2; imeas++){
        //reset the capacitor
        pinMode(pin_cap,OUTPUT);
        digitalWrite(pin_cap, LOW);
        delayMicroseconds(20);
        pinMode(pin_cap, INPUT);
        
        //apply pulses
        for (int ipulse = 0; ipulse < npulse; ipulse++) {
            digitalWrite(pin_pulse, HIGH);
            delayMicroseconds(3);
            digitalWrite(pin_pulse, LOW);
            delayMicroseconds(3);
        }

        //Read the charge on the capacitor
        int val = analogRead(pin_cap);  //takes 13x8=104 microseconds
        minval = min(val,minval);
        maxval = max(val,maxval);
        sum += val;

        long unsigned int timestamp = millis();
        byte ledstat = 0;
        if(timestamp < prev_flash + 10) {
            if(diff>0) ledstat = 1;
            if(diff<0) ledstat = 2;
        }
        if(timestamp > prev_flash + flash_period){
            if(diff>0) ledstat = 1;
            if(diff<0) ledstat = 2;
        }
        if(flash_period > 1000) ledstat = 0;

        if(ledstat == 0) {
            Serial.println("LEDs OFF");
            digitalWrite(FirstLED, LOW);
            digitalWrite(SecondLED, LOW);
        } if(ledstat == 1) {
            Serial.println("1st LED ON");
            digitalWrite(FirstLED, HIGH);
            digitalWrite(SecondLED, LOW);
        } if(ledstat == 2) {
            Serial.println("2nd LED ON");
            digitalWrite(FirstLED, LOW);
            digitalWrite(SecondLED, HIGH);
        }

    //subtract minimum and maximum val to remove spikes
    sum -= minval; sum -= maxval;

    //process
    if(sumsum == 0) sumsum = sum << 6; //set sumsum to expected val
    long int avgsum = (sumsum + 32) >> 6;
    diff = sum - avgsum;
    if(abs(diff)<avgsum>>10){
        sumsum = sumsum +sum -avgsum;
        skip = 0;
    } else skip++;
    if(skip > 64) {
      sumsum = sum << 6;
      skip = 0;
    }

    //one permille change = 2 ticks
    if(diff == 0) flash_period = 1000000;
    else flash_period = avgsum/(2*abs(diff));
    
  }
}
