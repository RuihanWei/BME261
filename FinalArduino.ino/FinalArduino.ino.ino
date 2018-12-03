#include "HX711.h"
#define DOUT  3
#define CLK  2
 
HX711 scale(DOUT, CLK);

int serialData = 0;
int pin = 13;
float calibration_factor = -50750.00;     // Determined through calibration

#include <LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
int breadbardpinIn = 13;
int guitarIn = 11;
int timer = 1;
bool lethals [3] = {false, false, false};
int lethal_stepper = 0;
bool remainLethal = false;

int patientWeight = 62;                   // default to average weight
double sampling_rate = 1;
int period = 3;
const int MAXQUEUESIZE = 3;
double flowRates[MAXQUEUESIZE];         // rolling window of flow rates
                                        // size is 3/sampling_rate
double offset = 15.848+1.347;
float rmax = 0.0;
float rmin = 0.0;

int rear = 0;
int front = 0;
int QueueSize = front > rear ? (MAXQUEUESIZE - front + rear) : (rear - front);
float reading = 0.0;

bool weightInputed = false;

//=============================================================================================
//                         SETUP
//=============================================================================================

void setup() {
  Serial.begin(9600);
  scale.set_scale();
  scale.tare();

  //rmax = 25/24*patientWeight-40;
  rmax = 5;
  rmin = 30/24*patientWeight;
 
  long zero_factor = scale.read_average(); //Get a baseline reading
//  Serial.print("Zero factor: "); 
//  Serial.println(zero_factor);

  Serial.println("START!!");

  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);

  pinMode(breadbardpinIn,OUTPUT);
//  pinMode(breadbardpinOut,OUTPUT);
//  analogWrite(breadbardpinIn, 255);
  digitalWrite(breadbardpinIn, LOW);
  digitalWrite(guitarIn, HIGH);
  
  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  tone(guitarIn, 493, 273.683002294);
}
 
//=============================================================================================
//                         LOOP
//=============================================================================================

void loop() {
    if (lethal_stepper + 1 == 4){
      lethal_stepper = 1;
      lethals[0] == false;
      lethals[1] == false;
      lethals[2] == false;
    }
    else{
      lethal_stepper++;
    }
    //tone(guitarIn, 493, 273.683002294);
    
    if(Serial.available() > 0){
      serialData = Serial.parseInt();
      patientWeight = serialData;
      
      tone(guitarIn, 200, 273.683002294); 

      Serial.print("Patient Weight: ");
      Serial.print(patientWeight);
      
      //rmax = 25/24*patientWeight-40;
      rmax = 5;     // for demo purposes only, in production code the code above will be used
      Serial.read();   // ignore second input
    }
  
  scale.set_scale(calibration_factor);         //Adjust to this calibration factor
  reading = ((scale.get_units()+offset)*(1));
  
  Serial.print("Reading: ");
  Serial.print(reading);
  Serial.print(" kg"); 

//  Serial.print(" calibration_factor: ");
//  Serial.print(calibration_factor);
//  Serial.println();
//  Serial.print("rear: ");
//  Serial.print(rear);
//  Serial.print("front: ");
//  Serial.print(front);

  if (rear == front){
    flowRates[rear] = reading;
    rear = (rear+1)%MAXQUEUESIZE;
    front = (front+1)%MAXQUEUESIZE;
  }else{
    flowRates[rear] = reading;
    rear = (rear+1)%MAXQUEUESIZE;
  }

  float avgFlow = 0;
  avgFlow = (flowRates[front] - flowRates[rear == 0 ? MAXQUEUESIZE - 1 : (rear - 1)])/period;
  avgFlow = avgFlow*3600;    //magnified by 1000 for testing and demo purposes

    Serial.print("remain lethal: ");
    Serial.print(remainLethal);
    
  if (avgFlow < rmax){
    lcd.print(reading,3);
    if (!remainLethal)
      digitalWrite(breadbardpinIn, LOW);
      
    if (remainLethal){
      tone(guitarIn, 600, 273.683002294);
    }
      
    lethals[lethal_stepper-1] = false;

  }
  else {
      if (timer > 2){
        lcd.print("lethal!");
        tone(guitarIn, 600, 273.683002294);
        digitalWrite(breadbardpinIn, HIGH);
        //lethals[lethal_stepper-1] = true;
        //lcd.print(reading,3);
      }
  }

  Serial.print("  time: ");
  Serial.print(timer);
  
  Serial.print(" Weight: [");
  Serial.print(flowRates[0],3);
  Serial.print(" ");
  Serial.print(flowRates[1],3);
  Serial.print(" ");
  Serial.print(flowRates[2],3);
  Serial.print("]  ");

  
  Serial.print("flow rate: ");
  Serial.print(avgFlow);

  Serial.print("   front: ");
  Serial.print(front);
  Serial.println();

  if (lethals[0] == true && lethals[1] == true && lethals[2] == true)
    remainLethal = true;
  
  delay(sampling_rate*1000);
//  delay(1000);
  lcd.clear();
  lcd.setCursor(0,0);
  timer ++;
}
//=============================================================================================
