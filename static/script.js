function buttonDown(button) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(button);
}

function buttonUp() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("stop");
}

function setSpeed(value) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("speed=" + value);
    document.getElementById("speedValue").textContent = Math.round(value * 100) + "%";
}

function adjustCalibration(motor, delta) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
    var param = "calibrate_" + motor + "=" + delta;
    xhttp.send(param);
    
    // Update display with new value
    var elementId = motor === 'left' ? 'calLeftValue' : 'calRightValue';
    var currentValue = parseFloat(document.getElementById(elementId).textContent);
    var newValue = currentValue + delta;
    
    // Clamp to valid range
    newValue = Math.max(-0.08, Math.min(0.08, newValue));
    document.getElementById(elementId).textContent = newValue.toFixed(3);
}
