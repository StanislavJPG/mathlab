import httpx
from bs4 import BeautifulSoup


class MathNewsSearcher:
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __get_page_content(self, url) -> BeautifulSoup:
        with httpx.Client(headers=self._HEADERS) as client:
            user_request: str = f'{url}'

            response = client.get(user_request)
            soup = BeautifulSoup(response.text, 'lxml')

        return soup

    def find_titles(self) -> list:
        news_titles = self.__get_page_content(
            f'https://www.google.com/search?q=математика+україна&tbm=nws&start=0'
        )
        search_results = news_titles.find_all('div', class_='SoaBEf', limit=1)

        titles = [{'title': result.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d"),
                   'new_url': result.find("a", class_="WlydOe").get('href'),
                   'posted': result.find('div', class_='OSrXXb rbYSKb LfVVr')}
                  for result in search_results]

        return titles
