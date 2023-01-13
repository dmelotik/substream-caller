#!/usr/bin/env python3

from ast import arg
import http.client
import sys
import os
import time
import grpc
import sys
import base64

from google.protobuf.json_format import MessageToDict

from sf.substreams.v1 import substreams_pb2_grpc
from sf.substreams.v1.substreams_pb2 import Request, STEP_IRREVERSIBLE
from sf.substreams.v1.substreams_pb2 import ModuleOutput
from sf.substreams.v1.package_pb2 import Package

jwt_token = os.getenv("SUBSTREAMS_API_TOKEN")
if not jwt_token: raise Error("set SUBSTREAMS_API_TOKEN")
endpoint = "api.streamingfast.io:443"
package_pb = "./spkgs/" + sys.argv[2] + ".spkg"
output_modules = [sys.argv[8]]
start_block = int(sys.argv[4])
end_block = start_block + int(sys.argv[6])
output = {}

def substreams_service():
    credentials = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt_token),
    )
    channel = grpc.secure_channel(endpoint, credentials=credentials)
    return substreams_pb2_grpc.StreamStub(channel)

def print_output():
    print("\n\n")
    print("Output: ", len(output))
    for key, value in output.items():
        print(key, value)

def main():
    with open(package_pb, 'rb') as f:
        pkg = Package()
        pkg.ParseFromString(f.read())

    service = substreams_service()
    stream = service.Blocks(Request(
        start_block_num=start_block,
        stop_block_num=end_block,
        fork_steps=[STEP_IRREVERSIBLE],
        modules=pkg.modules,
        output_modules=output_modules,
        # initial_store_snapshot_for_modules=output_modules
    ))

    start_time = time.time()
    last_time = start_time

    for response in stream:
        # progress message
        if response.progress and (time.time() - last_time) >= 5:
            print("time elapsed: %.2fs" % (time.time() - start_time))
            last_time = time.time()
        
        snapshot = MessageToDict(response.snapshot_data)

        if snapshot and snapshot["moduleName"] == output_modules[0]:
            snapshot_deltas = snapshot["deltas"]
            if snapshot_deltas:
                deltas = snapshot_deltas["deltas"]
                for delta in deltas:
                    key = delta["key"]
                    value = base64.b64decode(delta["newValue"])
                    output[key] = value
    
    print_output()

main()