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
    {
      /* This section cleans the navbar input with the purpose to only
        allow the mathematical symbols. */
                  // SPC, !, (, ), *, +, -, /, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ^
      var allowedCh = [32,33,40,41,42,43,45,47,48,49,50,51,52,53,54,55,56,57,94]
      var i = 0, chCode = 0, nQuery = '';
      // Checks every single character of the navbar.input
      for (i in navbar.value) {
        chCode = navbar.value.charCodeAt(i);
        // Verifies if the retrieved ch is within the allowed array
        if (allowedCh.includes(chCode))
          nQuery += navbar.value[i];
    }
    // Updates the navbar value for the new cleaned value
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
              infoHeader.innerHTML = 'The querry must be a <span style="text-decoration: underline;">natural number</span>!'
              break;
            }

            infoHeader.innerHTML = '<span style="color: #99ff8e; text-decoration: underline overline;">' + jObj.rNumber+'</span>';

            // is it a prime number?
            if (jObj.isPrime) {
              var a = document.getElementById('pni-h3');
              a.innerHTML = 'Yes';
              a.style.color = 'hsl(109, 87%, 70%)';

            } else {
              var a = document.getElementById('pni-h3');
              a.innerHTML = 'No';
              a.style.color = 'rgb(176, 176, 176)';
            }
            // format the factoration result to a str
            for (var key in jObj.fResult) {
              str += '<span style="color:#68ffea;">' + key + '</span>' + '^' + '<span style="color:#ff5e45;">' + jObj.fResult[key] + '</span>' + '  x  ';
            }

            document.getElementById('factorials').innerHTML = str.slice(0, -3);

            if (jObj.isPalin) {
              var a = document.getElementById('palindromic');
              a.innerHTML = 'Yes';
              a.style.color = 'hsl(109, 87%, 70%)';
            } else {
              var a = document.getElementById('palindromic');
              a.innerHTML = 'No';
              a.style.color = 'rgb(176, 176, 176)';
            }

            for (
                  var i = 0, h3lements = document.getElementsByClassName('section-data');
                  i <= h3lements.length - 1;
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
