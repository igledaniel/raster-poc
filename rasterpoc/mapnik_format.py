import mapnik


def feature_layers_to_features_list(feature_layers):
    features = []
    for layer_name, layer_features in feature_layers.items():
        for feature in layer_features:
            features.append(feature)
    return features


class MapnikFormatter(object):

    def __init__(self):
        pass

    def __call__(self, feature_layers):
        # take the feature_layers dict and generate a gif response

        # this just puts all the features across all layers into a
        # single one, and then just renders them all with a very
        # simple style as a proof of concept
        # we probably want to do this per layer with a separate style
        # for each
        features = feature_layers_to_features_list(feature_layers)

        layer = mapnik.Layer('tile')
        memds = mapnik.MemoryDatasource()
        ctx = mapnik.Context()
        for feature in features:
            wkb, properties, fid = feature
            for key in properties.keys():
                ctx.push(key.encode('utf-8'))
        i = 1
        for feature in features:
            wkb, properties, fid = feature
            mf = mapnik.Feature(ctx, i)
            i += 1
            mf.add_geometries_from_wkb(wkb)
            for k, v in properties.items():
                mf[k.encode('utf-8')] = str(v)
                memds.add_feature(mf)

        layer.datasource = memds

        m = mapnik.Map(256, 256)

        m.background = mapnik.Color('blue')

        s = mapnik.Style()
        r = mapnik.Rule()
        polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9'))
        r.symbols.append(polygon_symbolizer)
        line_symbolizer = mapnik.LineSymbolizer(
            mapnik.Color('rgb(50%,50%,50%)'), 0.1)
        r.symbols.append(line_symbolizer)
        s.rules.append(r)
        m.append_style('my style', s)
        layer.styles.append('my style')

        m.layers.append(layer)
        m.zoom_all()
        # from mapnik import Image
        # im = Image(m.width, m.height)
        # mapnik.render(m, im)
        # png_contents = im.tostring()

        # this was just the easiest way for me to get this to work
        import tempfile
        tmpfile = tempfile.NamedTemporaryFile()
        with tmpfile.file as fp:
            mapnik.render_to_file(m, tmpfile.name, 'png')
            fp.seek(0)
            png_contents = fp.read()

        return png_contents
