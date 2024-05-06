import httpx
from bs4 import BeautifulSoup


class MathNewsSearcher:
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        news_titles = self.__get_page_content(
            f'https://www.google.com/search?q=математика+україна&tbm=nws&start=0'
        )
        search_results = news_titles.find_all('div', class_='SoaBEf', limit=1)

        for result in search_results:
            titles = {'title': result.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d").text,
                      'new_url': result.find("a", class_="WlydOe").get('href'),
                      'posted': result.find('div', class_='OSrXXb rbYSKb LfVVr').text,
                      'add_info': result.find('div', class_='GI74Re nDgy9d').text}

            return titles

    def __get_page_content(self, url) -> BeautifulSoup:
        with httpx.Client(headers=self._HEADERS) as client:
            user_request: str = f'{url}'

            response = client.get(user_request)
            soup = BeautifulSoup(response.text, 'lxml')

        return soup
