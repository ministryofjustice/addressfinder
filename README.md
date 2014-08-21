Address Finder
==============

Postcode lookup HTTP/REST service using [Ordnance Survey AddressBase Basic](http://www.ordnancesurvey.co.uk/business-and-government/products/addressbase.html) data. No data is included in this project due to copyright/licensing.

Dependencies
------------

On MacOS:

`$ brew install python postgresql geos proj gdal postgis`

Stick the kettle on, it'll be a while.

Setup
-----

### Create GIS database

```bash
$ createdb addressfinder
$ psql addressfinder
```
```SQL
> CREATE EXTENSION postgis;
```

### Create virtualenv

```bash
$ pip install virtualenv
$ git clone https://github.com/ministryofjustice/addressfinder.git
$ cd addressfinder
$ virtualenv .venv
$ source .venv/bin/activate
```

### Install requirements

```bash
$ pip install -r requirements.txt
```

### Create database schema and superuser

```bash
$ ./manage.py syncdb
```

### Import OS AddressBase Basic CSV files

```bash
$ ./manage.py import_addressbase_basic <csv_path csv_path...>
```

### Start dev server

```bash
$ ./manage.py runserver
```

You can now access [Django Admin](http://127.0.0.1/admin/authtoken/token/) to create a token for your superuser.

## Usage

Access the API with your token in the Authorization header:

```Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b```

Postcodes can be specified in upper or lowercase, with or without spaces.

#### Address lookup
```
http://127.0.0.1:8000/addresses/?postcode=sw1a1aa
```

You can specify which fields you want in the response with the `fields` kwarg:

```
http://127.0.0.1:8000/addresses/?postcode=sw1a1aa&fields=formatted_address,point
```

View the available fields [here](https://github.com/ministryofjustice/addressfinder/blob/develop/addressfinder/apps/address/serializers.py#L25)

Example response:

```json
[
  {
    "uprn": "10033544614",
    "organisation_name": "BUCKINGHAM PALACE",
    "department_name": "",
    "po_box_number": "",
    "building_name": "",
    "sub_building_name": "",
    "building_number": null,
    "thoroughfare_name": "",
    "dependent_thoroughfare_name": "",
    "dependent_locality": "",
    "double_dependent_locality": "",
    "post_town": "LONDON",
    "postcode": "SW1A 1AA",
    "postcode_type": "L",
    "formatted_address": "Buckingham Palace\nLondon\nSW1A 1AA",
    "point": {
      "type": "Point",
      "coordinates": [
        -0.141587558526369,
        51.50100893654096
      ]
    }
  }
]
```

#### Lat/lon lookup

```
http://127.0.0.1:8000/postcodes/sw1a1aa/
```

Example response:

```json
{
  "type": "Point",
  "coordinates": [
    -0.141587558526369,
    51.50100893654096
  ]
}
```

This method returns a lat/lon point for the centre of the specified postcode area only.
