""" MicroNG"""

import os
import re
import csv
import math
import pandas as pd
import numpy as np
import json
from pathlib import Path
import sys

sys.path.append("/devel/mwillia3/branches/mock_msg")
from pairclient import Publisher


def createstat(file_path, currentDict):

    with open("{}".format(file_path)) as file:
        for line in file.readlines():
            if line.startswith("hostname:"):
                hostname = line.split(":")[1].strip()
            if line.startswith("userid:"):
                userid = line.split(":")[1].strip()
            if line.startswith("network:"):
                network = line.split(":")[1].strip()
            if line.startswith("protocol:"):
                protocol = line.split(":")[1].strip()
            if line.startswith("start_datetime:"):
                start_datetime = line.split(":")[1].strip()
            if line.startswith("end_datetime:"):
                end_datetime = line.split(":")[1].strip()
            if line.startswith("runtype:"):
                runtype = line.split(":")[1].strip()
            if line.startswith("step_name:"):
                step_name = line.split(":")[1].strip()
            if line.startswith("elapsed_time_secs:"):
                elapsed_time_secs = line.split(":")[1].strip()

            if line.startswith("error_code:"):
                error_code = line.split(":")[1].strip()
            if line.startswith("error_message:"):
                error_message = line.split(":")
            # if line.startswith("ERROR:"):
            #     sas_error = line.split(":")
            #     print(sas_error)
        currentDict["TABLE_NAME"] = "lp_sm"
        currentDict["hostname"] = hostname
        currentDict["userid"] = userid
        currentDict["network"] = network
        currentDict["protocol"] = protocol
        currentDict["start_datetime"] = start_datetime
        currentDict["end_datetime"] = end_datetime
        currentDict["runtype"] = runtype
        currentDict["step_name"] = step_name
        currentDict["elapsed_time_secs"] = elapsed_time_secs
        currentDict["error_code"] = error_code
        if error_code == "0":
            currentDict["error_message"] = error_message[1]
        else:
            currentDict["error_message"] = " ".join(error_message)
        currentDict["log_file"] = file_path

        # if error_code == "0":
        #     if "sas_error" in globals():
        #         currentDict["error_message"] = sas_error
        #         currentDict["error_code"] = "999"
        #     else:
        #         currentDict["error_message"] = error_message[1]
        # else:
        #     currentDict["error_message"] = " ".join(error_message)
        # currentDict["log_file"] = file_path

    # b = pd.DataFrame(currentDict, index=[0])
    return currentDict


def loop_protocols(network, protocols, steps, currentDict):
    # df_accum = pd.DataFrame(
    #     columns=[
    #         "hostname",
    #         "userid",
    #         "network",
    #         "protocol",
    #         "start_datetime",
    #         "end_datetime",
    #         "runtype",
    #         "step_name",
    #         "elapsed_time_secs",
    #         "error_code",
    #         "error_message",
    #         "log_file",
    #     ]
    # )
    for prot in protocols:
        # path='/trials/LabDataOps/{}/protocols/{}/logs'.format(network, prot)
        path = "/devel/ksharma/LDP-3114/{}/protocols/{}/logs".format(
            network, prot
        )
        for step in steps:
            name = "{}{}_run_sm_protocol_{}.log".format(network, prot, step)
            file_path = os.path.join(path, name)
            try:
                currentDict = createstat(file_path, currentDict)
                pub = Publisher()
                pub.send_json(currentDict)
                print(currentDict)

                # print(df.info())
                # print(
                #     df.loc[
                #         :,
                #         ["protocol", "step_name", "error_message", "log_file"],
                #     ]
                # )
            #     df_accum = df_accum.append(
            #         df[
            #             [
            #                 "hostname",
            #                 "userid",
            #                 "network",
            #                 "protocol",
            #                 "start_datetime",
            #                 "end_datetime",
            #                 "runtype",
            #                 "step_name",
            #                 "elapsed_time_secs",
            #                 "error_code",
            #                 "error_message",
            #                 "log_file",
            #             ]
            #         ],
            #         ignore_index=True,
            #     )
            except Exception as inst:
                print(f"File Error...{inst}")

    # print(df_accum.loc[:, ["protocol", "step_name", "error_message"]])
    # result = df_accum.to_json(orient="split")
    # parsed = json.loads(result)
    # print(type(parsed))
    # fileName = "SM_LOG_MONITOR"
    # filePathNameWExt = "/devel/ksharma/LDP-3114/" + fileName + ".json"
    # with open(filePathNameWExt, "w") as fp:
    #     json.dump(
    #         parsed,
    #         fp,
    #         sort_keys=True,
    #         indent=4,
    #     )


def main():
    currentDict = {}

    network = "mtn"
    protocols = ["042", "039", "043", "035"]
    steps = ["gatherdata", "findqcs", "commitqcs", "makereports"]
    loop_protocols(network, protocols, steps, currentDict)


if __name__ == "__main__":
    main()
