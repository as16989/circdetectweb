$(function() {
    $('#submit').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#choose')[0]);
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
            console.log(data['path'])
            console.log('Success!');
            // $("#resultFilename").text(data['name']);
            // $("#resultFilesize").text(data['size']);
            $("#result").attr('src', data['path']);
            $("#loader").css("display", "none");
        }).fail(function(data){
            alert('error!');
        });
    });
});
