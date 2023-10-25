import ssl

from aiohttp import web

import settings

with open("main.html") as main_page_file:
    main_page = main_page_file.read()


async def handle_main(request):
    return web.Response(text=main_page, content_type="text/html")


def main():
    ssl_context = None

    if settings.USE_SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(settings.CERT_FILE, settings.KEY_FILE)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_main),
        ]
    )

    web.run_app(app, port=settings.PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
