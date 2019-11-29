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

def helper(user_ob):
    html = '''<div class='row'><div class='col-md-4'><img src="{}" height='300px' width='300px'></div>'''.format(user_ob.avatarUrl)
    html += "<div class='col-md-8'><table class='table'>"
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Name', user_ob.name)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Repositories', user_ob.repoCount)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Commits this year', user_ob.commits_last_year)
    total_days = user_ob.days_not_contributed + user_ob.days_contributed
    html+='<tr><td>{} (in last {} days) </td><td>\t{} days</td></tr>'.format('Days contributed', total_days, user_ob.days_contributed)
    html+='<tr><td>{} (in last {} days) </td><td>\t{} days</td></tr>'.format('Longest contributing streak',total_days, user_ob.longest_streak)
    html+='</table></table>'
    return html

if __name__ == "__main__":
    app.run(port=8000)