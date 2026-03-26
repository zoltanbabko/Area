## 📐 Technical Architecture

### 1. Overview (Architecture Diagram)

The system relies on a microservices architecture orchestrated by Docker. All external requests pass through a reverse proxy (Nginx) before reaching the Backend API.

```mermaid
graph TD
    subgraph Clients
        Mobile[📱 Mobile Client Flutter]
        Web[💻 Web Client React]
    end

    subgraph Docker Infrastructure
        Nginx[🌐 Nginx Reverse Proxy]
        API[⚙️ Backend Server FastAPI]
        DB[🗄️ PostgreSQL]
    end

    subgraph "External World"
        Services[☁️ External Services\nGoogle, Discord, GitHub, etc.]
    end

    %% Flow
    Mobile -->|HTTP /80| Nginx
    Web -->|HTTP /80| Nginx
    Nginx -->|Proxy pass /8080| API
    API <-->|SQL| DB
    API <-->|REST API / OAuth2| Services
```

### 2. API Reference

Interactive and complete API documentation (automatically generated via OpenAPI/Swagger) is available once the project is launched.

Local URL: http://localhost:8080/docs

Content: List of routes, data schemas (Pydantic), and live endpoint testing.

### 3. Execution Logic (Sequence Diagram)

The diagram below illustrates the lifecycle of an automation (AREA), from triggering by the Scheduler to the execution of the Reaction.

Flow: Scheduler ➔ Polling ➔ Check Trigger ➔ Execute Reaction

```mermaid
sequenceDiagram
    autonumber
    participant S as Scheduler
    participant DB as Database
    participant E as Engine (Logic)
    participant A as Action (Gmail/etc)
    participant R as Reaction (Discord/etc)

    Note over S: Tâche de fond (Background)

    S->>DB: Récupérer les AREAs actives
    DB-->>S: Liste [Area 1, Area 2...]

    loop Pour chaque AREA
        S->>E: Lancer le traitement
        
        E->>A: Vérifier le Trigger (Check)
        A->>A: Appel API Externe
        
        alt Rien à signaler (Condition Non Remplie)
            A-->>E: Retourne "Vide" (Stop)
        else Trigger Activé !
            A-->>E: Retourne Données (ex: auteur, titre)
            
            Note right of E: Remplacement des variables<br/>(ex: {{titre}})
            
            E->>R: Exécuter la Réaction
            R->>R: Appel API Externe (Action)
            R-->>E: Succès
        end
    end
```
