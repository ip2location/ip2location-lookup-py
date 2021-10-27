from __future__ import print_function

import os
import platform
import time
import sys
import argparse
import IP2Location
from re import match
# from shutil import copyfile

ip2location_result_fields = ['ip', 'country_short', 'country_long', 'region', 'city', 'isp', 'latitude', 'longitude', 'domain', 'zipcode', 'timezone', 'netspeed', 'idd_code', 'area_code', 'weather_code', 'weather_name', 'mcc', 'mnc', 'mobile_brand', 'elevation', 'usage_type', 'address_type', 'category', ]
ip2location_outputs_reference = ['ip', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'latitude', 'longitude', 'domain', 'zip_code', 'time_zone', 'net_speed', 'idd_code', 'area_code', 'weather_station_code', 'weather_station_name', 'mcc', 'mnc', 'mobile_brand', 'elevation', 'usage_type', 'address_type', 'category', ]

# Define BIN database default path
if platform.system() == 'Windows':
    default_path = os.path.expanduser('~') + os.sep + "Documents" + os.sep
# elif platform.system() === 'Linux ':
else:
    default_path = '/usr/share/ip2location/'

# Now we copy the BIN database to default_path here instead of doing it duing installation as pip kept copied to wrong location.
'''
if (os.path.isfile(default_path + "IP2LOCATION-LITE-DB1.IPV6.BIN") == False):
    try:
        # create the dir is not exist
        if (os.path.exists(default_path) is False):
            os.mkdir(default_path)
        copyfile(os.path.dirname(os.path.realpath(__file__)) + os.sep + "data" + os.sep + "IP2LOCATION-LITE-DB1.IPV6.BIN", default_path + "IP2LOCATION-LITE-DB1.IPV6.BIN")
    except PermissionError as e:
        sys.exit("Root permission is required. Please rerun it as 'sudo ip2locationpy'.")
'''

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ip', metavar='Specify an IP address or hostname.')
    parser.add_argument('-d', '--database', metavar='Specify the path of IP2Location BIN database file.')
    parser.add_argument('-i', '--input_file', metavar='Specify an input file of IP address list, one IP per row.')
    parser.add_argument('-o', '--output_file', metavar='Specify an output file to store the lookup results.')
    parser.add_argument('-e', '--field', metavar='Output the field data.')
    parser.add_argument('-f', '--format', default="CSV", metavar='Output format.')
    parser.add_argument('-n', '--no_heading', action='store_true')
    # parser.add_argument('-b', '--bin_version', action='store_true')

    return parser

def print_usage():
    print(
"ip2location -p [IP ADDRESS] -d [IP2LOCATION BIN DATA PATH] [OPTIONS]\n"
"   -d, --data-file\n"
"       Specify the path of IP2Location BIN data file.\n"
"\n"
"   -e, --field\n"
"       Output the field data.\n"
"       Field name includes:\n"
"           country_code     \n"
"           Two-character country code based on ISO 3166.\n"
"\n"
"           country_name\n"
"           Country name based on ISO 3166.\n"
"\n"
"           region_name\n"
"           Region or state name.\n"
"\n"
"           city_name\n"
"           City name.\n"
"\n"
"           latitude\n"
"           City latitude. Defaults to capital city latitude if the city is unknown.\n"
"\n"
"           longitude\n"
"           City longitude. Defaults to capital city longitude if the city is unknown.\n"
"\n"
"           zip_code\n"
"           ZIP/Postal code (170 countries supported).\n"
"\n"
"           time_zone\n"
"           UTC time zone (with DST supported).\n"
"\n"
"           isp\n"
"           Internet Service Provider or company's name.\n"
"\n"
"           domain\n"
"           Internet domain name associated with IP address range.\n"
"\n"
"           net_speed\n"
"           Internet connection type.\n"
"\n"
"           idd_code\n"
"           The IDD prefix to call the city from another country.\n"
"\n"
"           area_code\n"
"           A varying length number assigned to geographic areas for calls between cities (221 countries supported).\n"
"\n"
"           weather_station_code\n"
"           The special code to identify the nearest weather observation station.\n"
"\n"
"           weather_station_name\n"
"           The name of the nearest weather observation station.\n"
"\n"
"           mcc\n"
"           Mobile Country Codes (MCC) as defined in ITU E.212 for use in identifying mobile stations in wireless telephone networks, particularly GSM and UMTS networks.\n"
"\n"
"           mnc\n"
"           Mobile Network Code (MNC) is used in combination with a Mobile Country Code (MCC) to uniquely identify a mobile phone operator or carrier.\n"
"\n"
"           mobile_brand\n"
"           Commercial brand associated with the mobile carrier. You may click here to view the coverage report.\n"
"\n"
"           elevation\n"
"           Average height of the city above sea level in meters (m).\n"
"\n"
"           usage_type\n"
"           Usage type classification of ISP or company.\n"
"\n"
"   -f, --format\n"
"   Output format. Supported format:\n"
"       - CSV (default)\n"
"       - TAB\n"
"       - XML\n"
"\n"
"   -h, -?, --help\n"
"   Display the help.\n"
"\n"
"   -i, --input_file\n"
"   Specify an input file of IP address list, one IP per row.\n"
"\n"
"   -n, --no_heading\n"
"   Suppress the heading display.\n"
"\n"
"   -o, --output_file\n"
"   Specify an output file to store the lookup results.\n"
"\n"
"   -p, --ip\n"
"   Specify an IP address query (Supported IPv4 and IPv6 address).\n"
"\n"
"   -v, --version\n"
"   Print the version of the IP2Location version.\n")

