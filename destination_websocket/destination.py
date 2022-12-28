#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from websocket import create_connection
import json
from typing import Any, Iterable, Mapping

from airbyte_cdk import AirbyteLogger
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, Status, Type

print("")  # force PR tests


class DestinationWebsocket(Destination):
    def write(
            self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog,
            input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:

        websocket_url = config["websocket_url"]
        ws = create_connection(websocket_url)
        for message in input_messages:
            if message.type == Type.RECORD:
                ws.send(json.dumps(message.record.data))
            if message.type == Type.STATE:
                yield message
        ws.close()

    def check(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> AirbyteConnectionStatus:
        try:
            websocket_url = config["websocket_url"]
            ws = create_connection(websocket_url)
            ws.close()

            return AirbyteConnectionStatus(status=Status.SUCCEEDED)
        except Exception as e:
            return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred: {repr(e)}")
