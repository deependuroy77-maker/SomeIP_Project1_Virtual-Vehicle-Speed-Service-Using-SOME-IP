import asyncio

from someipy import (
    connect_to_someipy_daemon,
    ServiceBuilder,
    ClientServiceInstance,
    Method,
    Event,
    EventGroup,
    TransportLayerProtocol,
    MessageType,
    ReturnCode
)

from someipy.serialization import Uint16

from service_config import (
    SERVICE_ID,
    INSTANCE_ID,
    MAJOR_VERSION,
    METHOD_ID_GET_SPEED,
    EVENT_ID_SPEED_CHANGED,
    EVENT_GROUP_ID,
    PROVIDER_IP,
    CONSUMER_IP,
    CONSUMER_PORT
)


# Callback for SpeedChanged event
def speed_changed_callback(event_id, payload):

    if event_id == EVENT_ID_SPEED_CHANGED:
        speed = int.from_bytes(payload, byteorder="big")
        print("SpeedChanged Event:", speed, "km/h")


async def main():

    # Connect to SOME/IP daemon
    daemon = await connect_to_someipy_daemon()

    # Define GetSpeed method
    speed_method = Method(
        id=METHOD_ID_GET_SPEED,
        protocol=TransportLayerProtocol.UDP
    )

    # Define SpeedChanged event
    speed_event = Event(
        id=EVENT_ID_SPEED_CHANGED,
        protocol=TransportLayerProtocol.UDP
    )

    # Define event group
    speed_eventgroup = EventGroup(
        id=EVENT_GROUP_ID,
        events=[speed_event]
    )

    # Build service definition
    speed_service = (
        ServiceBuilder()
        .with_service_id(SERVICE_ID)
        .with_major_version(MAJOR_VERSION)
        .with_method(speed_method)
        .with_eventgroup(speed_eventgroup)
        .build()
    )

    # Create consumer instance
    consumer = ClientServiceInstance(
        daemon=daemon,
        service=speed_service,
        instance_id=INSTANCE_ID,
        endpoint_ip=CONSUMER_IP,
        endpoint_port=CONSUMER_PORT
    )

    # Register event callback
    consumer.register_callback(speed_changed_callback)

    print("Instrument Cluster started.")
    print("Waiting for Vehicle Speed Service...")

    try:

        # Wait until provider becomes available
        while not await consumer.is_available():
            await asyncio.sleep(1)

        print("Vehicle Speed Service discovered!")

        # Call GetSpeed method
        result = await consumer.call_method(
            METHOD_ID_GET_SPEED,
            b""
        )

        if (
            result.message_type == MessageType.RESPONSE
            and result.return_code == ReturnCode.E_OK
        ):
            speed = int.from_bytes(result.payload, byteorder="big")
            print("GetSpeed Response:", speed, "km/h")
        else:
            print("GetSpeed request failed:", result.return_code)

        # Subscribe to SpeedChanged event group
        consumer.subscribe_eventgroup(speed_eventgroup, 5)

        print("Subscribed to SpeedChanged event.")
        print("Waiting for speed notifications...")

        await asyncio.Future()

    except KeyboardInterrupt:
        print("Stopping Instrument Cluster...")

    finally:
        await daemon.disconnect_from_daemon()


if __name__ == "__main__":
    asyncio.run(main())
