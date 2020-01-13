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
    $("#result").hide();
    $("#fnf").hide();
    $('#subuser').on('submit', function (event) {
        on();
        $("#result").hide();
        $("#error").hide();
        $("#days-plot").html('');
        $("#days-plot").hide();
        $("#months-plot").html('');
        $("#months-plot").hide();
        $("#streak-plot").html('');
        $("#streak-plot").hide();
        $("#last-contrib").text('');
        $("#repos").text('');
        $("#day-contributions").text('');
        $("#name").text('');
        $("#gap").text('');
        $("#streak").text('');
        $("#avg_commits").text('');
        $("#max_activity").text('');
        $("#joined").text('');
        $("#follwers").text('');
        $("#following").text('');
        $('#social_stats').hide();
        $('#fnf').hide();
        $('#ogs').hide();
        $('#langc').hide();
        $('#repo_info').hide();

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
                    $("#avatar").attr("src", data.value.avatar);
                    $("#profileUrl").attr("href", data.value.profileUrl);

                    $("#name").text(data.value.name);

                    var repos = data.value.repos;
                    $("#repos").text(sing_plu(repos, 'repository', 'repositories'));

                    const tc = data.value.total_contribution;
                    const days = data.value.days_contributed;
                    const txt = sing_plu(tc, 'contribution', 'contributions') + ' in ' + sing_plu(days, 'day', 'days');
                    $("#day-contributions").text(txt);

                    if (data.value.last_contribution) {
                        var lc = data.value.last_contribution;
                        $("#last-contrib").text('Last contribution\n' + lc);
                    }
                    var td = data.value.total_days
                    $("#total_days").text('In the last ' + td + ' days');

                    const gap = data.value.longest_gap;
                    $("#gap").text('Longest gap of ' + sing_plu(gap, 'day', 'days'));

                    const streak = data.value.longest_streak;
                    $("#streak").text('Longest streak of ' + streak);
                    if (data.value.avg_commits) {
                        var ac = data.value.avg_commits;
                        $("#avg_commits").text('with average of ' + ac);
                    }
                    if (data.value.max_activity) {
                        const num = data.value.max_activity.num
                        const act_day = data.value.max_activity.day
                        $("#max_activity").text('Maximum ' + sing_plu(num, 'contribution', 'contributions') + ' on ' + act_day);
                    }
                    if (data.value.joined)
                        $("#joined").text('Joined Github on ' + data.value.joined);
                    if (data.value.followers && data.value.following) {
                        $("#followers").text(sing_plu(data.value.followers, 'follower', 'followers'));
                        $("#following").text(sing_plu(data.value.following, 'following', 'following'));
                        $('#social_stats').show();
                    }
                    $('#result').show();
                    $('#profileUrl').show();
                    $("#avatar").show();
                }
                if (data.days) {
                    if (data.days.flag) {
                        $("#days-plot").html('<div><h5 style="text-align: center"> Day wise contributions </h5><div id="data-plot-days"></div></div>')
                        $("#days-plot").show();
                        Morris.Bar(data.days.data);
                    }
                }
                if (data.months) {
                    if (data.months.flag) {
                        $("#months-plot").html('<div><h5 style="text-align: center"> Month wise contributions </h5><div id="data-plot-months"></div></div>')
                        $("#months-plot").show();
                        Morris.Bar(data.months.data);
                    }
                }
                if (data.streak) {
                    if (data.streak.flag) {
                        $("#streak-plot").html('<div><h5 style="text-align: center"> Contributions during longest streak </h5><div id="data-plot-longest_streak"></div></div>')
                        $("#streak-plot").show();
                        Morris.Bar(data.streak.data);
                    }
                }
                if (data.repo) {
                    $('#repo_info').show();
                    const fnf = data.repo.forks + ' original and ' + data.repo.non_forks + ' forked repos'
                    $('#fnf').text(fnf);
                    $('#fnf').show();
                    $('#ogs').text(data.repo.og_stars + ' total stars in original repositories');
                    $('#ogs').show();
                    $('#langc').text(sing_plu(data.repo.lang_count, 'language', 'languages') + ' used');
                    $('#langc').show();
                    $('#langs').text(data.repo.langs);



                }
            });

        event.preventDefault();
    });
});
