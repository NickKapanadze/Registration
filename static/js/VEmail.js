let Token = getCookie("Token");
DINY = DINYf(Token)
if (DINY == false){
    window.location.href = '/';
} else {
    fetch(`/SendEVcode?userT=${Token}`)
}

function CheckEvCode(Token){
    Evcodev = document.getElementById("CodeInput").value
    fetch(`/checkEVcode?userT=${Token}&Evcodev=${Evcodev}`).then((response) => {
        response.text().then((txt) => {
            if (txt == "False"){
                alert("Verification Code is not correct.")
            } else {
                alert("Email is successfully verified.")
                sleep(300)
                window.location.href = '/';
            }
        })
    })  
}