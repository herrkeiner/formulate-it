// Set the focus when the page is loaded
document.getElementById('navbar').focus();

function dataParser(event) {
  var keyPressed = event.which || event.keyCode;

  navbar = document.getElementById('navbar');

  // is it enter?
  if (keyPressed == 13) {
    // Let's create our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

      }
    }
    xhttp.open('GET', 'parser?n=' + navbar.value, true);
    xhttp.send();
  }
  else if (keyPressed < 48 || keyPressed > 57) { // Is NOT a number?
    var i = 0, chCode = 0, nQuery = '';
    for(i in navbar.value) {
      chCode = navbar.value.charCodeAt(i);
      if (chCode >= 48 && chCode <= 57) {
        nQuery += navbar.value[i];
      }
    }
    navbar.value = nQuery;
  }
}
