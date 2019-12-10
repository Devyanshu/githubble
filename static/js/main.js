function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
$(document).ready(function () {
    $("#days-plot").hide();
    $("#months-plot").hide();
    $('#subuser').on('submit', function (event) {
        on();
        $("#result").html('');
        $("#error").html('');
        $("#days-plot").html('');
        $("#days-plot").hide();
        $("#months-plot").html('');
        $("#months-plot").hide();
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
                if (data.days) {
                    if (data.days.flag) {
                        $("#days-plot").html('<div><h4 style="text-align: center"> Day wise contributions </h4><div id="data-plot-days"></div></div>')
                        $("#days-plot").show();
                        Morris.Bar(data.days.data);
                    }
                }
                if (data.months) {
                    if (data.months.flag) {
                        $("#months-plot").html('<div><h4 style="text-align: center"> Month wise contributions </h4><div id="data-plot-months"></div></div>')
                        $("#months-plot").show();
                        Morris.Bar(data.months.data);
                    }
                }
            });

        event.preventDefault();
    });
});