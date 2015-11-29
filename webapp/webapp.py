import aiohttp
import aiohttp_jinja2
import asyncio
import jinja2


import settings
from routes import urls


if __name__ == '__main__':
    app = aiohttp.web.Application()
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR))
    for url in urls:
        app.router.add_route(*url)
    app.router.add_static(settings.STATIC_URL, settings.STATIC_DIR)

    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, settings.HOST, settings.PORT)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()
