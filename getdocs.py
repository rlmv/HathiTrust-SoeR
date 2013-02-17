#! /usr/local/bin/python

import sys
import os
import argparse
from string import replace

from requests.exceptions import RequestException

from hathitrust_api.data_api import DataAPI
from oauth_keys import client_key, client_secret


def get_data_and_write(htid, target_dir, data_resource):

    # convert to valid file name
    fname = replace(htid, ':', '+')
    fname = replace(fname, '/', '=')
    fname = fname + '.zip'

    try:
        r = data_resource.getaggregate(htid)
        fpath = os.path.join(target_dir, fname)
        with open(fpath, 'w') as f:
            f.write(r)

    except RequestException as re:
        print "Error with request: {}".format(re)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="An interactive document retriever for the HathiTrust data API.")
    parser.add_argument('targetdir', metavar='TARGETDIR',
        help="Retrieved files are stored in this directory.")
    parser.add_argument('id_file', metavar='IDFILE',
        nargs='?', 
        default=False,
        help="Path to a file of HathiTrust identifiers.")

    args = parser.parse_args()
    if not os.path.exists(args.targetdir):
        raise Exception("Target directory does not exist.")


    try:
        dataresource = DataAPI(client_key, client_secret)

        if args.id_file:
            with open(args.id_file, 'r') as f:
                for line in f:
                    get_data_and_write(line, args.targetdir, dataresource)

        else: # ineractive
            while True:
                s = raw_input("Enter target htid >> ")         
                get_data_and_write(s, args.targetdir, dataresource)

    except KeyboardInterrupt:
        print '/n'
        sys.exit()
            
            