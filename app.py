from flask import Flask, render_template, request, redirect, url_for
from user import User

app = Flask(__name__, static_url_path='/static')

app.debug = True
app.secret_key = "nothingfornow"

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data", methods=['POST'])
def process():
    data = dict(request.form)
    usr = User(data['username'])
    try:
        usr.get_details()
    except NameError:
        return {'error': 'We do not process enterprise account at the moment.'}
    except:
        return {'error': 'Username not valid'}
    else:
        return {'value': helper(usr)}

def sing_or_plural(value, text):
        value = int(value)
        if value==0: 
            return ''
        elif value==1: 
            return text
        else: 
            return text + 's'

def helper(user_ob):
    total_days = user_ob.days_not_contributed + user_ob.days_contributed
    html = '''<div class='row'><div class='col-md-4'><img src="{}" height='300px' width='300px'></div>'''.format(user_ob.avatarUrl)
    html += "<div class='col-md-8'><table class='table'>"
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Name', user_ob.name)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Repositories', user_ob.repoCount)
    html+='''</table>The below stats are for last {} days<table class='table'>'''.format(total_days)
    html+='<tr><td>{} </td><td>\t{}</td></tr>'.format('Commits', user_ob.commits_last_year)    

    html+='<tr><td>{} </td><td>\t{} {}</td></tr>'.format('Days contributed', user_ob.days_contributed, sing_or_plural(user_ob.days_contributed, 'day'))
    html+='<tr><td>{}</td><td>\t{} {}</td></tr>'.format('Longest contributing streak', user_ob.longest_streak, sing_or_plural(user_ob.longest_streak, 'day'))
    max_activity_day = list(user_ob.top_five_activity.keys())[0]
    max_activity = user_ob.top_five_activity[max_activity_day]
    max_activity_day = "-".join(max_activity_day.split('-')[::-1])
    html+='<tr><td>{}</td><td>\t{} {} ({})</td></tr>'.format('Maximum commits in a day', max_activity, sing_or_plural(max_activity, 'commit'), max_activity_day)
    html+='</table></table>'
    return html

if __name__ == "__main__":
    app.run(port=8000)