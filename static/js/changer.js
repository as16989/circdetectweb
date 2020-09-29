
  var button = document.getElementById('labeltestbtn');
  var p  = document.getElementById('labeltest');

  console.log('this happened');

  button.addEventListener('click', function (e) {
    e.preventDefault();

    p.innerHTML = "hello world";
});
