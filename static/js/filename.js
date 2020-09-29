'use strict';

console.log('filename loaded');

var inputs = document.querySelectorAll( '.inputfile' );
Array.prototype.forEach.call( inputs, function( input ){
  var label	 = input.nextElementSibling;
  var labelVal = label.innerHTML;
  input.addEventListener( 'change', function( e ){
    var fileName = '';
    fileName = e.target.value.split( '\\' ).pop();
    console.log(fileName);
    if( fileName )
    label.innerHTML = fileName;
    else
    label.innerHTML = labelVal;
  });
});
