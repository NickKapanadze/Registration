function ReadUN(Token) {
    fetch(`/readname?userT=${Token}`).then((response) => {
        response.text().then((txt) => {
            let RUm = txt
            document.getElementById("username_text").innerHTML = RUm;
        });
    });
};
function ReadRM(Token) {
    fetch(`/readreadme?userT=${Token}`).then((response) => {
        response.text().then((txt) => {
            let Rrm = txt
            document.getElementById("Read_me_box").value = Rrm;
        });
    });
};

let Token = getCookie("Token");
DINY = DINYf(Token)
if (DINY == false){
    window.location.href = '/';
} else {
    ReadUN(Token);
    ReadRM(Token);
};

function updateRM(Token) {
    let nRMTXT = document.getElementById("Read_me_box").value
    fetch(`/updatereadme?nRM=${nRMTXT}&userT=${Token}`);
    alert("done!");
};