# ThreatIntel Module
Python3 module that can be used in the development of Threat Intelligence Connectors for the Carbon Black Cloud.

## Requirements

The file `requirements.txt` contains a list of dependencies for this project. After cloning this repository, run the following command from the `examples/enterprise_edr/threat_intelligence` directory:

```python
pip3 install -r ./requirements.txt
```


## Introduction
This document describes how to use the ThreatIntel Python3 module for development of connectors that retrieve Threat Intelligence and import it into a Carbon Black Cloud instance.

Throughout this document, there are references to Carbon Black Enterprise EDR Feed and Report formats. Documentation on Feed and Report definitions is [available here.](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#definitions)

## Example

An example of implementing this ThreatIntel module is [available here](Taxii_README.md). The example uses cabby to connect to a TAXII server, collect threat intelligence, and send it to an Enterprise EDR Feed.


## Usage

`threatintel.py` has two main uses:

1. Report Validation with `schemas.ReportSchema`
2. Pushing Reports to a Carbon Black Enterprise EDR Feed with `threatintel.push_to_cb()`

### Report validation

Each Report to be sent to the Carbon Black Cloud should be validated
before sending. The [Enterprise EDR Report format](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#definitions) is a JSON object with
five required and five optional values.

|Required|Type|Optional|Type|
|---|---|---|---|
|`id`|string|`link`|string|
|`timestamp`|integer|`[tags]`|[str]|
|`title`|string|`iocs`|[IOC Format](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#definitions)|
|`description`|string|`[iocs_v2]`|[[IOCv2 Format](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#definitions)]|
|`severity`|integer|`visibility`|string|

The `push_to_cb` function checks for the existence and type of the five
required values, and (if applicable) checks the optional values, through a Schema.
See `schemas.py` for the definitions.

### Pushing Reports to a Carbon Black Enterprise EDR Feed

The `push_to_cb` function takes a list of `AnalysisResult` objects (or objects of your own custom class) and a Carbon
Black Enterprise EDR Feed ID as input, and writes output to the console.
The `AnalysisResult` class is defined in `results.py`, and requirements for a custom class are outlined in the Customization section below.

`AnalysisResult` objects are expected to have the same properties as
Enterprise EDR Reports (listed in the table above in Report Validation), with the addition of `iocs_v2`. The
`push_to_cb` function will convert `AnalysisResult` objects into
Report dictionaries, and then those dictionaries into Enterprise EDR
Report objects.

Any improperly formatted report dictionaries are saved to a file called `malformed_reports.json`.

Upon successful sending of reports to an Enterprise EDR Feed, you should
see something similar to the following INFO message in the console:

`INFO:threatintel:Appended 1000 reports to Enterprise EDR Feed AbCdEfGhIjKlMnOp`


### Using Validation and Pushing to Enterprise EDR in your own code

Import the module and supporting classes like any other python package, and instantiate a ThreatIntel object:

 ```python
  from threatintel import ThreatIntel
  from results import IOC_v2, AnalysisResult
  ti = ThreatIntel()
```

Take the threat intelligence data from your source, and convert it into ``AnalysisResult`` objects. Then, attach the indicators of compromise, and store your data in a list.

```python
  myResults = []
  for intel in myThreatIntelligenceData:
    result = AnalysisResult(analysis_name=intel.name, scan_time=intel.scan_time, score=intel.score, title=intel.title, description=intel.description)
    #ioc_dict could be a collection of md5 hashes, dns values, file hashes, etc.
    for ioc_key, ioc_val in intel.ioc_dict.items():
      result.attach_ioc_v2(values=ioc_val, field=ioc_key, link=link)
    myResults.append(result)
```

Finally, push your threat intelligence data to an Enterprise EDR Feed.
```python
  ti.push_to_cb(feed_id='AbCdEfGhIjKlMnOp', results=myResults)
```

`ti.push_to_cb` automatically validates your input to ensure it has the values required for Enterprise EDR. Validated reports will be sent to your specified Enterprise EDR Feed, and any malformed reports will be available for review locally at `malformed_reports.json`.



## Customization

Although the `AnalysisResult` class is provided in `results.py` as an example, you may create your own custom class to use with `push_to_cb`. The class must have the following attributes to work with the provided `push_to_cb` function, as well as the Enterprise EDR backend:


|Attribute|Type|
|---|---|
|`id`|string|
|`timestamp`|integer|
|`title`|string|
|`description`|string|
|`severity`|integer|
|`iocs_v2`|[[IOCv2 Format](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/#definitions)]|

It is strongly recommended to use the provided `IOC_v2()` class from `results.py`. If you decide to use a custom `iocs_v2` class, that class must have a method called `as_dict` that returns `id`, `match_type`, `values`, `field`, and `link` as a dictionary.


## Writing a Custom Threat Intelligence Polling Connector

An example of a custom Threat Intel connector that uses the `ThreatIntel` Python3 module is included in this repository as `stix_taxii.py`. Most use cases will warrant the use of the Enterprise EDR `Report` attribute `iocs_v2`, so it is included in `ThreatIntel.push_to_cb()`.

`ThreatIntel.push_to_cb()` and `AnalysisResult` can be adapted to include other Enterprise EDR `Report` attributes like `link, tags, iocs, and visibility`.

## FAQ

### How do I use this to upload lots of IOCs to a Feed?

Enterprise EDR Feeds contain Reports. A Report contains IOCs. To upload a batch of IOCs to a Feed, you will need to:

1. [Extract info from IOCs](#1-extract-info-from-iocs),
2. [Create Reports](#2-create-reports),
3. [Attach IOCs to Reports](#3-attach-iocs-to-reports),
4. [Send Reports to a Feed using the Feed ID](#4-send-reports-to-a-feed-using-the-feed-id).

There are a couple approaches you can take to creating Reports and attaching IOCs: either create a Report for each IOC, or attach multiple IOCs to a Report. To retain the most threat intelligence possible, we will create a Report for each IOC.

#### 1. Extract info from IOCs

Extract or infer the following information from each of your IOCs:

* Title
* ID
* Description
* Timestamp
* Severity (integer between 1 and 10, inclusive)
* Field
* Value(s)
* Link

For example, I have this STIX threat intelligence:

```xml
<stix:Indicator id="threatstream:indicator-916f9adc-9727-46e7-afc6-c22023e39d5e" timestamp="2020-11-02T22:32:17.346135+00:00" xsi:type="indicator:IndicatorType">
    <indicator:Title>phish_domain: mncovidmasksewists.net</indicator:Title>
    <indicator:Type xsi:type="stixVocabs:IndicatorTypeVocab-1.1">Domain Watchlist</indicator:Type>
    <indicator:Description>TS ID: 55474479396; iType: phish_domain; Date First: 2020-04-06T12:55:17.492Z; State: active; Source: DT COVID-19; Detail: COVID-19,Coronavirus,Domain-Risk-Score:99,Domainsquatting,Reference:https://www.domaintools.com/resources/blog/free-covid-19-threat-list-domain-risk-assessments-for-coronavirus-threatsSource:-DomainToolsTyposquatting,Source:DomainTools,Typosquatting; MoreDetail: imported by user 668</indicator:Description>
    <indicator:Observable id="threatstream:Observable-7e740bc2-eeb2-443e-9c61-57baba2627f8">
        <cybox:Title>phish_domain: mncovidmasksewists.net</cybox:Title>
        <cybox:Object id="threatstream:DomainName-d9e2a733-d692-4979-8438-2257def096ff">
            <cybox:Properties xsi:type="DomainNameObj:DomainNameObjectType">
                <DomainNameObj:Value>mncovidmasksewists.net</DomainNameObj:Value>
            </cybox:Properties>
        </cybox:Object>
    </indicator:Observable>
    <indicator:Producer>
        <stixCommon:Time>
            <cyboxCommon:Produced_Time>2020-04-06T22:15:05.389000+00:00</cyboxCommon:Produced_Time>
        </stixCommon:Time>
    </indicator:Producer>
</stix:Indicator>
```

This would be the extracted information:

```python
title = "phish_domain: mncovidmasksewists.net"
id = "threatstream:Observable-7e740bc2-eeb2-443e-9c61-57baba2627f8"
description = "TS ID: 55474479396; iType: phish_domain; [...]"
timestamp = 1586211305
severity = 10
field = "netconn_domain"
value = "mncovidmasksewists.net"
link = "https://www.domaintools.com/resources/blog/free-covid-19-threat-list-domain-risk-assessments-for-coronavirus-threats"
```

#### 2. Create Reports

Use the extracted Title, ID, Description, Timestamp, and Severity to create a Report.

```python
from examples.enterprise_edr.threat_intelligence.results import AnalysisResult
my_report = AnalysisResult(title=title, analysis_name=id, description=description,
                        timestamp=timestamp, score=severity)
```

Keep track of your Reports in a list. This is what will be sent to the Feed.

```python
report_list = []
report_list.append(my_report)
```

#### 3. Attach IOCs to Reports

For each IOC, attach it to the corresponding Report.

```python
my_report.attach_ioc_v2(values=value, field=field, link=link)
```

Repeat Steps 1, 2, and 3 for each IOC.

Alternatively, you can attach multiple IOCs to a single Report. IOCs do not support titles, descriptions, severities, or timestamps, so that approach is less informative than creating a Report for each IOC.

IOCs can be IP addresses, domains, file hashes, and many other types. See [Platform Search Fields for Processes and Enriched Events](https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/platform-search-fields) for an idea of what field to assign to each IOC.

#### 4. Send Reports to a Feed using the Feed ID

Send your list of Reports to a Feed using the Feed ID.

```python
from examples.enterprise_edr.threat_intelligence.threatintel import ThreatIntel
threat_intel = ThreatIntel()
threat_intel.push_to_cb(feed_id='WLFoE6chQwy8z7CQGCTG8A',
                        results=report_list)
```

Now, an attempt will be made to send your Reports. The Reports will be saved to a file called reports.json, which can be helpful if sending Reports fails.

This is the full workflow in one code block:

```python
# import the relevant modules
from examples.enterprise_edr.threat_intelligence.threatintel import ThreatIntel
from examples.enterprise_edr.threat_intelligence.results import AnalysisResult

# info extracted from the IOC, with description shortened for clarity
title = "phish_domain: mncovidmasksewists.net"
id = "threatstream:Observable-7e740bc2-eeb2-443e-9c61-57baba2627f8"
description = "TS ID: 55474479396; iType: phish_domain; [...]"
timestamp = 1586211305
severity = 10
field = "netconn_domain"
value = "mncovidmasksewists.net"
link = "https://www.domaintools.com/resources/blog/free-covid-19-threat-list-domain-risk-assessments-for-coronavirus-threats"

# create a Report for the IOC
my_report = AnalysisResult(title=title, analysis_name=id, description=description,
                        timestamp=timestamp, score=severity)

# attach the IOC info to the Report
my_report.attach_ioc_v2(values=value, field=field, link=link)

# keep track of the Report in report_list
report_list = []
report_list.append(my_report)

# send the list of Reports to the Feed
threat_intel = ThreatIntel()
threat_intel.push_to_cb(feed_id='WLFoE6chQwy8z7CQGCTG8A',
                        results=report_list)
```

## Troubleshooting

### Credential Error
In order to use this code, you must have CBC SDK installed and configured. If you receive an authentication error, visit the Developer Network Authentication Page for [instructions on setting up authentication](https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/). See [ReadTheDocs](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication.html) for instructions on configuring your credentials file.

### 504 Gateway Timeout Error
The [Carbon Black Enterprise EDR Feed Manager API](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/feed-api/) is used in this code. When posting to a Feed, there is a 60 second limit before the gateway terminates your connection. The amount of reports you can POST to a Feed is limited by your connection speed. In this case, you will have to split your threat intelligence into smaller collections until the request takes less than 60 seconds, and send each smaller collection to an individual Enterprise EDR Feed.
