// Global variables
navbar = document.getElementById('navbar');

// Set the focus when the page is loaded
navbar.focus();

function keyParser(event) {
  var keyPressed = event.which || event.keyCode;

  // is it enter?
  if (keyPressed == 13) {
    ajaxRequest();
  }
  else if (keyPressed < 48 || keyPressed > 57) { // Is NOT a number?
    var i = 0, chCode = 0, nQuery = '';
    for (i in navbar.value) {
      chCode = navbar.value.charCodeAt(i);
      if (chCode >= 48 && chCode <= 57) {
        nQuery += navbar.value[i];
      }
    }
    navbar.value = nQuery;
  }
}

function ajaxRequest() {
  var xhttp = new XMLHttpRequest();
  var infoHeader = document.getElementById('infoHeader');

  xhttp.onreadystatechange = function() {
    switch(this.readyState) {
      case 2:
        infoHeader.innerHTML = "Requesting . . .";
        infoHeader.style.display = "block";
        break;
      case 4:
        if (this.status == 200) {
            var jObj = JSON.parse(this.responseText);
            infoHeader.innerHTML = 'Number: ' + jObj.rNumber;
            document.getElementById('factorials').innerHTML = jObj.fResult;
            console.log(jObj);
        }
        break;
    }
  }

  xhttp.open('GET', 'parser&q=' + navbar.value, true);
  xhttp.send();
}
