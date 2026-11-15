# Vehicle Speed Service Using SOME/IP and Python

## 1. Project Overview

This project demonstrates SOME/IP communication between two virtual
automotive ECUs using Python and the someipy library.

The two ECUs are:
- Vehicle ECU (Provider): Provides vehicle speed information.
- Instrument Cluster (Consumer): Requests speed and receives updates.

## 2. Technologies Used

- Ubuntu Linux
- Python 3.14
- someipy 2.1.2
- SOME/IP and SOME/IP-SD
- UDP communication
- Wireshark

## 3. Service Configuration

| Parameter | Value |
|---|---|
| Service ID | 0x1234 |
| Instance ID | 0x5678 |
| Major Version | 1 |
| Method | GetSpeed (0x0001) |
| Event | SpeedChanged (0x8001) |
| Event Group | 0x0001 |
| Provider Endpoint | 127.0.0.1:3000 |
| Consumer Endpoint | 127.0.0.1:3002 |
| Event Period | 2 seconds |

## 4. Project Structure

- config/: SOME/IP daemon configuration
- src/: Provider, consumer and service configuration
- captures/: Wireshark packet capture
- screenshots/: Execution screenshots

## 5. Execution

Activate the virtual environment:

    source .venv/bin/activate

Start the SOME/IP daemon:

    someipyd --config config/someip_config.json

Start the provider:

    PYTHONPATH=src python src/provider.py

Start the consumer in another terminal:

    PYTHONPATH=src python src/consumer.py

## 6. Demonstrated Features

- Service discovery
- GetSpeed method request and response
- SpeedChanged event notifications
- Consumer started before provider
- Provider stop and restart
- Event notification period modification
- Wireshark packet analysis

## 7. Wireshark Capture

The packet capture is stored in:

    captures/assignment1-someip.pcapng

Display filter:

    udp.port == 30490 || udp.port == 3000 || udp.port == 3002

## 8. Conclusion

The project demonstrates basic SOME/IP service-oriented
communication between virtual automotive ECUs using Python.
Both request-response communication and event-based
communication were successfully tested.
