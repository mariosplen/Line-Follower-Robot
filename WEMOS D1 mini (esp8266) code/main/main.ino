#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef APSSID
#define APSSID "RC-Line-Follower"
#define APPSK "mariosplen"
#endif

const char *ssid = APSSID;
const char *password = APPSK;

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


        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                user-select: none;
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

            .d-flex {
                display: flex !important;
            }

            .justify-content-between {
                justify-content: space-between !important;
            }

            .flex-column {
                flex-direction: column !important;
            }

            .px-3 {
                padding-right: 1rem !important;
                padding-left: 1rem !important;
            }

            .justify-content-center {
                justify-content: center !important;
            }

            .py-5 {
                padding-top: 3rem !important;
                padding-bottom: 3rem !important;
            }

            .container {
                width: 100%;
                margin-right: auto;
                margin-left: auto;
            }

            @media (min-width: 576px) {
                .container {
                    max-width: 540px;
                }
            }

            @media (min-width: 768px) {
                .container {
                    max-width: 720px;
                }
            }

            @media (min-width: 992px) {
                .container {
                    max-width: 960px;
                }
            }

            @media (min-width: 1200px) {
                .container {
                    max-width: 1140px;
                }
            }

            @media (min-width: 1400px) {
                .container {
                    max-width: 1320px;
                }
            }

        </style>
    </head>
    <body>
    <div class="container">
        <div class="d-flex   justify-content-between ">


            <div class="d-flex flex-column rounded-bg  px-3 justify-content-center ">
                <i class=" py-5 control-icon" id="motor1-forward">▲</i>
                <span class="label py-5">Motor1</span>
                <i class="  py-5 control-icon" id="motor1-backward">▼</i>
            </div>

            <div class="d-flex flex-column rounded-bg  px-3 justify-content-center ">
                <i class=" py-5 control-icon" id="motor2-forward">▲</i>
                <span class="label py-5">Motor2</span>
                <i class="  py-5 control-icon" id="motor2-backward">▼</i>
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
    // Serial.println(state);

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
    delay(1000);
    // Serial.begin(115200);

    pinMode(MOTOR1_FORWARD_PIN, OUTPUT);
    pinMode(MOTOR1_REVERSE_PIN, OUTPUT);
    pinMode(MOTOR2_FORWARD_PIN, OUTPUT);
    pinMode(MOTOR2_REVERSE_PIN, OUTPUT);

    // Serial.print("Configuring access point...");

    IPAddress ip(192, 168, 1, 1);       // Set the IP address of the access point
    IPAddress subnet(255, 255, 255, 0); // Set the subnet mask
    IPAddress gateway(192, 168, 1, 1);  // Set the gateway address (same as IP address)

    WiFi.softAPConfig(ip, gateway, subnet); // Configure the access point with the new settings
    // You can add a password parameter if you want the AP to be secured.
    WiFi.softAP(ssid); // Start the access point with the new settings

    IPAddress myIP = WiFi.softAPIP();
    // Serial.print("AP IP address: ");
    // Serial.println(myIP);
    server.on("/", handleRoot);
    server.on("/motor1_forward", handleMotor1Forward);
    server.on("/motor1_reverse", handleMotor1Reverse);
    server.on("/motor2_forward", handleMotor2Forward);
    server.on("/motor2_reverse", handleMotor2Reverse);
    server.begin();
    // Serial.println("HTTP server started");
}

void loop()
{
    server.handleClient();
}
