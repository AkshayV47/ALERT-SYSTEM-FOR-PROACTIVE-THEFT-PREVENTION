-----------------README: ALERT SYSTEM FOR PROACTIVE THEFT PREVENTION + GPS TRACKER------------------

IoT security system with ESP32-CAM streaming images every 20s to Flask AI server. 
YOLOv5 detects weapons, face recognition identifies suspects from central database. 
NEW: MicroPython GPS+GSM+MQTT tracker sends location SMS on threat alerts via test.mosquitto.org broker to Indian number (+91).

Dual Architecture
text
ESP32-CAM → Flask AI (Weapons+Faces) → MQTT Broker → ESP32 GPS Tracker → SMS
Components
Vision: ESP32-CAM → Python (YOLOv5+face_recognition) → Alerts​

Tracker: ESP32 UART1(GSM:TX4/RX5)+UART1(GPS:TX8/RX9) → Google Maps SMS

Comms: MQTT send_data topic triggers +918667517648 SMS w/ live location

Integration Flow
AI detects threat → MQTT publish

GPS tracker receives → Extracts lat/lon via AT+CGNSINF

Auto-SMS: https://maps.google.com/?q=lat,lon

Complete proactive theft prevention: See threat + track thief instantly!
