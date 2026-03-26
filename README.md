# AREA - Automation Platform

Action-REAction Automation Platform (such as IFTTT/Zapier)

AREA is a software suite that allows users to create automations by connecting various services together. Based on the Trigger (Action) and Consequence (REAction) logic, the platform allows you to automate your digital life via a Web and Mobile interface.

---

## 🏗 Architecture

The project is divided into three main microservices orchestrated via Docker Compose:

- Server (Backend): REST API built with FastAPI (Python) & PostgreSQL. Handles business logic, OAuth2 authentication, and trigger execution.
- Web Client: Frontend interface built with React (Vite).
- Mobile Client: Native mobile application built with Flutter(Android).

---

## 🚀 Features

- User Management: Registration, Login, OAuth2 Login (Google, Discord, GitHub, Microsoft).
- Cross-Platform: Available on Web (Desktop/Mobile) and Android.
- AREA Creation: Visual interface to link a Trigger to a Reaction.
- Dynamic Forms: Input fields automatically adapt based on the arguments required by the selected service.
- Scheduler: Automations are checked and executed in real-time or via polling.
- APK Download: Automatic generation and hosting of the Android client.

---

## 🔌 Supported Services

The platform currently supports the following services:

| Service | Actions (Triggers) | Reactions |
| :--- | :--- | :--- |
| **Google** (Gmail, Drive) | New Email, New File | Send Email, Create Text File |
| **Microsoft** (Outlook, OneDrive) | New Email | Send Email, Create File |
| **Discord** | New Message | Post a Message |
| **GitHub** | New Push/Commit | (None) |
| **GitLab** | New Issue | Create an Issue |
| **Trello** | New Card in List | Create a Card |
| **Slack** | New Message in Channel | Post a Message |
| **Spotify** | New Liked Track | Add Track to Playlist |
| **Dropbox** | File Added | Create Text File |
| **OpenWeather** | Temperature Change, Weather Condition | (None) |
| **Timer** | Every Minute/Hour/Day, Custom Interval | (None) |

---

## 🛠 Installation & Setup

### Prerequisites

* **Docker** & **Docker Compose** (Latest version recommended)
* **Git**

### 1. Clone the repository

```bash
git clone git@github.com:EpitechPGE3-2025/G-DEV-500-PAR-5-2-area-6.git area
cd area
```

### 2. Environment Variables (.env)

Create a .env file at the root (or configure your backend environments). You must provide your own API keys for the services to work.

```
# Database
POSTGRES_USER=area
POSTGRES_PASSWORD=area
POSTGRES_DB=area
DATABASE_URL=postgresql://area:area@db:5432/area

# Security
SECRET_KEY=change_this_to_a_secure_random_string

# OAuth2 & API Keys (Required for services)
GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret

DISCORD_CLIENT_ID=your_discord_id
DISCORD_CLIENT_SECRET=your_discord_secret
DISCORD_BOT_TOKEN=your_discord_bot_token

GITHUB_CLIENT_ID=your_github_id
GITHUB_CLIENT_SECRET=your_github_secret

MICROSOFT_CLIENT_ID=your_microsoft_id
MICROSOFT_CLIENT_SECRET=your_microsoft_secret

OPENWEATHER_API_KEY=your_openweather_key

# Add other keys as needed (Spotify, Trello, etc.)
```

### 3. Launch the project

Use Docker Compose to build and start all containers.

```Bash

docker-compose up --build
```

> Note: The first build may take a few minutes, especially for the Mobile container which generates the APK.

## 💻 Usage

Once the containers are running:

#### Web Client
 
Access the web dashboard: http://localhost:8081

#### Mobile Client (Android)

Download the latest generated APK directly from the web client: http://localhost:8081/client.apk

(Installation: Download the file to your Android phone, authorize installation from unknown sources, and install).

#### Backend API / Documentation

API Root: http://localhost:8080

Swagger/OpenAPI Documentation: http://localhost:8080/docs

About.json: http://localhost:8080/about.json

## 👥 Authors

This project was built by:

- [Zoltan BABKO](https://github.com/zoltanbabko)
- [Alexandre ODRIOSOLO](https://github.com/alpharone)

## 🤝 Contributing

Contributions are welcome! Please check the [HOWTOCONTRIBUTE.md](./HOWTOCONTRIBUTE.md) file to learn how to add new services, actions, or reactions to the platform.

## 📜 License

This project is intended for educational purposes as part of the Epitech studies.