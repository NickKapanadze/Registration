document.getElementById("Form1").onsubmit = function() {submit1()};

var form = document.getElementById("Form1");
function handleForm(event) { event.preventDefault(); } 
form.addEventListener('submit', handleForm);