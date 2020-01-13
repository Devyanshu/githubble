from urllib.request import urlopen
import json
import tempdata


class Repos:
    def __init__(self, username):
        self.username = username
        self.url = 'https://api.github.com/users/' + \
            self.username + '/repos?page=1&per_page=100'
        self.repos = {}
        self.data = {}
        self.language_names = set()
        self.all_languages = {}
        self.non_fork_languages = {}
        self.own_language_frequency = {}
        self.total_stars = 0
        self.forks = 0
        self.non_forks = 0

    def _get_data(self):
        r = urlopen(self.url).read()
        self.data = json.loads(r.decode('utf-8'))
        # reading from a cache for testing
        # self.data = tempdata.data

    def get_repos_info(self):
        self._get_data()
        langs = set()
        stars = 0
        forks = 0
        non_forks = 0
        for repo in self.data:
            self.repos[repo['name']] = {
                'created': repo['created_at'],
                'isfork': repo['fork'],
                'language': repo['language'],
                'stars': repo['stargazers_count'],
                'watchers': repo['watchers'],
                'forks': repo['forks']
            }
            if repo['language']:
                langs.add(repo['language'])
            if not repo['fork']:
                stars += repo['stargazers_count']
                non_forks += 1
            else:
                forks += 1
        self.language_names = list(langs)
        self.total_stars = stars
        self.forks = forks
        self.non_forks = non_forks

    def languages_analysis(self):
        all_languages = {}
        non_fork_languages = {}
        own_language_frequency = {}
        repo_names = list(self.repos.keys())
        languageUrl = 'https://api.github.com/repos/' + self.username + '/'

        for i in repo_names:
            temp = urlopen(languageUrl + i + '/languages').read()
            lang_data = json.loads(temp.decode('utf-8'))
            if not self.repos[i]['isfork']:
                for lang in lang_data:
                    non_fork_languages[lang] = non_fork_languages.get(
                        lang, 0) + lang_data[lang]
                    own_language_frequency[lang] = own_language_frequency.get(
                        lang, 0) + 1
            for lang in lang_data:
                all_languages[lang] = all_languages.get(
                    lang, 0) + lang_data[lang]

        self.all_languages = all_languages
        self.non_fork_languages = non_fork_languages
        self.own_language_frequency = own_language_frequency


if __name__ == '__main__':
    test = Repos('Devyanshu')
    test.get_repos_info()
    # test.languages_analysis()
