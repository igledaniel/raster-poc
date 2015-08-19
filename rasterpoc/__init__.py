from shapely.geometry import asShape
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
import requests


def transform_to_feature_layers(json_response):
    # assumes more than one layer was requested
    feature_layers = {}
    for layer_name, layer_data in json_response.items():
        layer_features = layer_data['features']
        features = []
        for layer_feature in layer_features:
            geometry = layer_feature['geometry']
            shape = asShape(geometry)
            properties = layer_feature['properties']
            feature = (shape.wkb, properties, None)
            features.append(feature)
        feature_layers[layer_name] = features
    return feature_layers


class FetchResult(object):

    def __init__(self, is_error=False, content='No Content', status_code=200):
        self.is_error = is_error
        self.content = content
        self.status_code = status_code


class VectorTileServiceFetcher(object):

    def __init__(self, request_prefix):
        self.request_prefix = request_prefix

    def __call__(self, path):
        # this can also raise an error, in which case we'll just get a 500
        response = requests.get(self.request_prefix + path)
        if response.status_code != 200:
            return FetchResult(is_error=True, content=response.content,
                               status_code=response.status_code)
        json_data = response.json()
        return FetchResult(content=json_data)


class RasterProxy(object):

    def __init__(self, fetcher, mapnik_formatter):
        self.fetcher = fetcher
        self.mapnik_formatter = mapnik_formatter

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def generate_404(self):
        return Response('Not Found', status=404, mimetype='text/plain')

    def error_fetch_response(self, fetch_result):
        if fetch_result.status_code is not None:
            return Response(fetch_result.error, fetch_result.status_code)
        else:
            return Response('Internal Server Error', status_code=500)

    def handle_request(self, request):
        if not request.path.endswith('.png'):
            return self.generate_404()
        vector_tile_service_path = request.path.replace('.png', '.json')
        fetch_result = self.fetcher(vector_tile_service_path)
        if fetch_result.is_error:
            return self.error_fetch_response(self, fetch_result)
        json_data = fetch_result.content
        feature_layers = transform_to_feature_layers(json_data)
        gif_content = self.mapnik_formatter(feature_layers)
        response = Response(gif_content, mimetype='image/png',
                            headers=[('Access-Control-Allow-Origin', '*')])
        response.add_etag()
        response.make_conditional(request)
        return response
