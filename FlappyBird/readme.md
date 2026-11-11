# Real-Time Multiplayer Flappy Bird

A feature-rich, object-oriented multiplayer Flappy Bird clone developed in Python using **Pygame**. The application features custom low-level TCP socket networking with custom binary message framing, multi-threaded server architecture, persistent cloud authentication using **Firebase Firestore**, and secure password hashing using **Argon2**.

## Key Features

* **Real-Time Multiplayer:** Synchronized game state across multiple concurrent clients via custom socket communication.

* **Low-Level Socket Architecture:** Custom 4-byte length-prefixed packet structure using `struct` and binary serialization via `msgpack` for low-latency network payload transmission.

* **Multi-Threaded Server:** Dynamic client connection and disconnection handling using Python multithreading (`_thread`).

* **Cloud Backend & Security:** User authentication backed by Firebase Firestore with industry-standard password hashing using **Argon2**.

* **Local Persistence & State Management:** Remembers user credentials securely and maintains local game configurations via `SaveFile.json`.

* **Modular Game Engine:** Custom entity management system (`ObjectEntity`, `EntityManager`) supporting collision detection layer systems, dynamic obstacle generation, and frame animations.

## Architecture Overview

```
├── main.py                # Main game loop, rendering context, and UI management
├── Server.py              # Multi-threaded TCP socket server host
├── Network.py             # Client-side network wrapper for socket IO
├── packets.py             # Data packet definition & JSON/Msgpack serialization
├── DatabaseHandler.py     # Firebase Firestore interface & Argon2 hashing
├── entity.py              # Base object entity with custom box collision detection
├── entity_manager.py      # Multi-layered update/draw scheduler for entities
├── BirdObject.py          # Player entity with custom gravity and velocity physics
├── pipe_creation.py       # Dynamic pipe obstacle management & loop handling
├── Button.py              # Custom interactive UI button component
├── TextInputBox.py        # Custom active/inactive text input UI component
├── ScoreManager.py        # High score tracking logic
└── GlobalInfo.py          # Shared configurations (screen bounds, ports, etc.)
```

## Technical Highlights

### 1. Networking & Serialization

* **Protocol:** Built over raw TCP sockets (`socket.AF_INET`, `socket.SOCK_STREAM`).

* **Framing:** Prevents TCP fragmentation and packet stitching by prefixing each message with a 4-byte big-endian unsigned integer length header (`struct.pack('>I', length)`).

* **Serialization:** Uses `msgpack` (MessagePack) for efficient binary serialization instead of standard JSON strings to minimize bandwidth usage.

### 2. Security & Backend Integration

* **Authentication:** Validates user credentials against a remote Google Cloud Firebase Firestore database.

* **Encryption:** Passwords are hashed using the **Argon2id** password hashing algorithm prior to persistence, preventing plain-text data exposure.

* **Credential Protection:** Secrets (`FlappyBird-Secrets.json`) are strictly excluded from version control via `.gitignore`.

## Prerequisites & Installation

### Requirements

* Python 3.9+
* Firebase Project & Service Account Keys (`FlappyBird-Secrets.json`)
* [ngrok](https://ngrok.com/) (required for hosting multiplayer games over the internet without port forwarding)

### Dependencies

Install the required packages using pip:

```bash
pip install pygame firebase-admin argon2-cffi msgpack
```

## Running the Application

### 1. Start the Server

First, start the multiplayer server locally on your machine:

```bash
python Server.py
```

### 2. Tunnel Traffic via ngrok (For Remote/Online Multiplayer)

To allow players outside your local Wi-Fi network to connect to your local server without configuring router port forwarding, open a TCP tunnel using `ngrok`:

```bash
ngrok tcp 4000
```

`ngrok` will provide a dynamic address and port (e.g., `tcp://0.tcp.ngrok.io:12345`). Update `GlobalInfo.py` on client machines with the assigned hostname and port:

```python
class GlobalInfo():
    server = "0.tcp.ngrok.io"  # Host address provided by ngrok
    port = 12345               # Dynamic port assigned by ngrok
```

### 3. Launch Client(s)

Open separate terminal instances and launch the game client:

```bash
python main.py
```

To enable multiplayer, click the **Multiplayer Toggle** on the main menu, type your username/password, and press `Space` when ready!

## AWS Cloud Deployment Alternative

To host `Server.py` on an **AWS EC2** instance instead of local ngrok tunneling:

1. Open inbound TCP traffic for port `4000` in your AWS Security Group.
2. Bind the server address in `GlobalInfo.py` to `"0.0.0.0"`.
3. Update the client IP address in `GlobalInfo.py` to point to your AWS EC2 Public IPv4 Address.