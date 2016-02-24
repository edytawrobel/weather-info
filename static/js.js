$(function() {
    $('#sendEmail').click(function() {

        $.ajax({
            url: '/user',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log("successfull", response);
            },
            error: function(error) {
                console.log("wrong", error);
            }
        });
    });
});
