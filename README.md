# Raster Proof of Concept

This is meant as an ephemeral testing space for raster tiles.

## Details

This python service proxies requests over to the mapzen vector tile service to use as a data source, and then uses mapnik to render into a raster png.

## Installation

You'll need to make sure that mapnik is installed globally first along with the python bindings. On ubuntu 14.04:

```bash
apt-get install libmapnik libmapnik-dev mapnik-utils python-mapnik
```

On a mac, hopefully in homebrew it's just the following to install mapnik and the python bindings:

```bash
brew update
brew install mapnik
```

This should run without issues:

```bash
python -c 'import mapnik'
```

You'll also need libgeos for shapely:

Ubuntu:

```bash
apt-get install libgeos-dev
```

And on a mac?

```bash
brew install libgeos
```

Now you can install the raster poc service:

```bash
git clone https://github.com/mapzen/raster-poc.git
cd raster-poc
virtualenv --system-site-packages env
source env/bin/activate
python setup.py develop
rasterserve
```

With the service running, there is an included simple leaflet page to exercise it:

```bash
cd leaflet
python -m SimpleHTTPServer
```

Now, just navigate to http://localhost:8000/
