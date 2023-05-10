#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

const char *ssid = "Nova-m";
const char *password = "848685M8";

ESP8266WebServer server(80);

const int MOTOR1_FORWARD_PIN = D2;
const int MOTOR1_REVERSE_PIN = D0;
const int MOTOR2_FORWARD_PIN = D1;
const int MOTOR2_REVERSE_PIN = D8;

void handleRoot()
{
    String html = R"html(
    <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/html">
    <head>
        <meta charset="UTF-8">
        <meta content="IE=edge" http-equiv="X-UA-Compatible">

        <title>Remote Control Line Follower Robot</title>
        <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
            integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" rel="stylesheet">
        <link crossorigin="anonymous" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
            integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w=="
            rel="stylesheet"/>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }


            span.label {
                font-size: 60px;
                color: #8e8e8e;
            }

            div.rounded-bg {
                background: #d9d9d9;
                border-radius: 50px;

            }

            i.control-icon {
                font-size: 24px;
                color: #2e2e2e;
                width: 100%;
                text-align: center;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <div class="d-flex  mt-4 justify-content-between px-2">


            <div class="d-flex flex-column rounded-bg py-5 px-3 justify-content-center align-items-center">
                <i class="fas fa-chevron-up py-5 control-icon" id="motor1-forward"></i>
                <span class="label py-5">Motor1</span>
                <i class="fas fa-chevron-down py-5 control-icon" id="motor1-backward"></i>
            </div>

            <div class="d-flex flex-column rounded-bg py-5 px-3 justify-content-center align-items-center">
                <i class="fas fa-chevron-up py-5 control-icon" id="motor2-forward"></i>
                <span class="label py-5">Motor2</span>
                <i class="fas fa-chevron-down py-5 control-icon" id="motor2-backward"></i>
            </div>


        </div>
    </div>
    <script>
        const motor1ForwardButton = document.getElementById('motor1-forward');
        motor1ForwardButton.addEventListener('touchstart', function () {
            sendRequest('/motor1_forward', 1);
            console.log("pressed");
        });
        motor1ForwardButton.addEventListener('touchend', function () {
            sendRequest('/motor1_forward', 0);
        });

        const motor2ForwardButton = document.getElementById('motor2-forward');
        motor2ForwardButton.addEventListener('touchstart', function () {
            sendRequest('/motor2_forward', 1);
        });
        motor2ForwardButton.addEventListener('touchend', function () {
            sendRequest('/motor2_forward', 0);
        });

        const motor1ReverseButton = document.getElementById('motor1-backward');
        motor1ReverseButton.addEventListener('touchstart', function () {
            sendRequest('/motor1_reverse', 1);
        });
        motor1ReverseButton.addEventListener('touchend', function () {
            sendRequest('/motor1_reverse', 0);
        });

        const motor2ReverseButton = document.getElementById('motor2-backward');
        motor2ReverseButton.addEventListener('touchstart', function () {
            sendRequest('/motor2_reverse', 1);
        });
        motor2ReverseButton.addEventListener('touchend', function () {
            sendRequest('/motor2_reverse', 0);
        });

        function sendRequest(url, state) {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url + '?state=' + state, true);
            xhr.send();
        }
    </script>
    </body>
    </html>
  )html";
    server.send(200, "text/html", html);
}

void handleMotor1Forward()
{
    int state = server.arg("state").toInt();
    Serial.println(state);

    digitalWrite(MOTOR1_FORWARD_PIN, state);
    server.send(200, "text/plain", "OK");
}

void handleMotor1Reverse()
{
    int state = server.arg("state").toInt();
    digitalWrite(MOTOR1_REVERSE_PIN, state);
    server.send(200, "text/plain", "OK");
}

void handleMotor2Forward()
{
    int state = server.arg("state").toInt();
    digitalWrite(MOTOR2_FORWARD_PIN, state);
    server.send(200, "text/plain", "OK");
}

void handleMotor2Reverse()
{
    int state = server.arg("state").toInt();
    digitalWrite(MOTOR2_REVERSE_PIN, state);
    server.send(200, "text/plain", "OK");
}

void setup()
{
    Serial.begin(115200);
    delay(10);

    pinMode(MOTOR1_FORWARD_PIN, OUTPUT);
    pinMode(MOTOR1_REVERSE_PIN, OUTPUT);
    pinMode(MOTOR2_FORWARD_PIN, OUTPUT);
    pinMode(MOTOR2_REVERSE_PIN, OUTPUT);

    WiFi.begin(ssid, password);
    Serial.println("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    server.on("/", handleRoot);
    server.on("/motor1_forward", handleMotor1Forward);
    server.on("/motor1_reverse", handleMotor1Reverse);
    server.on("/motor2_forward", handleMotor2Forward);
    server.on("/motor2_reverse", handleMotor2Reverse);

    server.begin();

    Serial.println("Server started");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop()
{
    server.handleClient();
}
