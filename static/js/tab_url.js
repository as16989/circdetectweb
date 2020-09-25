function tab_url() {
  var choose = document.getElementById("choose");
  var url = document.getElementById("url");

  choose.style.display = "none";
  url.style.display = "block";

  fileButton.style.backgroundColor = "black"
  fileButton.style.color = "white"
  fileButton.style.border = "2px solid black"

  urlButton.style.backgroundColor = "white"
  urlButton.style.color = "black"
  urlButton.style.border = "2px solid black"

  $("#fileButton").hover(function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
    }, function(){
    $(this).css("background-color", "black");
    $(this).css("color", "white");
  });

  $("#urlButton").hover(function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
    }, function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
  });

}
