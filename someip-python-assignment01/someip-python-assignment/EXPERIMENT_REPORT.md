# Experiment Report: SOME/IP Vehicle Speed Service

## Objective
To implement SOME/IP communication between a virtual Vehicle ECU
and an Instrument Cluster using Python and someipy.

## Implementation
- Provider: Vehicle ECU
- Consumer: Instrument Cluster
- Communication: UDP
- Service ID: 0x1234
- Instance ID: 0x5678
- Method: GetSpeed (0x0001)
- Event: SpeedChanged (0x8001)
- Event Group: 0x0001
- Event notification period: 2 seconds

## Experiments and Observations

1. Service Discovery:
   Consumer successfully discovered the provider.

2. Method Communication:
   Consumer successfully requested vehicle speed using GetSpeed
   and received the response.

3. Event Communication:
   Consumer successfully received periodic SpeedChanged events.

4. Consumer Before Provider:
   Consumer waited for the service and discovered it after
   the provider started.

5. Provider Failure:
   Event notifications stopped when the provider was stopped.

6. Provider Restart:
   Communication resumed after restarting the provider.

7. Event Period Modification:
   Event notification interval was changed from 2 seconds
   to 1 second and then restored to 2 seconds.

8. Wireshark Analysis:
   SOME/IP and SOME/IP-SD traffic was captured on the loopback
   interface using Wireshark.

## Conclusion
The implementation successfully demonstrated SOME/IP service
discovery, request-response communication, and event-based
communication between virtual automotive ECUs.
