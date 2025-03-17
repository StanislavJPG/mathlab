import httpx
from bs4 import BeautifulSoup
from yarl import URL


class MathNewsSearcher:
    """
    This is improvised news searcher.
    """

    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    default_url = URL('https://www.google.com/search').with_query(q='математика+україна', tbm='nws', start=0)

    def __init__(self, limit: int = 10, url: str = None):
        self.url = self.default_url if not url else url
        self.limit = limit

    def _get_titles(self) -> list[dict]:
        news_titles = self.__get_page_content(str(self.url))
        search_results = news_titles.find_all('div', class_='SoaBEf', limit=self.limit)
        results = []

        for result in search_results:
            titles = {
                'title': result.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d').text,
                'origin_url': result.find('a', class_='WlydOe').get('href'),
                'improvised_published_at': result.find('div', class_='OSrXXb rbYSKb LfVVr').text,
                'short_content': result.find('div', class_='GI74Re nDgy9d').text,
            }
            results.append(titles)

        return results

    def __get_page_content(self, url) -> BeautifulSoup:
        with httpx.Client(headers=self._HEADERS) as client:
            user_request: str = f'{url}'

            response = client.get(user_request)
            soup = BeautifulSoup(response.text, 'lxml')

        return soup

    @property
    def kwargs_list(self):
        titles = self._get_titles()
        kwargs_list = []
        for title in titles:
            kwargs_list.append(
                {
                    'title': title['title'],
                    'origin_url': title['origin_url'],
                    'improvised_published_at': title['improvised_published_at'],
                    'short_content': title['short_content'],
                }
            )
        return kwargs_list
