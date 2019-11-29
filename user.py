from urllib.request import urlopen
import bs4 as bs
import re

class User:

    def __init__(self, username):
        self.username = username
        baseUrl = 'https://github.com/'
        self.url = baseUrl + self.username
        self.name = None
        self.repoCount = 0
        self.commits_last_year = 0
        self.avatarUrl = None
        self.top_five_activity = {}
        self.days_contributed = 0
        self.days_not_contributed = 0
        self.longest_streak = 0

    def get_details(self):        
        content = urlopen(self.url).read()
        data = bs.BeautifulSoup(content,'lxml')
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
        for span in spans:
            try:
                if 'Counter' in span["class"]:
                    self.repoCount = span.text.strip(' ').strip('\n').strip(' ')
                    # add checks for stars, followers and following here.
                    break            
            except:
                continue
        h2s = data.findAll('h2')
        for h2 in h2s: 
            try:
                if 'contribution' in h2.text:
                    self.commits_last_year = h2.text.strip('\n').strip().split(' ')[0]
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
        lst = sorted(activity.keys(), key=activity.get, reverse=True)
        self.top_five_activity = {i:activity[i] for i in lst[:5]}

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
        det = '{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(self.name, self.repoCount, self.top_five_activity, self.commits_last_year,self.avatarUrl, self.days_contributed, self.days_not_contributed)
        print(det)
        return ''

    def find_longest_streak(self, activity):
        max_streak = 0
        curr_streak = 0
        st = ''
        end = ''
        for ii in activity:
            if activity[ii]:
                curr_streak += 1
            else:
                end
                max_streak = max(max_streak, curr_streak)
                curr_streak = 0
        self.longest_streak = max_streak

if __name__ == '__main__':
    test = User('Devyanshu')
    test.get_details()
    test.print_all()