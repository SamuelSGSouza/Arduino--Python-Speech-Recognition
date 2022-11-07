int led1 = 8; int led2 = 9; int led3 = 10;
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char serial = Serial.read();
    if (serial == "a"){
      digitalWrite(led1, HIGH);
    }
    if (serial == "b"){
      digitalWrite(led2, HIGH);
    }
    if (serial == "c"){
      digitalWrite(led3, HIGH);
    }
    if (serial == "A"){
      digitalWrite(led1, LOW);
    }
    if (serial == "B"){
      digitalWrite(led2, LOW);
    }
    if (serial == "C"){
      digitalWrite(led3, LOW);
    }
  }
}
