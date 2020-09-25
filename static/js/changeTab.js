function changeTab() {
  var choose = document.getElementById("choose");
  var url = document.getElementById("url");
  var fileButton = document.getElementById("fileButton");
  var urlButton  = document.getElementById("urlButton");

  fileButton.onclick = function() {
    choose.style.display = "block";
    url.style.display = "none";

    fileButton.style.backgroundColor = "black"
    fileButton.style.color = "white"
    fileButton.style.border = "0 none"

    urlButton.style.backgroundColor = "white"
    urlButton.style.color = "black"
    urlButton.style.border = "2px solid black"
  };

  urlButton.onclick = function() {
    console.log('hi');
    choose.style.display = "none";
    url.style.display = "block";

    fileButton.style.backgroundColor = "white"
    fileButton.style.color = "black"
    fileButton.style.border = "2px solid black"

    urlButton.style.backgroundColor = "black"
    urlButton.style.color = "white"
    urlButton.style.border = "0 none"
  };
}
