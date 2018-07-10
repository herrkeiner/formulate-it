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
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText);
    }
  }
  xhttp.open('GET', 'parser&q=' + navbar.value, true);
  xhttp.send();
}
