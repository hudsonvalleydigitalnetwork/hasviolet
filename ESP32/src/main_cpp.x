/*
  HASviolet-Duck.ino

  INTRO

  Duckhunt is transmitter hunting revisited. We refer to the hunted as “ducks” who are RPi or ESP32 devices
  equipped with LoRa and WiFi. Ducks "quack" RF using LoRa at programmable intervals and triggers.


  This is a prototype.

  20200714
     
*/

// Import required libraries
#include "Time.h"
#include "TimeLib.h"
#include "heltec.h"
#include "hvdn-logo.h"
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "SPIFFS.h"

// Set WiFi AP
const char* APssid = "Duck";                 // Unique WiFi AP SSID for this Duck
const char* APpassword = "123456789";        // Unique WiFi password for this Duck

// Set WebAuthh
const char* wwwUSERNAME = "admin";           // Webpage Login
const char* wwwAUTHPASS = "Quackers";        // Webpage password

// Configure LoRa and Appstack
#define BAND    911250000                    // you can set band here directly, ( 868E6,915E6 )
byte localaddressLORA = 0xBB;                // LoRa address of this device (irrelevant)
byte destinationLORA = 0xFF;                 // LoRa destination to send to (broadcast default)
String HASmyCall = " NOCALL";
String HASmySSID = "00";
String HASdstcall = " BEACON";               // HASviolet Destination Call ( BEACON )
String HASdstssid = "99";                    // HASviolet Desnitation Call ( 99 )
String HASlastmsg = "None";                  // Last received message
String HASlastTXmsg = "None";                // Last transmitted message
int HASfreq = 911250000;                     // HASviolet default settings for safe LoRa module init
int HAStxpwr = 5;
int HASsignalBW = 125000;
int HAScodingrate4 = 8;
int HASspreadingFactor = 7;

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Duck Declarations (as found in order in duckhunt.cfg)
String simple_interval;
String simple_trigger;
String simple_message;
String harder_interval;
String harder_trigger;
String harder_message;

// Display HVDN Logo on OLED
void logo(){
  Heltec.display->clear();
  Heltec.display->drawXbm(0,5,hvdnimg_width,hvdnimg_height,hvdnimg_bits);
  Heltec.display->display();
  delay(1500);
  Heltec.display->clear();
}

void OLEDme(String myOLEDmsg, int oledTIME)
{
  Heltec.display->clear();
  Heltec.display->setTextAlignment(TEXT_ALIGN_LEFT);
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 15, myOLEDmsg);
  Heltec.display->display();
  delay(oledTIME);
  Heltec.display->clear();
}

// Read DUCK.CFG from SPIFFS
void getDUCKCFG()                           
  {
    File duckcfgREAD = SPIFFS.open("/duck.cfg");
    if(!duckcfgREAD){
      Serial.println("ERR: Opening DUCK.CFG for read");
      return;
    }
    while (duckcfgREAD.available()){
      String file_freq = duckcfgREAD.readStringUntil('\n');
      HASfreq = file_freq.toInt();
      String file_txpwr = duckcfgREAD.readStringUntil('\n');
      HAStxpwr = file_txpwr.toInt();
      HASmyCall = duckcfgREAD.readStringUntil('\n');
      HASmySSID = duckcfgREAD.readStringUntil('\n');
      HASdstcall = duckcfgREAD.readStringUntil('\n');
      HASdstssid = duckcfgREAD.readStringUntil('\n');
    }
    duckcfgREAD.close();
  }

// Read DUCKHUNT.CFG from SPIFFS
void getDUCKHUNTCFG()                           
  {
    File duckhuntREAD = SPIFFS.open("/duckhunt.cfg");
    if(!duckhuntREAD){
      Serial.println("ERR: Opening DUCKHUNT.CFG for read");
      return;
    }
    while (duckhuntREAD.available()){
      simple_interval = duckhuntREAD.readStringUntil('\n');
      simple_trigger = duckhuntREAD.readStringUntil('\n');
      simple_message = duckhuntREAD.readStringUntil('\n');
      harder_interval = duckhuntREAD.readStringUntil('\n');
      harder_trigger = duckhuntREAD.readStringUntil('\n');
      harder_message = duckhuntREAD.readStringUntil('\n');
    }
    duckhuntREAD.close();
  }

// Write DUCK.CFG to SPIFFS
void writeDUCKCFG()
{
  File duckcfgWRITE = SPIFFS.open("/duck.cfg", FILE_WRITE);
  if(!duckcfgWRITE){
    Serial.println("ERR: Error opening DUCK.CFG for write");
    return;
  }
  while (duckcfgWRITE.available()){
    duckcfgWRITE.println(HASfreq);
    Serial.println("115: Writing to DUCK.CFG");
    duckcfgWRITE.println(HAStxpwr);
    duckcfgWRITE.println(HASmyCall);
    duckcfgWRITE.println(HASmySSID);
    duckcfgWRITE.println(HASdstcall);
    duckcfgWRITE.println(HASdstssid);
  }
  duckcfgWRITE.close();
}

