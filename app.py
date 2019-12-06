from flask import Flask, render_template, request, redirect, url_for, escape
from user import User

app = Flask(__name__, static_url_path='/static')

app.debug = True
app.secret_key = "nothingfornow"


@app.route("/")
def home():
    args = dict(request.args)
    if 'q' in args:
        usr = User(args['q'])
        try:
            usr.get_details()
        except NameError:
            return render_template('index.html', data='Organization accounts are not processed at the moment.')
        except:
            return render_template('index.html', data='Username not valid')
        else:
            return render_template('index.html', data=helper(usr))

    return render_template('index.html', data=None)


@app.route("/data", methods=['POST'])
def process():
    data = dict(request.form)
    usr = User(data['username'])
    # usr.get_details()
    try:
        usr.get_details()
    except NameError:
        return {'error': 'Organization accounts are not processed at the moment.'}
    except:
        return {'error': 'Username not valid'}
    else:
        return {'value': helper(usr), 'map': get_map(usr)}


def sing_or_plural(value, text):
    value = int(value)
    if value == 0:
        return ''
    elif value == 1:
        return text
    else:
        return text + 's'


def helper(user_ob):
    total_days = user_ob.days_not_contributed + user_ob.days_contributed
    html = '''<div class='row'><div class='col-md-4'><img src="{}" height='300px' width='300px'></div>'''.format(
        user_ob.avatarUrl)
    html += "<div class='col-md-8'><table class='table'>"
    html += '<tr><td>{}</td><td>\t{}</td></tr>'.format('Name', user_ob.name)
    html += '<tr><td>{}</td><td>\t{}</td></tr>'.format(
        'Repositories', user_ob.repoCount)
    html += '''</table>The below stats are for last {} days<table class='table'>'''.format(
        total_days)
    if user_ob.last_contribution:
        html += '<tr><td>{} </td><td>\t{}</td></tr>'.format(
            'Last contribution', user_ob.last_contribution)
    html += '<tr><td>{} </td><td>\t{}</td></tr>'.format(
        'Total contributions', user_ob.commits_last_year)
    if user_ob.longest_streak['length'] <= 1:
        duration = ''
    else:
        duration = '''(From {} to {})'''.format(
            user_ob.longest_streak['start'], user_ob.longest_streak['end'])

    html += '<tr><td>{} </td><td>\t{} {}</td></tr>'.format(
        'Days contributed', user_ob.days_contributed, sing_or_plural(user_ob.days_contributed, 'day'))
    html += '<tr><td>{}</td><td>\t{} {}</td></tr>'.format(
        'Longest gap in contribution', user_ob.longest_gap, sing_or_plural(user_ob.longest_gap, 'day'))
    html += '<tr><td>{}</td><td>\t{} {} {}</td></tr>'.format(
        'Longest contributing streak', user_ob.longest_streak['length'], sing_or_plural(user_ob.longest_streak['length'], 'day'), duration)
    if user_ob.longest_streak['avg_commits'] >= 2:
        html += '<tr><td>{}</td><td>\t{} {}</td></tr>'.format(
            'Average contributions during longest streak', user_ob.longest_streak['avg_commits'], '/day')
    max_activity_day = list(user_ob.top_five_activity.keys())[0]
    max_activity = user_ob.top_five_activity[max_activity_day]
    max_activity_day = "-".join(max_activity_day.split('-')[::-1])
    if max_activity:
        html += '<tr><td>{}</td><td>\t{} {} ({})</td></tr>'.format(
            'Maximum contributions in a day', max_activity, sing_or_plural(max_activity, 'commit'), max_activity_day)
    else:
        html += '<tr><td>{}</td><td>\t{} {}</td></tr>'.format(
            'Maximum contributions in a day', max_activity, sing_or_plural(max_activity, 'commit'))
    html += '</table></table>'
    return html


def get_map(user_ob):
    lst = []
    flag = False
    temp = user_ob.weekday_wise_contributions
    if any(list(temp.values())):
        flag = True

    for ii in temp:
        lst.append({
            'value': temp[ii],
            'day': ii
        })

    dct = {
        'element': 'data-plot',
        'data': lst,
        'xkey': 'day',
        'ykeys': ['value'],
        'barColors': ['#000000'],
        'hideHover': 'auto',
        'gridLineColor: '#eef0f2',
        'resize': 'true'
    }
    return {'data': dct, 'flag': flag}

if __name__ == "__main__":
    app.run(port=5555)
