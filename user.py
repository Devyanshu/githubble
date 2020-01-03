from urllib.request import urlopen
import bs4 as bs
import re
import datetime
import calendar
import json


class User:

    def __init__(self, username):
        self.username = username
        baseUrl = 'https://github.com/'
        api_url = 'https://api.github.com/users/'
        self.url = baseUrl + self.username
        self.apiUrl = api_url + self.username
        self.name = None
        self.repoCount = None
        self.followers = ''
        self.following = ''
        self.joined = ''
        self.commits_last_year = 0
        self.avatarUrl = None
        self.top_five_activity = {}
        self.days_contributed = 0
        self.days_not_contributed = 0
        self.longest_streak = {}
        self.longest_gap = 0
        self.last_contribution = ''
        self.weekday_wise_contributions = {}
        self.month_wise_contributions = {}
        self.repos = {}

    def get_details(self):
        flag = False
        try:
            r = urlopen(self.apiUrl).read()
            apiData = json.loads(r.decode('utf-8'))
        except:
            flag = True
        else:
            userType = apiData['type']
            if userType != 'User':
                raise NameError('organization account')
            self.avatarUrl = apiData['avatar_url']
            self.name = apiData['name']
            if not self.name:
                self.name = '(Name not provided)'
            self.repoCount = apiData['public_repos']
            self.followers = apiData['followers']
            self.following = apiData['following']
            self.joined = '-'.join(apiData['created_at'].split('T')
                                   [0].split('-')[::-1])

        content = urlopen(self.url).read()
        data = bs.BeautifulSoup(content, 'lxml')

        if flag:

            images = data.findAll('img')
            for img in images:
                if ("avatar" in img["class"] and img['src'] != ''):
                    self.avatarUrl = img['src']
                    break

            spans = data.findAll('span')
            for span in spans:
                try:
                    if span["itemprop"] == 'name':
                        self.name = span.text
                except:
                    continue
            if self.name is None:
                raise NameError('enterprise account')
            if self.name == '':
                self.name = '(Name not provided)'

            for span in spans:
                try:
                    if 'Counter' in span["class"]:
                        self.repoCount = span.text.strip(
                            ' ').strip('\n').strip(' ')
                        # add checks for stars, followers and following here.
                        break
                except:
                    continue

        h2s = data.findAll('h2')
        for h2 in h2s:
            try:
                if 'contribution' in h2.text:
                    self.commits_last_year = h2.text.strip(
                        '\n').strip().split(' ')[0]
                    break
            except:
                continue
        activity = {}
        rects = data.findAll('rect')
        for rect in rects:
            try:
                activity[rect['data-date']] = int(rect['data-count'])
            except:
                continue

        self.days_activity(activity)
        self.find_longest_streak(activity)
        self.find_longest_gap(activity)
        self.find_last_contribution(activity)
        lst = sorted(activity.keys(), key=activity.get, reverse=True)
        self.top_five_activity = {i: activity[i] for i in lst[:5]}
        self.find_weekday_wise(activity)
        self.find_month_wise(activity)

    def days_activity(self, activity):
        nc, c = 0, 0
        for i in activity:
            if activity[i] == 0:
                nc += 1
            else:
                c += 1
        self.days_contributed = c
        self.days_not_contributed = nc

    def print_all(self):
        det = '{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(self.name, self.repoCount,
                                                  self.top_five_activity,
                                                  self.commits_last_year,
                                                  self.avatarUrl,
                                                  self.days_contributed,
                                                  self.days_not_contributed)
        print(det)
        return ''

    def find_longest_gap(self, activity):
        max_gap = 0
        curr_gap = 0
        for ii in activity:
            if not activity[ii]:
                curr_gap += 1
            else:
                max_gap = max(max_gap, curr_gap)
                curr_gap = 0
        self.longest_gap = max_gap

    def find_longest_streak(self, activity):
        streak_sum = 0
        max_streak = 0
        curr_streak = 0
        streak_end = ''
        streak_start = ''
        for ii in activity:
            if activity[ii]:
                curr_streak += 1
            else:
                if curr_streak >= max_streak:
                    streak_end = ii
                max_streak = max(max_streak, curr_streak)
                curr_streak = 0

        l_streak = max(max_streak, curr_streak)
        if l_streak == curr_streak and l_streak != 0:
            streak_end = ii
            keys = list(activity.keys())
            streak_start = keys[keys.index(streak_end) - l_streak + 1]
            streak_end = keys[keys.index(streak_end)]
            streak_sum = sum(list(activity.values())[
                keys.index(streak_start):keys.index(streak_end)+1])
        else:
            keys = list(activity.keys())
            streak_start = keys[keys.index(streak_end) - l_streak]
            streak_end = keys[keys.index(streak_end)-1]
            streak_sum = sum(list(activity.values())[
                keys.index(streak_start):keys.index(streak_end)+1])

        day_wise_streak = {}
        st = keys.index(streak_start)
        end = keys.index(streak_end)
        for ii in range(st, end + 1):
            day_wise_streak[keys[ii]] = activity[keys[ii]]

        self.longest_streak = {
            'length': l_streak,
            'avg_commits': 0 if l_streak == 0 else round(streak_sum/l_streak, 2),
            'start': "-".join(streak_start.split('-')[::-1]),
            'end': "-".join(streak_end.split('-')[::-1]),
            'daywise': day_wise_streak
        }

    def find_last_contribution(self, activity):
        day = ''
        for i in list(activity.keys())[::-1]:
            if activity[i] != 0:
                day = i
                break

        if day:
            today = datetime.date.today()
            query = datetime.date(*list(map(int, day.split('-'))))
            delta = today - query

            if delta.days == 0:
                self.last_contribution = 'Today, {}'.format(
                    '-'.join(day.split('-')[::-1]))
            elif delta.days == 1:
                self.last_contribution = 'Yesterday, {}'.format(
                    '-'.join(day.split('-')[::-1]))
            else:
                text = '{} {} ago, {}'.format(
                    int(delta.days), 'days', '-'.join(day.split('-')[::-1]))
                self.last_contribution = text
        else:
            self.last_contribution = ''

    def find_weekday_wise(self, activity):
        dct = {}
        days = list(activity.keys())
        for i in days:
            weekday = datetime.datetime.strptime(i, '%Y-%m-%d').weekday()
            weekday = calendar.day_name[weekday]
            dct[weekday] = dct.get(weekday, 0) + activity[i]
        self.weekday_wise_contributions = dct

    def find_month_wise(self, activity):
        months = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'April',
                  '05': 'May', '06': 'June', '07': 'July', '08': 'Aug',
                  '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

        dct = {}
        days = list(activity.keys())
        for i in days:
            y, m, _ = i.split('-')
            text = months[m] + " '" + y[-2:]
            dct[text] = dct.get(text, 0) + activity[i]
        self.month_wise_contributions = dct


if __name__ == '__main__':
    test = User('Devyanshu')
    test.get_details()
    test.print_all()
