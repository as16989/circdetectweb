function changeTab() {
  var choose = document.getElementById("choose");
  var url = document.getElementById("url");
  if (choose.style.display === "none") {
    choose.style.display = "block";
    url.style.display = "none";
  } else {
    choose.style.display = "none";
    url.style.display = "block";
  }
}
