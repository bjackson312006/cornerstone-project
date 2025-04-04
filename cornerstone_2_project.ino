void setup() {
    Serial.begin(9600);
  }
  
  void loop() {
    int A0_Value = analogRead(A0);
    int A1_Value = analogRead(A1);
    int A2_Value = analogRead(A2);
    int A3_Value = analogRead(A3);
  
    /* Message Format: {id}:{data} */
    Serial.print("A0:"); Serial.println(A0_Value);
    Serial.print("A1:"); Serial.println(A1_Value);
    Serial.print("A2:"); Serial.println(A2_Value);
    Serial.print("A3:"); Serial.println(A3_Value);
    delay(500); // Send monitor messages every 500ms
  }