// Write DUCKHUNT.CFG to SPIFFS
void writeDUCKHUNTCFG(String form_s_msg, String form_s_interval, String form_s_trigger, String form_h_msg, String form_h_interval, String form_h_trigger)
{
  simple_interval = form_s_interval;
  simple_trigger = form_s_trigger;
  simple_message = form_s_msg;
  harder_interval = form_h_interval;
  harder_trigger = form_h_trigger;
  harder_message = form_h_msg;
  File duckhuntWRITE = SPIFFS.open("/duckhunt.cfg", FILE_WRITE);
  if(!duckhuntWRITE){
    Serial.println("ERR: Error opening DUCKHUNT.CFG for write");
    return;
  }
  duckhuntWRITE.println(simple_interval);
  duckhuntWRITE.println(simple_trigger);
  duckhuntWRITE.println(simple_message);
  Serial.println("125: Writing to DUCKHUNT.CFG");
  duckhuntWRITE.println(harder_interval);
  duckhuntWRITE.println(harder_trigger);
  duckhuntWRITE.println(harder_message);
  duckhuntWRITE.close();
}

//Send LoRa message
void startQUACKING(String HASheader, String LORAmessage, int LORAinterval )
{
  LoRa.beginPacket();                        // start packet
  LoRa.setFrequency(HASfreq);
  LoRa.setSignalBandwidth(HASsignalBW);
  LoRa.setCodingRate4(HAScodingrate4);
  LoRa.setSpreadingFactor(HASspreadingFactor);
  LoRa.enableCrc();
  LoRa.setTxPower(HAStxpwr,RF_PACONFIG_PASELECT_PABOOST);
  LoRa.print(HASheader);
  LoRa.write(destinationLORA);               // add destination address
  LoRa.write(localaddressLORA);              // add sender address
  LoRa.write(LORAmessage.length());          // add payload length
  LoRa.print(LORAmessage);                   // add payload
  LoRa.endPacket();                          // finish packet and send it
  OLEDme("Sending ...",1000);
  Serial.print("1230: Sending LoRa ");
  Serial.print(millis());
  Serial.print(" ");
  Serial.println(LORAmessage);
  delay (LORAinterval);                      // seconds
 }

//Receive LoRa Message
void receiveLORA(int packetSize)
{
  // received a packet
  Serial.print("210: Received LoRa packet '");
  if (packetSize == 0) return;               // if there's no packet, return
  // read packet header bytes:
  int recipient = LoRa.read();               // recipient address
  byte sender = LoRa.read();                 // sender address
  byte incomingMsgId = LoRa.read();          // incoming msg ID
  byte incomingLength = LoRa.read();         // incoming msg length
  String incoming = "";                      // payload of packet
  while (LoRa.available())                   // can't use readString() in callback
  {
    incoming += (char)LoRa.read();           // add bytes one by one
  }
  if (incomingLength != incoming.length())   // check length for error
  {
    Serial.println("error: message length does not match length");
    return;                                  // skip rest of function
  }
  HASlastmsg = incoming;                     // Save as last rx message
  OLEDme(incoming, 1000);
  Serial.println();
  Serial.println("Received from: 0x" + String(sender, HEX));
  Serial.println("Received from: 0x" + String(sender, HEX));
  Serial.println("Sent to: 0x" + String(recipient, HEX));
  Serial.println("Message ID: " + String(incomingMsgId));
  Serial.println("Message length: " + String(incomingLength));
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + String(LoRa.packetRssi()));
  Serial.println("Snr: " + String(LoRa.packetSnr()));
  Serial.println();
}

String processor(String var)
{
  if(var == "SIMPLE_TRIGGER")
    return simple_trigger;
  if(var == "SIMPLE_INTERVAL")
    return simple_interval;
  if(var == "SIMPLE_MESSAGE")
    return simple_message;
  if(var == "HARDER_TRIGGER")
    return harder_trigger;
  if(var == "HARDER_INTERVAL")
    return harder_interval;
  if(var == "HARDER_MESSAGE")
    return harder_message;
  if(var == "FREQUENCY")
    return String (HASfreq);
  if(var == "TXPWR")
    return String (HAStxpwr);
  if(var == "MYCALL")
    return HASmyCall;
  if(var == "MYSSID")
    return HASmySSID;
  if(var == "DSTCALL")
    return HASdstcall;
  if(var == "DSTSSID")
    return HASdstssid;
  if(var == "MESSAGE")
    return HASlastTXmsg;
  return String("unknown");
}

