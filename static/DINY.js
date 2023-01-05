function DINYf(Token){
    let DINY = null
    if (Token == null) {
        document.cookie = "Token=;";
        DINYf();
    } else {
        if (Token == "") {
            return false
        } else {
            return true
        }
    }
}