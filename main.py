import ssl

from aiohttp import web

with open("main.html") as main_page_file:
    main_page = main_page_file.read()


async def handle(request):
    return web.Response(text=main_page, content_type="text/html")


app = web.Application()
app.add_routes(
    [
        web.get("/", handle),
    ]
)

if __name__ == "__main__":
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(
        "/etc/letsencrypt/live/reptiloid.fun/fullchain.pem",
        "/etc/letsencrypt/live/reptiloid.fun/privkey.pem",
    )
    web.run_app(app, port=443, ssl_context=ssl_context)
