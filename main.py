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
    web.run_app(app, port=80)