def print_version():
    print(
"IP2Location™ Applications Version 8.0.0\n"
"Copyright (c) 2021 IP2Location.com [MIT License]\n"
"https://www.ip2location.com/free/applications\n")
    
def print_header(format, output_file, field):
    row = None
    if format == "CSV":
        # row = '"'
        row = ''
        if field is not None:
            output = field.split(",")
            for i in output:
                if (i in ip2location_outputs_reference):
                    row = row + '"' + str(i) + '",'
        else:
            for i in range(0, len(ip2location_outputs_reference)):
                row = row + '"' + str(ip2location_outputs_reference[i]) + '",'
        if row.endswith(','):
            row = row[:-1]
    elif format == 'TAB':
        row = ''
        if field is not None:
            output = field.split(",")
            for i in output:
                if (i in ip2location_outputs_reference):
                    row = row + str(i) + '\t'
        else:
            for i in range(0, len(ip2location_outputs_reference)):
                row = row + str(ip2location_outputs_reference[i]) + '\t'
        if row.endswith('\t'):
            row = row[:-1]
    if row is not None:
        print("{}".format(row), end="")
        print()
    if output_file is not None and row is not None:
        output_file.write(row + '\n')

class Lookup:
    def __init__(self, ip, database):
        self.ip = ip
        self.database = database

        if (ip is None):
            print ("Missing IP address or hostname.")
            sys.exit()

        # Open up IP2Location BIN file
        if (database is not None):
            if os.path.isfile(database) == False:
                # Now will check if the filename passed is a BIN extension or not
                if database.upper().endswith(".BIN"):
                    # check if the given filename is under current dir or not.
                    if (os.getcwd().endswith(os.sep)):
                        filepath = os.getcwd() + database
                    else:
                        filepath = os.getcwd() + os.sep + database
                    # print(filepath)
                    if os.path.isfile(filepath) == False:
                        if os.path.isfile(default_path + database) == False:
                            print("BIN database file not found.")
                            sys.exit()
                        else:
                            self.obj = IP2Location.IP2Location(default_path + database)
                    else:
                        self.obj = IP2Location.IP2Location(filepath)
                else:
                    print("Only BIN database is accepted. You can download the latest free IP2Location BIN database from https://lite.ip2location.com.")
                    sys.exit()
            else:
                self.obj = IP2Location.IP2Location(database)
        else:
            if (os.path.isfile(default_path + "IP2LOCATION-LITE-DB1.IPV6.BIN") != False):
                self.obj = IP2Location.IP2Location(default_path + "IP2LOCATION-LITE-DB1.IPV6.BIN")
            else:
                print("Missing IP2Location BIN database. Please enter ‘ip2locationpy -h’ for more information.")
                sys.exit()
        
    def query(self):
        record = self.obj.get_all(self.ip)
        return record
    
    def print_record(self, record, format, output_file, field):
        record_dict = {}
        for attr, value in record.__dict__.items():
            record_dict[attr] = value
        if format == "CSV":
            # row = '"'
            row = ''
            if field is not None:
                output = field.split(",")
                for i in output:
                    # if (i in ip2location_outputs_reference):
                    if (i in ip2location_outputs_reference):
                        if (ip2location_result_fields[ip2location_outputs_reference.index(i)] in record_dict) and (record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]] is not None):
                            row = row + '"' + str(record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]]) + '",'
                        else:
                            if i == 'latitude' or i == 'longitude':
                                row = row + '"0.000000",'
                            else:
                                row = row + '"N/A",'
            else:
                for i in range(0, len(ip2location_result_fields)):
                    if (ip2location_result_fields[i] in record_dict) and (record_dict[ip2location_result_fields[i]] is not None):
                        row = row + '"' + str(record_dict[ip2location_result_fields[i]]) + '",'
                    else:
                        if ip2location_outputs_reference[i] == 'latitude' or ip2location_outputs_reference[i] == 'longitude':
                            row = row + '"0.000000",'
                        else:
                            row = row + '"N/A",'
            if row.endswith(','):
                row = row[:-1]
        elif format == "XML":
            row = '<row>'
            if field is not None:
                output = field.split(",")
                for i in output:
                    if (i in ip2location_outputs_reference):
                        if (ip2location_result_fields[ip2location_outputs_reference.index(i)] in record_dict) and (record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]] is not None):
                            row = row + "<" + str(i) + ">" + str(record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]]) + "</" + str(i) + ">"
                        else:
                            if i == 'latitude' or i == 'longitude':
                                row = row + "<" + str(i) + ">" + '0.000000' + "</" + str(i) + ">"
                            else:
                                row = row + "<" + str(i) + ">" + 'N/A' + "</" + str(i) + ">"
            else:
                for i in range(0, len(ip2location_result_fields)):
                    if (ip2location_result_fields[i] in record_dict) and (record_dict[ip2location_result_fields[i]] is not None):
                        row = row + "<" + str(ip2location_outputs_reference[i]) + ">" + str(record_dict[ip2location_result_fields[i]]) + "</" + str(ip2location_outputs_reference[i]) + ">"
                    else:
                        if ip2location_outputs_reference[i] == 'latitude' or ip2location_outputs_reference[i] == 'longitude':
                            row = row + "<" + str(ip2location_outputs_reference[i]) + ">" + '0.000000' + "</" + str(ip2location_outputs_reference[i]) + ">"
                        else:
                            row = row + "<" + str(ip2location_outputs_reference[i]) + ">" + 'N/A' + "</" + str(ip2location_outputs_reference[i]) + ">"
            row = row + '</row>'
        elif format == "TAB":
            row = ''
            if field is not None:
                output = field.split(",")
                for i in output:
                    if (i in ip2location_outputs_reference):
                        if (ip2location_result_fields[ip2location_outputs_reference.index(i)] in record_dict) and (record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]] is not None):
                            row = row + str(record_dict[ip2location_result_fields[ip2location_outputs_reference.index(i)]]) + '\t'
                        else:
                            if i == 'latitude' or i == 'longitude':
                                row = row + '0.000000\t'
                            else:
                                row = row + 'N/A\t'
            else:
                for i in range(0, len(ip2location_result_fields)):
                    if (ip2location_result_fields[i] in record_dict) and (record_dict[ip2location_result_fields[i]] is not None):
                        row = row + str(record_dict[ip2location_result_fields[i]]) + '\t'
                    else:
                        if ip2location_outputs_reference[i] == 'latitude' or ip2location_outputs_reference[i] == 'longitude':
                            row = row + '0.000000\t'
                        else:
                            row = row + 'N/A\t'
            if row.endswith('\t'):
                row = row[:-1]
        print("{}".format(row), end="")
        print()
        if output_file is not None:
            output_file.write(row + '\n')


