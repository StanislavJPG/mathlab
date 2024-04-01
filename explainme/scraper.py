from bs4 import BeautifulSoup
import httpx
from .decorators import ToUserFriendlyInterface


class ExplainmeScraper:
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __init__(self, request: str) -> None:
        self.request = request

    async def __get_page_content(self, url) -> BeautifulSoup:
        async with httpx.AsyncClient(headers=self._HEADERS) as client:
            user_request: str = f'{url}'

            response = await client.get(user_request)
            soup = BeautifulSoup(response.text, 'lxml')

        return soup

    @ToUserFriendlyInterface.description
    async def get_description(self) -> list:
        # let's find wiki url by user's question
        wiki_url = await self.__get_page_content(
            f'https://www.google.com/search?q=site:uk.wikipedia.org математика {self.request}'
        )
        search_results = wiki_url.find_all('div', class_='yuRUbf', limit=1)
        url = [result.find('a', jsname='UWckNb').get('href') for result in search_results][0]

        # now let's get explanation directly from wiki page
        wiki_page_content = await self.__get_page_content(url)
        all_descriptions = wiki_page_content.find_all('div', class_='mw-body-content')
        __full_explanation = [desc.find_all('p', limit=3) for desc in all_descriptions]

        return __full_explanation

    async def get_image(self) -> list:
        yahoo_content = await self.__get_page_content(
            f'https://images.search.yahoo.com/search/images?p=математика {self.request}'
        )
        img_url = yahoo_content.find_all('li', id='resitem-0', limit=1)
        __final_img = [img.find('img').get('data-src') for img in img_url]

        return __final_img[0]
