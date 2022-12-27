#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from destination_websocket import DestinationWebsocket

if __name__ == "__main__":
    DestinationWebsocket().run(sys.argv[1:])
