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
    except:
        return {'error': 'Username not valid'}
    else:
        return {'value': helper(usr)}

def helper(user_ob):
    html = '''<img src="{}">'''.format(user_ob.avatarUrl)
    html += "<table class='table'>"
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Name', user_ob.name)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Repositories', user_ob.repoCount)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Commits this year', user_ob.commits_last_year)
    html+='<tr><td>{}</td><td>\t{}</td></tr>'.format('Days contributed', user_ob.days_contributed)
    html+='</table>'
    return html

if __name__ == "__main__":
    app.run(port=8000)