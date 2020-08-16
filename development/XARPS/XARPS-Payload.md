# XARPS Payload Specification

XARPS stands for eXtensible Amateur Radio Payload Specification. Referencing the Open Systems
Interconnection model (OSI model), XARPS is an application layer protocol with link-level awareness
for use by RF systems providing application level connectivity to other networked systems. 
ASCII (UTF-8) is used throughout the specification

## Payload Fields

| Src | Dest | Options | Type |   Data  | 
| ----| ---- | ------  | ---- | ------- |
|  9  |  9   |   1     |  1   | 21-255  |


* Source and Destination

Each contain callsign/handle with SSID. Field size supports IARU decision for 7 character callsigns.
Field are right justified and padded Example source and destination data include W1FCC50, PURPLE53.
BEACON99 is a reserved word in the destination field for broadcast messages. You can change the SSID
to another number for use in multicast

| BEACON-XX |            Target         |
| --------- | ------------------------- |
|     99    |  ALL stations - Broadcast |
|     89    |  ALL gateways - Multicast |
|     79    |       ALL RAN - Multicast |
|     69    | ALL Local RAN - Multicast |

* Options

| Value |     Option        | Description | 
| ---  | ------------------ | -------------- |
| 0-5  |    Reserved        |  |
|  6   |   ACK Response     | Response to ACK Request |
|  7   |   ACK Request     | Send ACK |

* Data Type

| Value | payload Type               | Description                 |
| ----- | ------------------------- | -----------------------------|
| 0x00  | Reserved                  | Reserved                     |
| 0x01  | Battery                   | Battery voltage update       |
| 0x02  | Time                      | Current time payload         |
| 0x03  | Position Update           | GPS position update          |
| 0x04  | WX Update                 | Emergency Alert Message      |
| 0x05  | Telemetry                 | Telemetry                    |
| 0x06  | Binary File Transfer      | Binary File transfer         |
| 0x07  | Text Message              | Text message between stations|
| 0x08  | APRS                      | APRS Encapsulated            |
| 0x09  | Last Seen Stations        | Digest of recent stations    |
| 0x0A - 0x23   RESERVED                                           |
| 0x0C  | Text File Trasnfer        | Text File transfer           |
| 0x50  | HTTP                      | HTTP                         |
| 0x71  | Ident                     | Ident                        |

** 0x00 - Reserved

Not used

** 0x01 - Battery

This payload type provides battery voltage in ASCII numeric format, which may contain a floating point.

** 0x02 - Time

This payload contains the time in epoch UTC

** 0x03 - Position Update

This message is used to provide position updates, such as GPS locations of any station.

[timestamp],[object-type],[latitude],[longitude],[altitude],[altitude-units]

Station types:

| Value |        Object Type     |
| ----- | ---------------------- |
| 0x00  | Static Land Station    |
| 0x01  | handheld               |
| 0x02  | pedestrian             |
| 0x03  | Civilian Vehicle       |
| 0x04  | Commercial Vehicle     |
| 0x05  | Police Vehicle         |
| 0x06  | Medical Vehicle        |
| 0x07  | Fire Vehicle           |
| 0x08  | Federal Vehicle        |
| 0x09  | Command Vehicle        |
| 0x0A  | Marina                 |
| 0x0B  | Float                  |
| 0x0C  | Swimmer                |
| 0x0D  | Civilian Boat          |
| 0x0E  | Commercial Boat        |
| 0x0F  | Police Boat            |
| 0x10  | Fire Boat              |
| 0x11  | Coast Guard Boat       |
| 0x12  | Command Boat           |
| 0x13  | RESERVED               |
| 0x14  | Perimeter Marker       |
| 0x15  | UAV                    |
| 0x16  | Experimental Manned    |
| 0x17  | Civilian Helicopter    |
| 0x18  | Civilian Fixed Wing    |
| 0x19  | Commercial Fixed Wing  |
| 0x1A  | Police Helicopter      |
| 0x1B  | Medical Helicopter     |

** 0x04 - WX Update

This message is used to provide position updates, such as GPS locations of any station.

[timestamp],[latitude],[longitude],[temperature],[temp-units],[humidity],[barometer],[wind-direction],[wind-speed],[wind-speed-units]

** 0x05 - Telemetry

** 0x06 - Binary Data

** 0x07 - Text Message

** 0x08 - APRS

** 0x09 - Last Seen Stations

** 0x50 - HTTP

** 0x71 - Ident
