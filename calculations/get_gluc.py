import datetime
import gzip
import hashlib
import json
import logging
import os
import random
import string
from urllib.parse import urlparse
import tempfile
tempdir = tempfile.mkdtemp()

import arrow
import requests

MAX_RETRIES = 4

# Set up logging.
logger = logging.getLogger(__name__)

import base64

def convert_dict_to_bytes(input_dict):
    message = str(input_dict)
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)

    # msg_bytes = base64.b64decode(output_byte)
    # ascii_msg = msg_bytes.decode('ascii')
    # # Json library convert stirng dictionary to real dictionary type.
    # # Double quotes is standard format for json
    # ascii_msg = ascii_msg.replace("'", "\"")
    # output_dict = json.loads(ascii_msg)  # convert string dictionary to dict format
    return output_byte


def get_ns_entries(ns_url, before_date, after_date):
    """
    Get Nightscout entries data, ~60 days at a time.

    Retrieve ~60 days at a time until either (a) the start point is reached
    (after_date parameter) or (b) a run of 6 empty calls or (c) Jan 2010.
    """
    filepath = os.path.join(tempdir, '{}'.format("entries") + '_' + after_date + '_to_' + before_date + '.json.gz')
    # file_obj = gzip.open(filepath, 'wb')
    data = ""
    end = arrow.get(before_date).ceil('second').timestamp() * 1000
    start = arrow.get('2010-01-01').floor('second').timestamp() * 1000
    if after_date:
        start = arrow.get(after_date).floor('second').timestamp() * 1000

    ns_entries_url = ns_url + '/api/v1/entries.json'

    # Start a JSON array.
    data += "["
    # file_obj.write('['.encode())
    initial_entry_done = False  # Entries after initial are preceded by commas.

    # Get 8 million second chunks (~ 1/4th year) until none, or start reached.
    complete = False
    curr_end = end
    curr_start = curr_end - 5000000000
    empty_run = 0
    retries = 0
    while not complete:
        if curr_start < start:
            curr_start = start
            complete = True
            logger.debug('Final round (starting date reached)...')
        ns_params = {'count': 1000000}
        ns_params['find[date][$lte]'] = curr_end
        ns_params['find[date][$gt]'] = curr_start
        entries_req = requests.get(ns_entries_url, params=ns_params)
        logger.debug('Request complete.')
        assert entries_req.status_code == 200 or retries < MAX_RETRIES, \
            'NS entries URL != 200 status'
        if entries_req.status_code != 200:
            retries +=1
            logger.debug("RETRY {}: Status code is {}".format(
                retries, entries_req.status_code))
            continue
        logger.debug('Status code 200.')
        retries = 0
        logger.debug('Retrieved {} entries...'.format(len(entries_req.json())))
        if entries_req.json():
            empty_run = 0
            for entry in entries_req.json():
                if initial_entry_done:
                    data += ","
                    # file_obj.write(',')  # JSON array separator
                else:
                    initial_entry_done = True
                # entry = convert_dict_to_bytes(entry)
                # print(entry)
                # json.dump(entry, file_obj)
                data += json.dumps(entry)
            logger.debug('Wrote {} entries to file...'.format(len(entries_req.json())))
        else:
            empty_run += 1
            if empty_run > 6:
                logger.debug('>10 empty calls: ceasing entries queries.')
                break
        curr_end = curr_start
        curr_start = curr_end - 5000000000
    data += "]"
    # file_obj.write(']'.encode())  # End of JSON array
    out_file = open("glucose_values.json", "w")
    out_file.write(data)
    out_file.close()
    logger.debug('Done writing entries to file.')


if __name__ == '__main__':
    from datetime import datetime as dt
    get_ns_entries("https://tig-diab.herokuapp.com","2022-04-21","")