# TAXII Connector
Connector for pulling and converting STIX information from TAXII Service Providers into Enterprise EDR Feeds.

## Requirements/Installation

The file `requirements.txt` contains a list of dependencies for this project. After cloning this repository, run the following command from the `examples/enterprise_edr/threat_intelligence` directory:

```python
pip3 install -r ./requirements.txt
```

## Introduction
This document describes how to configure the CB Enterprise EDR TAXII connector.
This connector allows for the importing of STIX data by querying one or more TAXII services, retrieving that data and then converting it into CB feeds using the CB JSON format for IOCs.

## Setup - TAXII Configuration File
The TAXII connector uses the configuration file `config.yml`. An example configuration file is available [here.](config.yml) An explanation of each entry in the configuration file is provided in the example.

## Running the Connector
The connector can be activated by running the Python3 file `stix_taxii.py`. The connector will attempt to connect to your TAXII service(s), poll the collection(s), retrieve the STIX data, and send it to the Enterprise EDR Feed specified in your `config.yml` file.

```python
python3 stix_taxii.py
```

This script supports updating each TAXII configuration's `start_date`, the date for which to start requesting data, via the command line with the argument `site_start_date`. To change the `stat_date` value for each site in your config file, you must supply the site name and desired `start_date` in `%Y-%m-%d %H:%M:%S` format.

```python
python3 stix_taxii.py --site_start_date my_site_name_1 '2019-11-05 00:00:00' my_site_name_2 '2019-11-05 00:00:00'
```

This may be useful if the intention is to keep an up-to-date collection of STIX data in an Enterprise EDR Feed.

## Troubleshooting

### Credential Error
In order to use this code, you must have CBC SDK installed and configured. If you receive an authentication error, visit the Developer Network Authentication Page for [instructions on setting up authentication](https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/). See [ReadTheDocs](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication) for instructions on configuring your credentials file.

### 504 Gateway Timeout Error
The [Carbon Black Enterprise EDR Feed Manager API](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/) is used in this code. When posting to a Feed, there is a 60 second limit before the gateway terminates your connection. The amount of reports you can POST to a Feed is limited by your connection speed. In this case, you will have to split your threat intelligence into smaller collections until the request takes less than 60 seconds, and send each smaller collection to an individual Enterprise EDR Feed.
