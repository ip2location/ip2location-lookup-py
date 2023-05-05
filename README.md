# IP2Locationpy

IP2Locationpy is a Python tool allowing user to get IP address information such as country, region, city, latitude, longitude, zip code, time zone, ISP, domain name, connection type, area code, weather, mobile network, elevation, usage type, address type, IAB category, district, autonomous system number (ASN) and autonomous system (AS) by IP address (IPv4 or IPv6) from IP2Location BIN database.

For more details, please visit:
https://www.ip2location.com/free/applications

### Installation

You can install this tool by using pip in Windows or Linux. To install this tool in Windows and Linux, just type `pip install IP2Locationpy` in your console and IP2Location-Lookup will be installed in your machine.

*Note: This tool require [IP2Location](https://github.com/chrislim2888/IP2Location-Python) library to work with. If pip did not install the dependency for you, you can manually install it by using `pip install IP2Location`.*

### Usage

Query an IP address and display the result

```
ip2locationpy -d [IP2LOCATION BIN DATA PATH] --ip [IP ADDRESS]  
```

Query all IP addresses from an input file and display the result

```
ip2locationpy -d [IP2LOCATION BIN DATA PATH] -i [INPUT FILE PATH]  
```

Query all IP addresses from an input file and display the result in XML format

```
ip2locationpy -d [IP2LOCATION BIN DATA PATH] -i [INPUT FILE PATH] --format XML  
```

## Download More Sample Databases

```
wget https://www.ip2location.com/downloads/sample.bin.db26.zip
unzip samples-db26.zip
```

## Support

Email: [support@ip2location.com](mailto:support@ip2location.com)
URL: [https://www.ip2location.com](https://www.ip2location.com/)
