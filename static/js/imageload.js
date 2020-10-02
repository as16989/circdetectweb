$(function() {
    $('#submitbutton1').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#choose')[0]);
        $('#imagePlaceholder').empty();
        $.ajax({
            type: 'POST',
            url: '/uploadfile',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log(data['paths']);
            console.log('Success!');
            resultsArray = data['paths'];


            if(resultsArray[0] == 'nothing') {
              var no_img_str = $('<p/>', {
                text: "Please choose a file!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if(resultsArray[0] == 'badfile') {
              var no_img_str = $('<p/>', {
                text: "Please choose an image file!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if(resultsArray[0] == 'toolarge') {
              var no_img_str = $('<p/>', {
                text: "The chosen file is too large!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if(resultsArray[0] == 'toobig') {
              var no_img_str = $('<p/>', {
                text: "Please choose an image smaller than 1024x1024!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if (resultsArray.length > 0) {

              var click_to_dl = $('<p/>', {
                text: "Click on the image you would like to download:",
              }).appendTo($('#imagePlaceholder'));

              for (var i = 0; i < resultsArray.length; i++) {

                var link = $('<a/>', {
                  id:   'link' + i,
                  href: Flask.url_for("download", {"filename": resultsArray[i].slice(10)})
                }).appendTo($('#imagePlaceholder'));

                var img = $('<img/>', {
                  id:   'result' + i,
                  src:  resultsArray[i],
                  alt:  'Result ' + i
                }).appendTo($(link));

                var num = $('<p/>', {
                  text: "Result " + i,
                }).appendTo($('#imagePlaceholder'));

                var br = $('<br/><br/>').appendTo($('#imagePlaceholder'));

              }
            }
            else {
              var no_img_str = $('<p/>', {
                text: "No circles found in the input image.",
              }).appendTo($('#imagePlaceholder'));
            }
            $("#loader").css("display", "none");
        }).fail(function(data){
            alert('error!');
        });
    });
});

$(function() {
    $('#submitbutton2').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#url')[0]);
        $('#imagePlaceholder').empty();
        $.ajax({
            type: 'POST',
            url: '/uploadfile',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log(data['paths']);
            console.log('Success!');
            resultsArray = data['paths'];

            if(resultsArray[0] == 'nothing') {
              var no_img_str = $('<p/>', {
                text: "Please paste a valid image URL!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if(resultsArray[0] == 'toobig') {
              var no_img_str = $('<p/>', {
                text: "Please choose an image smaller than 1024x1024!",
              }).appendTo($('#imagePlaceholder'));
            }

            else if (resultsArray.length > 0) {
              for (var i = 0; i < resultsArray.length; i++) {

                var link = $('<a/>', {
                  id:   'link' + i,
                  href: Flask.url_for("download", {"filename": resultsArray[i].slice(10)})
                }).appendTo($('#imagePlaceholder'));

                var img = $('<img/>', {
                  id:   'result' + i,
                  src:  resultsArray[i],
                  alt:  'Result ' + i
                }).appendTo($(link));

                var num = $('<p/>', {
                  text: "Result " + i,
                }).appendTo($('#imagePlaceholder'));

                var br = $('<br/>').appendTo($('#imagePlaceholder'));

              }
            }
            else {
              var no_img_str = $('<p/>', {
                text: "No circles found in the input image.",
              }).appendTo($('#imagePlaceholder'));
            }
            $("#loader").css("display", "none");
        }).fail(function(data){
            alert('error!');
        });
    });
});
