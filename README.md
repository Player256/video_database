````markdown
# 📺 YouTube Video Fetcher

This project continuously fetches the latest YouTube videos for a given search query (e.g., "cricket", "latest news"), stores them in a PostgreSQL database, and exposes a paginated API to retrieve them.

---

## 🚀 Features

- Polls YouTube Data API v3 every few seconds (configurable)
- Stores new videos in a PostgreSQL database
- REST API to query latest videos (`GET /videos`)
- Docker Compose setup for local development
- Kubernetes manifests for cluster deployment

---

## 🔧 Requirements

- Docker + Docker Compose  
- Or: Kubernetes (![Minikube Installation Guide](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download))
- A valid **YouTube Data API v3 key**  
  👉 [Get yours here](https://console.developers.google.com/)
- Add YouTube data v3 API and create credentials to obtain the API key.
---

## ⚙️ Environment Variables

Create a `.env` file with:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/youtube_db
YOUTUBE_API_KEYS=your_api_key
SEARCH_QUERY="latest news"
FETCH_INTERVAL=10
````

You can use `.env` for Docker Compose and `k8s/secrets.yaml` + `configMap.yaml` for Kubernetes.

---

## Local Development with Docker Compose

### Start

```bash
docker compose up --build
```

* FastAPI server → `http://localhost:8000`
* API Docs → `http://localhost:8000/docs`
* Video API → `GET /videos`

### Stop

```bash
docker compose down
```

---

## ☸️ Kubernetes Deployment

### 1. Build & Push Docker Image

```bash
docker build -t charizarddocker/youtube-database:latest .
docker push charizarddocker/youtube-database:latest
```

> Replace `charizarddocker` with your Docker Hub username.

### 2. Apply Kubernetes Resources

```bash
kubectl apply -f k8s/
```

This will deploy:

* PostgreSQL database
* FastAPI server with YouTube poller
* Services and volumes

### 3. Port Forward to Access API

```bash
kubectl port-forward service/youtube-service 8000:80
```

Then open:

```
http://localhost:8000/docs
```

---

## API Example

### `GET /videos`

```
GET http://localhost:8000/videos?skip=0&limit=10
```

Response:

```json
[
  {
    "video_id": "abc123",
    "title": "Live Match Highlights",
    "description": "Today’s match...",
    "published_at": "2025-08-07T10:12:00Z",
    "thumbnail_url": "https://youtube.com/vi/..."
  }
]
```

---




