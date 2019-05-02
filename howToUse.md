# Usage Manual

### Find a station

As a scientist or scientific technician I'm using a browser to get a station id from the
[list of stations](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_list_soil.txt) or
[the static map image](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_map_soil.png) provided by the DWD on the DWD FTP
Server.

### Get the capabilities of a station

As a scientist or scientific technician I'm using the DWD Proxy API `capabilities` endpoint to get a list of
capabilities provided by the DWD on the DWD FTP Server for a given station id. Each capability has a specific resolution
(i.g. "10_minutes") and one or more observationtypes (i.g. "air_temperature" or "pressure"). When I use the curl-command
`curl "https://www.example.com/capabilities/2878"` it will produce the following output:

```json
{
  "stationId": "2878",
  "capabilities": [
    {
      "resolution": "10_minutes",
      "observationTypes": [
        "air_temperature",
        "extreme_temperature",
        "extreme_wind",
        "precipitation",
        "solar",
        "wind"
      ]
    },
    {
      "resolution": "1_minute",
      "observationTypes": [
        "precipitation"
      ]
    },
    {
      "resolution": "daily",
      "observationTypes": [
        "kl",
        "more_precip",
        "soil_temperature",
        "water_equiv"
      ]
    },
    {
      "resolution": "hourly",
      "observationTypes": [
        "air_temperature",
        "precipitation",
        "soil_temperature",
        "sun",
        "wind"
      ]
    },
    {
      "resolution": "monthly",
      "observationTypes": [
        "kl",
        "more_precip"
      ]
    }
  ]
}
```

### Query timeseries data

As a scientist or scientific technician I'm using the DWD Proxy API `timeseries` endpoint to get a list of measurement
objects for a given station id (2878), a given resolution (10_minutes), a given observation type (air_temperature) and optional start
and end timestamps. When I use the curl-command `curl
"https://www.example.com/timeseries/2878/10_minutes/air_temperature?start=2017-10-01%2010%3A00%3A00&end=2018-10-01%2009%3A59%3A59"`
it will produce the following output:

```json
{
  "stationId": "2878",
  "resolution": "10_minutes",
  "observation_type": "air_temperature",
  "timeseries": [
    {
      "timestamp": "2017-10-01T10:00:00.000Z",
      "epoch": "recent",
      "sourceUrl": "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/air_temperature/recent/10minutenwerte_TU_02878_akt.zip",
      "sourceFile": "produkt_zehn_min_tu_20170918_20190321_02878.txt",
      "sourceLine": 3230,
      "values": [
        {
          "name": "QN",
          "value": 3
        },
        {
          "name": "PP_10",
          "value": -999
        },
        {
          "name": "TT_10",
          "value": 13.2
        },
        {
          "name": "TM5_10",
          "value": 14.9
        },
        {
          "name": "RF_10",
          "value": 75.9
        },
        {
          "name": "TD_10",
          "value": 9.0
        }
      ]
    },
    {
      "timestamp": "2017-10-01T10:00:00.000Z",
      "epoch": "recent",
      "sourceUrl": "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/air_temperature/recent/10minutenwerte_TU_02878_akt.zip",
      "sourceFile": "produkt_zehn_min_tu_20170918_20190321_02878.txt",
      "sourceLine": 3231,
      "values": [
        {
          "name": "QN",
          "value": 3
        },
        {
          "name": "PP_10",
          "value": -999
        },
        {
          "name": "TT_10",
          "value": 13.5
        },
        {
          "name": "TM5_10",
          "value": 12.9
        },
        {
          "name": "RF_10",
          "value": 85.2
        },
        {
          "name": "TD_10",
          "value": 11.1
        }
      ]
    }
  ]
}
```
This is a shorted example: The real response will contain something like 70.000 timestamp objects in the timeseries
array.

@TBC

## The DWD FTP service

@see ftp://ftp-cdc.dwd.de/pub/CDC/Readme_intro_CDC_ftp.pdf

Basepath for DWD-Proxy version 1.0.0: ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/

Example station id: 2878 (Lauchstädt, Bad)

## Grep parameters from DWD FTP

    lftp ftp-cdc.dwd.de -e "du /pub/CDC/observations_germany/climate/" > development/dwd-proxy/dwd-ftp-tree-2018-12-19
    awk -F"/" '{print $1}' dwd-ftp-tree-2018-12-19-clean | sort | uniq
    
    10_minutes
    1_minute
    annual
    daily
    hourly
    monthly
    multi_annual
    subdaily
    
    awk -F"/" '{print $2}' dwd-ftp-tree-2018-12-19-clean | sort | uniq 
    
    air_temperature
    cloudiness
    cloud_type
    extreme_temperature
    extreme_wind
    kl
    mean_61-90
    mean_71-00
    mean_81-10
    more_precip
    precipitation
    pressure
    soil_temperature
    solar
    standard_format
    sun
    visibility
    water_equiv
    wind     
    
    awk -F"/" '{print $3}' dwd-ftp-tree-2018-12-19-clean | sort | uniq 

    historical
    meta_data
    now
    recent
    
## TBC