function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}

function sing_plu(val, sing, plu) {
    if (val == 1)
        return '1 ' + sing;
    else
        return val + ' ' + plu;
}
$(document).ready(function () {
    $("#avatar").hide();
    $("#days-plot").hide();
    $("#months-plot").hide();
    $('#subuser').on('submit', function (event) {
        on();
        $("#result").hide();
        $("#error").hide();
        $("#days-plot").html('');
        $("#days-plot").hide();
        $("#months-plot").html('');
        $("#months-plot").hide();
        $("#last-contrib").text('');
        $("#repos").text('');
        $("#tc").text('');
        $("#name").text('');

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
                    $("#error").html(data.error);
                    $("#error").show();
                }
                else {
                    off();
                    var show = data.value;
                    $("#avatar").attr("src", data.value.avatar);
                    $("#avatar").show();
                    $("#name").text(data.value.name);

                    var repos = data.value.repos;
                    $("#repos").text(sing_plu(repos, 'repository', 'repositories'));
                    var tc = data.value.total_contribution;
                    $("#tc").text(sing_plu(tc, 'contribution', 'contributions'));
                    // $("#result").html(show);

                    if (data.value.last_contribution) {
                        var lc = data.value.last_contribution;
                        $("#last-contrib").text('Last contribution\n' + lc);
                    }
                    var td = data.value.total_days
                    $("#total_days").text('In the last ' + td + ' days');


                    $('#result').show();
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