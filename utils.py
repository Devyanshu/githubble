
def sing_or_plural(value, text):
    value = int(value)
    if value == 0:
        return ''
    elif value == 1:
        return text
    else:
        return text + 's'


def helper(user_ob):
    dct = {}
    total_days = user_ob.days_not_contributed + user_ob.days_contributed

    if user_ob.longest_streak['length'] <= 1:
        duration = ''
    else:
        duration = '''(From {} to {})'''.format(
            user_ob.longest_streak['start'], user_ob.longest_streak['end'])

    dct['name'] = user_ob.name
    if user_ob.joined:
        dct['joined'] = user_ob.joined
    if user_ob.followers:
        dct['followers'] = user_ob.followers
    if user_ob.following:
        dct['following'] = user_ob.following

    dct['profileUrl'] = user_ob.url
    dct['avatar'] = user_ob.avatarUrl
    dct['repos'] = user_ob.repoCount
    dct['total_days'] = total_days
    dct['total_contribution'] = user_ob.commits_last_year
    if user_ob.last_contribution:
        dct['last_contribution'] = user_ob.last_contribution
    dct['days_contributed'] = user_ob.days_contributed
    dct['longest_gap'] = user_ob.longest_gap
    dct['longest_streak'] = '{} {} {}'.format(user_ob.longest_streak['length'], sing_or_plural(
        user_ob.longest_streak['length'], 'day'), duration)
    if user_ob.longest_streak['avg_commits'] >= 2:
        dct['avg_commits'] = '{} {}'.format(
            user_ob.longest_streak['avg_commits'], 'contributions/day')

    max_activity_day = list(user_ob.top_five_activity.keys())[0]
    max_activity = user_ob.top_five_activity[max_activity_day]
    max_activity_day = "-".join(max_activity_day.split('-')[::-1])

    if max_activity:
        dct['max_activity'] = {
            'num': max_activity,
            'day': max_activity_day
        }

    return dct


def get_weekwise(user_ob):
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
        'element': 'data-plot-days',
        'data': lst,
        'xkey': 'day',
        'ykeys': ['value'],
        # 'labels': list(temp.keys()),
        'barColors': ['#000000'],
        'hideHover': 'auto',
        'gridLineColor: '  # eef0f2',
        'lineWidth': 1,
        'resize': 'true'
    }
    return {'data': dct, 'flag': flag}


def get_monthwise(user_ob):
    lst = []
    flag = False
    temp = user_ob.month_wise_contributions
    if any(list(temp.values())):
        flag = True

    for ii in temp:
        lst.append({
            'value': temp[ii],
            'month': ii
        })

    dct = {
        'element': 'data-plot-months',
        'data': lst,
        'xkey': 'month',
        'ykeys': ['value'],
        # 'labels': list(temp.keys()),
        'barColors': ['#000000'],
        'hideHover': 'auto',
        'gridLineColor: '  # eef0f2',
        'lineWidth': 1,
        'resize': 'true'
    }
    return {'data': dct, 'flag': flag}


def get_longest_streak_values(user_ob):
    lst = []
    flag = False
    temp = user_ob.longest_streak['daywise']
    if len(temp) >= 5:
        flag = True

    for ii in temp:
        lst.append({
            'value': temp[ii],
            'day': '/'.join(ii.split('-')[::-1][:-1])
        })

    dct = {
        'element': 'data-plot-longest_streak',
        'data': lst,
        'xkey': 'day',
        'ykeys': ['value'],
        # 'labels': list(temp.keys()),
        'barColors': ['#000000'],
        'hideHover': 'auto',
        'gridLineColor: '  # eef0f2',
        'lineWidth': 1,
        'resize': 'true'
    }
    return {'data': dct, 'flag': flag}


def repo_helper(repo_ob):
    dct = {}
    dct['forks'] = repo_ob.forks
    dct['non_forks'] = repo_ob.non_forks
    dct['og_stars'] = repo_ob.total_stars
    dct['lang_count'] = len(repo_ob.language_names)
    dct['langs'] = ', '.join(repo_ob.language_names)

    return dct


if __name__ == "__main__":
    pass
