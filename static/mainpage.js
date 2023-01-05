let Token = getCookie("Token");
  DINY = DINYf(Token)
  if (DINY == false){
    document.getElementById("doiknowyou").style.display = "block";
    document.getElementById("Iknowyou").style.display = "none";
  } else {
    document.getElementById("doiknowyou").style.display = "none";
    document.getElementById("Iknowyou").style.display = "block";
    fetch(`/readname?userT=${Token}`).then((response) => {
      response.text().then((txt) => {
        var username = txt
        document.getElementById("Iknowyou").innerHTML = "Welcome " + username;
      })
    })
  }