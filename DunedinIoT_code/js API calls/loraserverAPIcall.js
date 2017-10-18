function onJWT(jwt){
  var xhr2 = new XMLHttpRequest();
  xhr2.open("GET", "https://iot.op-bit.nz/api/applications/3/nodes?", true);
  xhr2.setRequestHeader("Content-type", "application/json");
  xhr2.onload = function (e) {
    if (xhr2.readyState === 4) {
      if (xhr2.status === 200) {
        console.log(xhr2.responseText);
        console.log(xhr2.response);
      } else {
        console.error(xhr2.statusText);
	    console.log(xhr2.responseText);
      }
    }
  };
  xhr2.onerror = function (e) {
    console.error(xhr.statusText);
  };
  xhr2.send(jwt);
}

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();
xhr.open("POST", "https://iot.op-bit.nz/api/internal/login", true);
//Send the proper header information along with the request
xhr.setRequestHeader("Content-type", "application/json");
var login = '{ "password": "Bugger0ff", "username": "admin"}';
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      console.log(xhr.response);
      onJWT(xhr.response);
    } else {
      console.error(xhr.statusText);
	  console.log(xhr.responseText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(login);
//https://iot.op-bit.nz/api/applications/3/nodes?limit=100&offset=1