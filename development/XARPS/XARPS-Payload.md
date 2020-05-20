# XARPS Payload Specification

The eXtensible Amateur Radio Payload Specification (XARPS) is data-link layer neutral and
implements >Layer3 services within the packet payload. This specification is inspired
by the experimental [LARPS protocol] (https://github.com/EnhancedRadioDevices/LARPS)

## Payload Fields

| Src | Dest | Options | Type |   Data  | 
| ----| ---- | ------  | ---- | ------- |
|  8  |  8   |   1     |  1   | 19-255  |


**Values in Payload**

Src and Dest are string.  
Options is a binary-packed single-byte integer. Unpacked integer is boolean for each flag. 
Type is a single byte integer
Data is string

## Payload Structure

**Src**

Source callsign/handle with SSID. example (W1FCC50,  PURPLE53)
Any unused values, including empty callsign space, should be designated as 0x00 (NULL).
ASCII
**Dest**

Destination callsign/handle with SSID. example (W1FCC50,  PURPLE53) 
Any unused values, including empty callsign space, should be designated as 0x00 (NULL).

| Special Callsign | Meaning |
| ---------------- | ----- |
| * | Wildcard, a beacon to any station |

**Options**

Option is a one-byte bitmap

| Bit  |     Option         | Description | 
| ---  | ------------------ | -------------- |
| 0-5  |    Reserved        |  |
|  6   |  ACK Response     | Response to ACK Request |
|  7   |   ACK Request     | Used when positive verification is required that a payload was received |

**Type**

Type indicates the payload type. This dictates what is contained in the actual data and how it will be parsed. The types are extensive, so this will be addressed later in the document.

**Data**

Data is a variable length field. It can range from 0 to 235 bytes, depending on the type.

## Payload Types

A variety of payload types are pre-defined with XARPS. Additional types can be added by the community. 

**Payload Type List**

| Value | payload Type               | Description                 |
| ----- | ------------------------- | -----------------------------|
| 0x00  | Reserved                  | Reserved                     |
| 0x01  | Battery                   | Battery voltage update       |
| 0x02  | Time                      | Current time payload         |
| 0x03  | Position Update           | GPS position update          |
| 0x04  | Emergency Alert           | Emergency Alert Message      |
| 0x05  | Weather Update            | Weather station data         |
| 0x06  | Broadcast Message         | Message to all stations      |
| 0x07  | Beacon                    | Propagation beacon           |
| 0x08  | Text Message              | Text message between stations|
| 0x09  | Bulletin                  | News bulletin                |
| 0x0A  | Last Seen Stations        | Digest of recent stations    |
| 0x0B  | Game Session              | Game session                 |
| 0x0C  | Text File Trasnfer        | Text File transfer           |
| 0x0D  | Binary File Transfer      | Binary File transfer         |
| 0x0E  | Streaming                 | Streaming data               |
| 0x0F  | Reserved                  | Reserved                     |
| 0x46  | Gopher                    | Gopher                       |
| 0x50  | HTTP                      | HTTP                         |
| 0x71  | Ident                     | Ident                        |
| 0x77  | NNTP                      | NNTP                         |
| 0x7B  | NTP                       | NTP                          |
| 0xC2  | IRC                       | IRC                          |


**0x00 - Reserved**

Not used

**0x01 - Battery**

This payload type provides battery voltage in ASCII numeric format, which may contain a floating point.

**0x02 - Time**

This payload contains the time in epoch UTC

**0x03 - Position Update**

This message is used to provide position updates, such as GPS locations of any station.

Data format in text:

[time in UTC],[latitude],[longitude],[altitude],[speed],[direction],[station type]

Station types:

| ascii value | station type description |
| ----- | ------------------------ |
| 0     | handheld                 |
| 1     | pedestrian               |
| 2     | car                      |
| 3     | truck                    |
| 4     | van                      |
| 5     | emergency vehicle        |
| 6     | ambulance                |
| 7     | fire truck               |
| 8     | command vehicle          |
| 9     | officer                  |
| 10    | aircraft                 |
| 11    | boat                     |
| 12    | quadcopter UAV           |
| 13    | fixed wing UAV           |
| 14    | balloon                  |
| 15    | float                    |
| 16    | landmark                 |
| 17    | road closed              |
| 18    | accident                 |
| 19    | hazard                   |
| 20    | Perimeter Marker         |
| 21-255 | reserved for future use |

**0x04 - Emergency Alert**

Emergency alerts are free text fields. They should only be utilized in emergencies. They can also be used to announce weather advisories, watches and warnings.

**0x05 - Weather Update**

Weather updates are still in the definition process, but should utilize METAR format

**0x06 - Broadcast Message**

TBD.

**0x07 - Beacon**

Used for propagation beacon payloads. This is a free form text field.

**0x08 - Text Message**

Free text field for text message between stations. 

**0x09 - Bulletin**

Bulletins are free text fields. No advise on formatting at this time. Bulletins can be used (and not limited to) the following:

* Amateur radio items for sale
* Local nets
* Swapmeets
* Club Meetings
* Any other announcements

**0x0A - Last Seen Stations**

Contains a comma delimited list of recently heard stations. 

**0x0B - Game Session**

This payload type is used for a variety of experimental games. Simple turn-based games, drawing applications, and other applications are being evaluated. This payload type will eventually have a structure that will allow discovery of players, start and stop of game sessions, registered games in a game id, as well as free form data fields for the specific application.

**0x0C - Text**

This payload type contains the higher layer protocol which manages reliable text transmission.

**0x0D - Binary**

This payload type contains the higher layer protocol which manages reliable binary file transmissions.

**0x0E - Streaming**

This payload type contains the higher layer protocol which manages reliable streaming transmissions.

**0x0F - Reserved**

Not used
