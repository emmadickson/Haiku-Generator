

function collectText (){
    var elements = document.getElementsByTagName('*');
    var text = document.body.innerText;
    return text;
}

var text = collectText();
text = text.replace(/(\r\n|\n|\r|\t)/gm," ");

var http = new XMLHttpRequest();
var url = "http://localhost:5000/pipeline";

var params = '{ "text": "' + text + '" }';
http.open("POST", url, true);

//Send the proper header information along with the request
http.setRequestHeader("Content-type", "application/json");

http.onreadystatechange = function() {

//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {

        alert(http.responseText);
        console.log(http.responseText)
    }
}

http.send(params);