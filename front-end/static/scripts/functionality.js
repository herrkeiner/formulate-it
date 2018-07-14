// Global variables
navbar = document.getElementById('navbar');

// Set the focus when the page is loaded
navbar.focus();

function keyParser(event) {
  var keyPressed = event.which || event.keyCode;

  // is it enter?
  if (keyPressed == 13)
    ajaxRequest();
  else
    if (keyPressed < 48 || keyPressed > 57) { // Is NOT a number?
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
      // Request received
      case 4:
      // is its status OK?
        if (this.status == 200) {
            var jObj = JSON.parse(this.responseText);
            var str = '';

            if (jObj.fResult == 'NaN') {
              infoHeader.innerHTML = 'The querry ' + jObj.rNumber + ' is not a number.'
              break;
            }

            infoHeader.innerHTML = 'Number: ' + jObj.rNumber;

            // format the factoration result to a str
            for (var key in jObj.fResult) {
              str += key + '^' + jObj.fResult[key] + ' x ';
            }

            document.getElementById('factorials').innerHTML = str.slice(0, -3);

            if ( jObj.isPalin == 'False' )
              document.getElementById('palindromic').innerHTML = 'No';
            else
              document.getElementById('palindromic').innerHTML = 'Yes';

            for (
                  var i = 0, h3lements = document.getElementsByClassName('section-data');
                  i <= h3lements.length;
                  i++
                )
                h3lements[i].style.display = 'block';
                
        }
        break;
    }
  }

  xhttp.open('GET', 'parser&q=' + navbar.value, true);
  xhttp.send();
}
