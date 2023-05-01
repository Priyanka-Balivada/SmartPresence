#include <Adafruit_MLX90614.h>
#include <ESP8266WiFi.h>
#include <ThingSpeak.h>
WiFiClient client;
int buzzer=D5;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  pinMode (buzzer,OUTPUT);
  WiFi.begin("wifiName","password");
  while(WiFi.status() !=WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }

  ThingSpeak.begin(client);
  
  Serial.begin(115200);
  while (!Serial);

  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);
  };
}

void loop() {
//  float ambienttemp=mlx.readAmbientTempF();
  float objecttemp=mlx.readObjectTempF();
//  ThingSpeak.writeField(myChannelNumber, 1,ambienttemp, myWriteAPIKey);
  ThingSpeak.writeField(myChannelNumber, 2,objecttemp, myWriteAPIKey);
  
  if(objecttemp>100.4)
  {
    digitalWrite(buzzer,HIGH) ; 
  }
  else
  {
    digitalWrite(buzzer,LOW) ; 
  }
  
//  Serial.print("Ambient temperature = ");
//  Serial.print(ambienttemp);
//  Serial.print("°F");      
//  Serial.print("   ");
  Serial.print("Object temperature = "); 
  Serial.print(objecttemp); 
  Serial.println("°F");

  Serial.println("-----------------------------------------------------------------");
}
