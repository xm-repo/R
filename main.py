import ssl

from aiohttp import web

import settings

reptiloid = "https://storage.yandexcloud.net/reptiloid/reptiloid1.jpg"
family = "https://storage.yandexcloud.net/reptiloid/family.jpg"

with open("main.html") as main_page_file:
    main_page = main_page_file.read()


async def handle_main(request):
    return web.Response(text=main_page.format(reptiloid), content_type="text/html")


async def handle_family(request):
    return web.Response(text=main_page.format(family), content_type="text/html")


def main():
    ssl_context = None

    if settings.USE_SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(settings.CERT_FILE, settings.KEY_FILE)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_main),
            web.get("/family/", handle_family),
        ]
    )

    web.run_app(app, port=settings.PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
