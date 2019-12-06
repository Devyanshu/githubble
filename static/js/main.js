function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
$(document).ready(function () {
    $('#subuser').on('submit', function (event) {
        on();
        $("#result").html('');
        $("#error").html('');
        $.ajax({
            data: {
                username: $("#username").val(),
            },
            type: "POST",
            url: '/data'
        })
            .done(function (data) {
                if (data.error) {
                    off();
                    var show = "<h3>" + data.error + "</h3>"
                    $("#error").html(show);
                }
                else {
                    off();
                    var show = data.value;
                    $("#result").html(show);
                }
            });

        event.preventDefault();
    });
});