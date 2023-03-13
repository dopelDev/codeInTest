import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import aiohttp
import asyncio
import async_timeout
import aiodns
from multidict import CIMultiDict, CIMultiDictProxy
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy()) # Usamos el policy de uvloop para mejorar el rendimiento

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    custom_settings = {
        'CONCURRENT_REQUESTS': 32, # Número máximo de solicitudes simultáneas
        'DOWNLOAD_DELAY': 1, # Retraso entre descargas
        'RETRY_TIMES': 2, # Número máximo de reintentos
        'ROTATING_PROXY_LIST': [ # Lista de proxies a utilizar
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080',
            'http://proxy3.example.com:8080'
        ]
    }

    # Función para obtener el contenido de una página web utilizando aiohttp
    async def fetch_page(self, session, url):
        try:
            async with session.get(url) as response:
                async with async_timeout.timeout(10):
                    return await response.text(), response.status, response.headers
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f'Error fetching {url}: {e}')
            return None, None, None

    # Función para procesar la respuesta de una página web y extraer la información deseada
    async def parse_page(self, response):
        title = response.xpath('//title/text()').extract_first()
        yield {'title': title}

    # Función para manejar una solicitud utilizando aiohttp y llamar a la función parse_page
    async def handle_request(self, session, url):
        html, status, headers = await self.fetch_page(session, url)
        if html:
            response = scrapy.http.HtmlResponse(
                url=url,
                body=html.encode(),
                status=status,
                headers=CIMultiDictProxy(CIMultiDict(headers)),
                request=scrapy.http.Request(url)
            )
            await self.parse_page(response)

    # Función para manejar múltiples solicitudes utilizando asyncio.gather
    async def handle_requests(self, session, urls):
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(self.handle_request(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    # Función principal que configura aiohttp, obtiene una sesión y llama a handle_requests
    async def run(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ttl_dns_cache=300), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}) as session:
            await self.handle_requests(session, self.start_urls)

# Configuración del proceso de scrapy y ejecución del spider
if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })
    process.crawl(MySpider)
    process.start()

