#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

int IN1=3;
int IN2=4;
int ENA=2;


int ENB=5;
int IN3=6;
int IN4=7;

int pwm = 9;

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *myMotor = AFMS.getMotor(1);

#define motor_speed 75

String test = "";
void motor (String check);

void motor(String check) {

  if (check.equals("f")) {
    Serial.println("FORWARD");
    myMotor->setSpeed(motor_speed);
    myMotor->run(FORWARD);
  }

  else if (check.equals("b")) {
      Serial.println("BACKWARD");
    myMotor->setSpeed(motor_speed);
    myMotor->run(BACKWARD);
  }

  else if (check.equals("0")) {
    myMotor->setSpeed(0);
  }

  else if (check.equals("e")) {
    Serial.println("EXTENDING");
    analogWrite(ENA, 255);// motor speed
    analogWrite(ENB, 245);  
    digitalWrite(IN1,LOW);// rotate forward
    digitalWrite(IN3,LOW);// rotate forward
    digitalWrite(IN2,HIGH);
    digitalWrite(IN4,HIGH);
    delay(6000);
    
  }

  else if (check.equals("r")) {
    Serial.println("RETRACTING");
    digitalWrite(IN1,HIGH);// rotate reverse
    digitalWrite(IN3,HIGH);// rotate reverse
    digitalWrite(IN2,LOW);
    digitalWrite(IN4,LOW);
    delay(5000);
    
  }

  else if (check.equals("p")) {
    Serial.println("BAG");

    int speed_converted = map(2000, 0, 6000, 0, 255); //see link for correct range
    analogWrite(pwm, speed_converted);
  }

  else if (check.equals("l")) {
   Serial.println("BAG OFF");

    int speed_converted = map(0, 0, 6000, 0, 255); //see link for correct range
    analogWrite(pwm, speed_converted);
  }
  

}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
  myMotor->setSpeed(motor_speed);

  pinMode(IN1,OUTPUT);
 pinMode(IN2,OUTPUT);  
 pinMode(IN3,OUTPUT);
 pinMode(IN4,OUTPUT); 
 analogWrite(ENA, 255);// motor speed
 analogWrite(ENB, 245);
   
  
  
}

void loop() {
  // put your main code here, to run repeatedly


  test = "";
  while (Serial.available()) {
    test += (char)Serial.read();
  }
  if (test != "") {
    Serial.println(test);
    motor(test);
  }


  
//  Serial.println("FORWARD");
//  
//  myMotor->run(FORWARD);
//  delay(5000);
//  
//  Serial.println("BACKWARD");
//
//   myMotor->run(BACKWARD);
//   delay(5000);

//  Serial.println("RELEASE");
//
//   myMotor->run(RELEASE);
//   delay(5000);
//  delay(500);


  

}
