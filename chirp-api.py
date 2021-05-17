import os
import sys
import time

import grpc
from chirpstack_api.as_pb.external import api

# Configuration.

# This must point to the API interface.
server = "138.68.97.249:8080"

# The DevEUI for which you want to enqueue the downlink.
dev_eui = bytes([0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x03, 0x07])

# The API token (retrieved using the web-interface).
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiNDU2MWY1M2EtYTBkMy00NzQyLWJjYjItMWYzYjRmZDFjMGM5IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTYyMTIzNjYxMSwic3ViIjoiYXBpX2tleSJ9.lNXzswwZtVsyOPGwiHS03X_pTUvBlmi0pokij1gsIOg"

def send_msg(dev_eui, client, auth_token, msg):
    req = api.EnqueueDeviceQueueItemRequest()
    req.device_queue_item.confirmed = False
    req.device_queue_item.data = bytes(msg, "utf-8")
    req.device_queue_item.dev_eui = dev_eui.hex()
    req.device_queue_item.f_port = 201
    resp = client.Enqueue(req, metadata=auth_token)
    # Print the downlink frame-counter value.
    print(resp.f_cnt)

if __name__ == "__main__":
  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceQueueServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % api_token)]

  for i in range(0, 10):
    update_string = "UpdateData" + str(i).rjust(4, '0') + "Garbage1337" + "Garbage1337" + "Garbage1337"
    send_msg(dev_eui, client, auth_token, update_string)
    time.sleep(4)

  