//
// SETUP
//
void setup()
{
  // Serial port for debugging purposes
  Serial.begin(115200);
  Serial.println();
  Serial.println();
  Serial.println("000: HASviolet-Duck ESP32");
  Serial.println("===============================");
  
  // Initialize SPIFFS
  if(!SPIFFS.begin(true)){
    Serial.println("ERR: SPIFFS mounting");
    return;
  }
  Serial.println("100: SPIFFs initialized...");

  getDUCKCFG();
  Serial.println("110: DUCK.CFG read...");

  getDUCKHUNTCFG();
  Serial.println("120: DUCKHUNT.CFG read...");

  Heltec.begin(true /*DisplayEnable Enable*/, true /*Heltec.LoRa Disable*/, true /*Serial Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);
  Serial.println("130: ESP32 ready...");
  
  // Initialize LoRa
  LoRa.onReceive(receiveLORA);
  LoRa.receive();
  Serial.println("200: LoRa initialized...");

  // Initialize WiFi AP
  WiFi.softAP(APssid, APpassword);
  IPAddress IP = WiFi.softAPIP();
  Serial.println("300: WiFi AP initialized... ");

  //
  // Webserver pages
  //
  server.on("/",  HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/index.html", "text/html");
    Serial.println("1400: GET /");
  });

  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/style.css", "text/css");
    Serial.println("1410: GET /style.css");
  });

  server.on("/send", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/send.html", String(), false, processor);
    Serial.println("1420: GET /send");
  });

  server.on("/receive", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", HASlastmsg);
    Serial.println("1430: GET /received");
  });

  server.on("/duck", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/duckhunt.html", String(), false, processor);
    Serial.println("1440: GET /duckhunt");
  });

  server.on("/duckcfg", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/duck.cfg", "text/plain");
    Serial.println("1450: Show duck.cfg");
  });

  server.on("/duckhuntcfg", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/duckhunt.cfg", "text/plain");
    Serial.println("1460: Show duckhunt.cfg");
  });

  server.on("/TX", HTTP_GET, [](AsyncWebServerRequest *request) {
    String inputCALL;
    String inputSSID;
    String inputMSG;
    Serial.println("1470: POST /TX");
    inputCALL = request->getParam("dstcall")->value().c_str();
    inputSSID = request->getParam("dstssid")->value().c_str();
    inputMSG = request->getParam("message")->value().c_str();
    String HASheader = HASmyCall + "-" + HASmySSID + ">" + inputCALL + "-" + inputSSID + ":";
    request->send(200, "text/plain", HASheader + inputMSG);
    Serial.println(request->url());
    startQUACKING(HASheader, inputMSG, 0);
  });

  server.on("/DUCKCONFIG", HTTP_GET, [](AsyncWebServerRequest *request) {
    String form_s_msg;
    String form_s_interval;
    String form_s_trigger;
    String form_h_msg;
    String form_h_interval;
    String form_h_trigger;
    Serial.println("1480: UPDATE duck.cfg");
    form_s_msg = request->getParam("simple_message")->value();
    form_s_interval = request->getParam("simple_interval")->value();
    form_s_trigger = request->getParam("simple_trigger")->value();
    form_h_msg = request->getParam("harder_message")->value();
    form_h_interval = request->getParam("harder_interval")->value();
    form_h_trigger = request->getParam("harder_trigger")->value();
    Serial.println(request->url());
    writeDUCKHUNTCFG(form_s_msg, form_s_interval, form_s_trigger, form_h_msg, form_h_interval, form_h_trigger);
    request->send(200, "text/plain", "Success");
  });

  // Start Webserver
  server.begin();
  Serial.println("400: Webserver initialized...");
  
  // Start OLED
  Heltec.display->init();
  Heltec.display->flipScreenVertically();  
  Heltec.display->setFont(ArialMT_Plain_10);

  // Reached this point then all is well - Display HVDN Logo on OLED
  logo();
  Serial.println("500: HVDN Logo displayed (OLED)...");
  Serial.println("===============================");
  Serial.print("999: Duck is awake and available at ");
  Serial.print(IP);
  Serial.print(" on SSID: ");
  Serial.println(APssid);
  Serial.println();
}

// 
// MAIN LOOP
//
void loop(){
  //Timer Trigger Checks
  if (millis() > (harder_trigger.toInt()))
  {
    String HASheader = HASmyCall + "-" + HASmySSID + ">" + HASdstcall + "-" + HASdstssid + ":";
    int HASinterval = harder_interval.toInt();
    startQUACKING(HASheader, harder_message, HASinterval);
    LoRa.receive();                         // go back into receive mode
  }  
  else if (millis() > (simple_trigger.toInt()))
  {
    String HASheader = HASmyCall + "-" + HASmySSID + ">" + HASdstcall + "-" + HASdstssid + ":";
    int HASinterval = simple_interval.toInt();
    startQUACKING(HASheader, simple_message, HASinterval);
    LoRa.receive();                         // go back into receive mode
  } 
}