# if __name__ == '__main__':
def main():
    is_help = False
    # print(sys.argv)
    if len(sys.argv) >= 2:
        for index, arg in enumerate(sys.argv):
            if arg in ['--help', '-h', '-?']:
                print_usage()
                is_help = True
            elif arg in ['--version', '-v']:
                print_version()
                is_help = True
        if is_help is False:
            parser = create_parser()
            args = parser.parse_args(sys.argv[1:])
            if args.no_heading is not None:
                no_heading = args.no_heading
            else:
                no_heading = False
            database = args.database
            format = args.format
            field = args.field
            # output_file = args.output_file
            # print (args.field)
            if args.output_file is not None:
                    output_file_pointer = open(args.output_file, 'a', encoding="utf-8")
            else:
                output_file_pointer = None
            if format != "CSV" and format != "XML" and format != "TAB":
                print("Invalid format {}, supported formats: CSV, XML, TAB\n".format(format))
                sys.exit()
            if no_heading is False:
                print_header(format, output_file_pointer, field)
            if args.ip is not None:
                new_lookup = Lookup(args.ip, database)
                record = new_lookup.query()
                if format == "XML":
                    print("<xml>", end="")
                    print()
                    if output_file_pointer is not None:
                        output_file_pointer.write("<xml>" + '\n')
                new_lookup.print_record(record, format, output_file_pointer, field)
                if format == "XML":
                    # print()
                    print("</xml>", end="")
                    if output_file_pointer is not None:
                        output_file_pointer.write("</xml>" + '\n')
            if args.input_file is not None:
                if os.path.isfile(args.input_file) == False:
                    # check if the given filename is under current dir or not.
                    if (os.getcwd().endswith(os.sep)):
                        filepath = os.getcwd() + args.input_file
                    else:
                        filepath = os.getcwd() + os.sep + args.input_file
                    # print(filepath)
                    if os.path.isfile(filepath) == False:
                        if os.path.isfile(default_path + args.input_file) == False:
                            print("input file not found.")
                            sys.exit()
                        else:
                            ip_list = open(default_path + args.input_file,'r').read().split('\n')
                    else:
                        ip_list = open(filepath,'r').read().split('\n')
                else:
                    ip_list = open(args.input_file,'r').read().split('\n')
                # print(len(ip_list))
                if len(ip_list) > 0:
                    if format == "XML":
                        print("<xml>", end="")
                        print()
                        if output_file_pointer is not None:
                            output_file_pointer.write("<xml>" + '\n')
                    for ip in ip_list:
                        new_lookup = Lookup(ip, database)
                        record = new_lookup.query()
                        new_lookup.print_record(record, format, output_file_pointer, field)
                    if format == "XML":
                        print()
                        print("</xml>", end="")
                        if output_file_pointer is not None:
                            output_file_pointer.write("</xml>" + '\n')
            if output_file_pointer is not None:
                output_file_pointer.close()
    else:
        print("Missing parameters. Please enter 'ip2locationpy -h' for more information.")