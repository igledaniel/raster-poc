def debugserve():
    from rasterpoc import RasterProxy
    from rasterpoc import VectorTileServiceFetcher
    from rasterpoc.mapnik_format import MapnikFormatter
    from werkzeug.serving import run_simple

    fetcher = VectorTileServiceFetcher('http://vector.mapzen.com')
    mapnik_formatter = MapnikFormatter()
    raster_proxy = RasterProxy(fetcher, mapnik_formatter)
    run_simple('localhost', 8080, raster_proxy,
               use_debugger=True, use_reloader=True)


if __name__ == '__main__':
    debugserve()
