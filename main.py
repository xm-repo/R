import logging
import ssl
import sys

import jinja2
from aiohttp import web

import gpt
import settings

reptiloid1 = "https://storage.yandexcloud.net/reptiloid/reptiloid1.jpg"
reptiloid2 = "https://storage.yandexcloud.net/reptiloid/reptiloid2.jpg"
family = "https://storage.yandexcloud.net/reptiloid/family.jpg"

jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
main_page = jenv.get_template("main.html")


async def handle_main(request):
    return web.Response(
        text=main_page.render(
            photo=reptiloid1,
            bday=False,
            gpt=False,
        ),
        content_type="text/html",
    )


async def handle_family(request):
    return web.Response(
        text=main_page.render(
            photo=family,
            bday=False,
            gpt=False,
        ),
        content_type="text/html",
    )


async def handle_bday(request):
    return web.Response(
        text=main_page.render(
            photo=reptiloid2,
            bday=True,
            gpt=False,
        ),
        content_type="text/html",
    )


async def handle_advice(request):
    return web.Response(
        text=main_page.render(
            photo=reptiloid1,
            bday=False,
            gpt=True,
            advice=(await gpt.query()),
        ),
        content_type="text/html",
    )


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    ssl_context = None

    if settings.USE_SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(settings.CERT_FILE, settings.KEY_FILE)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_main),
            web.get("/family", handle_family),
            web.get("/family/", handle_family),
            web.get("/bday", handle_bday),
            web.get("/bday/", handle_bday),
            web.get("/advice", handle_advice),
            web.get("/advice/", handle_advice),
        ]
    )

    web.run_app(app, port=settings.PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
