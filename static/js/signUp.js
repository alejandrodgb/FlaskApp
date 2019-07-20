$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if (response === '200') {
                    location.href = "https://google.com"
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});