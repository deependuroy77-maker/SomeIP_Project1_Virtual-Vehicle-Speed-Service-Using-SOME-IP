import asyncio

from someipy import (
    connect_to_someipy_daemon,
    ServiceBuilder,
    ServerServiceInstance,
    Method,
    Event,
    EventGroup,
    TransportLayerProtocol,
    MethodResult,
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
    PROVIDER_PORT,
    EVENT_PERIOD
)

# Current vehicle speed
current_speed = 60


# Method handler: GetSpeed
async def get_speed_handler(request_payload, client_address):

    print("GetSpeed request received from:", client_address)

    result = MethodResult()
    result.message_type = MessageType.RESPONSE
    result.return_code = ReturnCode.E_OK
    result.payload = Uint16(current_speed).serialize()

    print("Sending vehicle speed:", current_speed, "km/h")

    return result


async def main():

    global current_speed

    # Connect to SOME/IP daemon
    daemon = await connect_to_someipy_daemon()

    # Define GetSpeed method
    speed_method = Method(
        id=METHOD_ID_GET_SPEED,
        protocol=TransportLayerProtocol.UDP,
        method_handler=get_speed_handler
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

    # Build SOME/IP service
    speed_service = (
        ServiceBuilder()
        .with_service_id(SERVICE_ID)
        .with_major_version(MAJOR_VERSION)
        .with_method(speed_method)
        .with_eventgroup(speed_eventgroup)
        .build()
    )

    # Create provider instance
    provider = ServerServiceInstance(
        daemon=daemon,
        service=speed_service,
        instance_id=INSTANCE_ID,
        endpoint_ip=PROVIDER_IP,
        endpoint_port=PROVIDER_PORT,
        ttl=5,
        cyclic_offer_delay_ms=2000
    )

    # Offer service
    await provider.start_offer()

    print("Vehicle Speed Service is running.")
    print("Service ID:", hex(SERVICE_ID))
    print("Instance ID:", hex(INSTANCE_ID))
    print("Provider endpoint:", PROVIDER_IP, PROVIDER_PORT)

    try:

        while True:

            # Simulate changing vehicle speed
            current_speed = (current_speed + 5) % 121

            # Serialize speed
            speed_payload = Uint16(current_speed).serialize()

            # Publish event
            provider.send_event(
                EVENT_GROUP_ID,
                EVENT_ID_SPEED_CHANGED,
                speed_payload
            )

            print("SpeedChanged event:", current_speed, "km/h")

            await asyncio.sleep(EVENT_PERIOD)

    except KeyboardInterrupt:
        print("Stopping Vehicle Speed Service...")

    finally:
        await provider.stop_offer()
        await daemon.disconnect_from_daemon()


if __name__ == "__main__":
    asyncio.run(main())
