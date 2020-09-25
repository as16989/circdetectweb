function tab_file() {
  var choose = document.getElementById("choose");
  var url = document.getElementById("url");

  choose.style.display = "block";
  url.style.display = "none";

  fileButton.style.backgroundColor = "white"
  fileButton.style.color = "black"
  fileButton.style.border = "2px solid black"

  urlButton.style.backgroundColor = "black"
  urlButton.style.color = "white"
  urlButton.style.border = "2px solid black"

  $("#urlButton").hover(function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
    }, function(){
    $(this).css("background-color", "black");
    $(this).css("color", "white");
  });

  $("#fileButton").hover(function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
    }, function(){
    $(this).css("background-color", "white");
    $(this).css("color", "black");
  });


}
