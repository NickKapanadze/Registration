let Token = getCookie("Token");
DINY = DINYf(Token)
if (DINY == false){
    window.location.href = '/';
} else {
    //pass
};
header(Token);