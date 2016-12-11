// content.js

function collectText (){
    var elements = document.getElementsByTagName('*');
    var text = document.body.innerText;
    return text;
}
console.log("loaded");
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
      console.log("in");
      var text = collectText();
      text = text.replace(/(\r\n|\n|\r|\t)/gm," ");
      text = encodeURI(text)
      console.log(text);
      var http = new XMLHttpRequest();
      var url = "http://localhost:5000/pipeline";

      var params = '{ "text": "' + text + '" }';
      http.open("POST", url);

      //Send the proper header information along with the request
      http.setRequestHeader("Content-type", "application/json");

      http.send(params);
      console.log("sent")
      http.onreadystatechange = function() {
      //Call a function when the state changes.
      if (http.readyState == XMLHttpRequest.DONE) {
          alert(http.responseText);
          console.log(http.responseText);}
      }
    }
  }
);
