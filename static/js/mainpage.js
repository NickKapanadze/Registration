let Token = getCookie("Token");
const IDKYBs = document.querySelectorAll('.IDKYB');
const IKUTexts = document.querySelectorAll('.IKUText');
  DINY = DINYf(Token)
  if (DINY == false){
    IDKYBs.forEach(IDKYB => {
      IDKYB.style.display = 'block';
    });
    IKUTexts.forEach(IKUText => {
      IKUText.style.display = 'none';
    });
  } else {
    IDKYBs.forEach(IDKYB => {
      IDKYB.style.display = 'none';
    });
    IKUTexts.forEach(IKUText => {
      IKUText.style.display = 'block';
    });
    fetch(`/readname?userT=${Token}`).then((response) => {
      response.text().then((txt) => {
        var username = txt
        document.getElementById("UsernameText").innerHTML = username;
      })
    })
  }