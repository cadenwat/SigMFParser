'''
GOAL:

Take the json file parsed and repackage it into data chuncks in the same format for use in a neural network
'''
import numpy as np
import sigmf
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str, get_sigmf_iso8601_datetime_now
import os
from collections import defaultdict
import json
import argparse

# Chunck Size (in units of captures)
segSize = 10000


# Packages a single file with data segement
def savesegment(name, data, location):
    # Recconsruct the original structure
    """
    "metadata": {
            "annotations": [],
            "captures": [
                {
                    "capture_details:gain": 30.0,
                    "core:datetime": "2025-06-03T18:14:35Z",
                    "core:frequency": 914500000.0,
                    "core:sample_start": 0
                }
            ]
    """
    captures = {
        "capture_details:gain": 30.0,
        "core:datetime": "2025-06-03T18:14:35Z",
        "core:frequency": 914500000.0,
        "core:sample_start": 0
    }
    metadata = {
        "annotations": [],
        "captures": captures
    }

    '''
    "global": {
                "antenna:type": "UNK",
                "core:datatype": "cf32_le",
                "core:description": "OmniSIG Recording",
                "core:extensions": [
                    {
                        "name": "antenna",
                        "optional": true,
                        "version": "1.0.0"
                    },
                    {
                        "name": "spatial",
                        "optional": true,
                        "version": "1.0.0"
                    },
                    {
                        "name": "capture_details",
                        "optional": true,
                        "version": "1.0.0"
                    },
                    {
                        "name": "deepsig",
                        "optional": true,
                        "version": "1.0.0"
                    }
                ],
                "core:recorder": "OmniSIG Sensor v3.4.2",
                "core:sample_rate": 25000000.0,
                "core:version": "1.1.0",
                "deepsig:classifier_model": "Default",
                "deepsig:sensor_id": "rfdp451-Titan-18-HX-A14VIG"
            }
        },
        '''
    extension = [
                    {
                        "name": "antenna",
                        "optional": True,
                        "version": "1.0.0"
                    },
                    {
                        "name": "spatial",
                        "optional": True,
                        "version": "1.0.0"
                    },
                    {
                        "name": "capture_details",
                        "optional": True,
                        "version": "1.0.0"
                    },
                    {
                        "name": "deepsig",
                        "optional": True,
                        "version": "1.0.0"
                    }
                ]
    glob = {
        "antenna:type": "UNK",
        "core:datatype": "cf32_le",
        "core:description": "OmniSIG Recording",
        "core:extensions": extension,
        "core:recorder": "OmniSIG Sensor v3.4.2",
        "core:sample_rate": 25000000.0,
        "core:version": "1.1.0",
        "deepsig:classifier_model": "Default",
         "deepsig:sensor_id": "rfdp451-Titan-18-HX-A14VIG"
    }

    # NEW DETAILS
    data = {
        "timeseries_samples": data
    }


    # Tack on the end
    globalInfo = {
        "antenna:type": "UNK",
        "core:datatype": "cf32_le",
        "core:description": "OmniSIG Recording",
        "core:extensions": [
            {
                "name": "antenna",
                "optional": True,
                "version": "1.0.0"
            },
            {
                "name": "spatial",
                "optional": True,
                "version": "1.0.0"
            },
            {
                "name": "capture_details",
                "optional": True,
                "version": "1.0.0"
            },
            {
                "name": "deepsig",
                "optional": True,
                "version": "1.0.0"
            }
        ],
        "core:recorder": "OmniSIG Sensor v3.4.2",
        "core:sample_rate": 25000000.0,
        "core:version": "1.2.5",
        "deepsig:classifier_model": "Default",
        "deepsig:sensor_id": "rfdp451-Titan-18-HX-A14VIG",
        "core:num_channels": 1,
        "core:sha512": "493ae75eb24e83c94cf898ee84c005110d991a5461d57e9169fd12f70c8f848009db4ba506b8bd79d5727d03153081d8965ba09c9d685c7de705e3bf5a7da1d6"
    }
               

    output = {
        "metadata": metadata,
        "global": glob,
        "data": data,
        "global_info": globalInfo,
        "captures": [
        {
            "capture_details:gain": 30.0,
            "core:datetime": "2025-06-03T18:14:35Z",
            "core:frequency": 914500000.0,
            "core:sample_start": 0
        }
        ],
        "annotations": []
    }

    
    
    


    # Ensure save directory exists
    os.makedirs(location, exist_ok=True)

    # Build the file path
    filepath = os.path.join(location, f"{name}.json")

    # Write the JSON
    with open(filepath, "w") as f:
        json.dump(output, f, indent=4)

    print(f"[+] Saved segment to {filepath}")



# Import json file into python
with open('data/export/dataset-onerecord-timeseriesincluded.json', 'r') as f:
    data = json.load(f)

    seg = 0
    segment = []
    num = 1
    for i in data['2025-06-03-18-14-35_915MHz_chan_0']['data']["timeseries_samples"]:
        seg += 1
        
        segment.append(i)
        if seg >= segSize:
            savesegment("Segment " + str(num), segment, 'segments')
            segment = []
            seg = 0
            num += 1
    # save the last segment
    savesegment("Segment " + str(num), segment, 'segments')
