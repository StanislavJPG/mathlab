import httpx
from bs4 import BeautifulSoup


class GraphBuilderScraper:
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __init__(self, function: str) -> None:
        self.__function = function

    async def get_page_content(self):
        async with httpx.AsyncClient(headers=self._HEADERS) as client:
            user_request: str = f'https://www.google.com/search?q={self.__function}'

            response = await client.get(user_request)
            soup = BeautifulSoup(response.text, 'lxml')
            soup_all_content = soup.find_all('svg')
            result = [graph.prettify() for graph in soup_all_content]
            print(result)
        return soup_all_content
