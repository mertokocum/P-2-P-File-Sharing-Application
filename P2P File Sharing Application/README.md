
# FILE SHARING APP

MK File Sharing App is uses UDP broadcast and TCP file transfer protocols to share and receive file fragments between devices on the same network.

## Operational Scenarios:
**Chunk Announcer:**
The Chunk Announcer component splits the Image files into several parts and broadcasts the stack information to other devices. Users are requested to enter the path of the file they want to share. The chosen image file is split into five chunks. 

**Chunk Uploader:**
The Chunk Uploader component acts as a server, accepting connections from other devices and sending requested file chunks over TCP.If the requested file chunk is existed, it is sent to the client with TCP connection.If the file is not found, program prints errors.

**Chunk Discovery:**
Chunk Discovery listens for UDP broadcast messages and adds the data it receives to a "content dictionary" text file.

**Chunk Downloader:**
It downloads and merges the "chunk files" mentioned in the "content dictionary" file.

There is a 50mb file size limitation.
The app is programmed only for transferring png files.

## RUN SEQUENCE:
1:Chunk Announcer (by server)

2:Chunk Discovery (by client)

3:Chunk Uploader (by server)

4:Chunk Downloader (by client)
