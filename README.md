Address Finder
--------------

Quick and dirty postcode lookup HTTP/REST service using [Ordnance Survey AddressBase](http://www.ordnancesurvey.co.uk/business-and-government/products/addressbase.html) data. More to come.

Dependencies
============

On MacOS:

`$ brew install postgresql geos proj gdal postgis`

Stick the kettle on, it'll be a while.

Create GIS database
===================

`$ createdb addressfinder`
`$ psql addressfinder`
`> CREATE EXTENSION postgis;`
