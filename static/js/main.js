'use strict';
/* global XMLHttpRequest addEventListener Chart Paho */

const usernameText = document.querySelector('#username');
const passwordText = document.querySelector('#password');
const connectButton = document.querySelector('#connectMQTT');
let mqttClient;

if (connectButton) {
  addEventListener('click', startConnect);
}

// Called after form input is processed

function startConnect() {
  // connectButton.disabled = true; // prevent double subscription
  const host = 'itwot.mooo.com';
  const port = 8083;
  const clientID = `roller-webpage-${parseInt(Math.random() * 4095)}`;

  // Initialize new Paho client connection
  mqttClient = new Paho.Client(host, port, clientID);

  // Set callback handlers
  mqttClient.onConnectionLost = onConnectionLost;
  mqttClient.onMessageArrived = onMessageArrived;

  // Connect the client, if successful, call onConnect function
  mqttClient.connect({
    onSuccess: onConnect,
    userName: usernameText.value,
    password: passwordText.value,
    useSSL: true
  });
}

// Called when the client connects
function onConnect() {
  const topic = 'au701034/airquality';
  console.log('Now connected to ' + topic);
  mqttClient.subscribe(topic);
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
  console.log('onConnectionLost: Connection Lost');
  if (responseObject.errorCode !== 0) {
    console.log(`onConnectionLost: ${responseObject.errorMessage}`);
  }
}

// To get the date to the right sqlite3-format
function getCurrentDate() {
  var now = new Date(); 
  var year    = now.getFullYear();
  var month   = now.getMonth()+1; 
  var day     = now.getDate();
  var hour    = now.getHours();
  var minute  = now.getMinutes();
  var second  = now.getSeconds(); 
  if(month.toString().length == 1) {
        month = '0'+month;
  }
  if(day.toString().length == 1) {
        day = '0'+day;
  }   
  if(hour.toString().length == 1) {
        hour = '0'+hour;
  }
  if(minute.toString().length == 1) {
        minute = '0'+minute;
  }
  if(second.toString().length == 1) {
        second = '0'+second;
  }   
  var dateTime = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second;   

  return dateTime;
}


// Called when a message arrives
function onMessageArrived(message) {
  const newDataInput = document.createElement("div");
  newDataInput.className = "datainputs";

  const newAir = JSON.parse(message.payloadString);
  let tvoc = newAir.tvoc;
  let eco2 = newAir.eco2;
  let date = getCurrentDate();
  console.log(`MQTT: New Data: ${newAir}`);

  const newtvoc = document.createElement("p");
  newtvoc.textContent = "TVOC: " + tvoc;
  newtvoc.setAttribute('class', 'tvoc');
  newDataInput.append(newtvoc);
  
  const neweco2 = document.createElement("p");
  neweco2.textContent = "eCO2: " + eco2;
  neweco2.setAttribute('class', 'eco2');
  newDataInput.append(neweco2);

  const newdate = document.createElement("p");
  newdate.textContent = "Date: " + date;
  newdate.setAttribute('class', 'date');
  newDataInput.append(newdate);

  document.getElementById('main_data').prepend(newDataInput);
}