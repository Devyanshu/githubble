function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
$(document).ready(function () {
    $("#plot").hide();
    $('#subuser').on('submit', function (event) {
        on();
        $("#result").html('');
        $("#error").html('');
        $("#plot").html('');
        $("#plot").hide();
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
                if (data.map) {
                    if (data.map.flag) {
                        $("#plot").html('<div><h4 style="text-align: center"> Day wise contributions </h4><div id="data-plot"></div></div>')
                        $("#plot").show();
                        Morris.Bar(data.map.data);
                    }
                }
            });

        event.preventDefault();
    });
});