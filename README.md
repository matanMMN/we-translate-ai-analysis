# WeTranslate-AI

## Development Environment Setup

### Backend Services
- FastAPI Application: `localhost:8000`
  - Swagger Documentation: `localhost:8000/docs`
- Monitoring
  - Prometheus: `localhost:9090`
  - Grafana: `localhost:3000`
    - Username: `admin`
    - Password: `pass`
- Database & Cache
  - PostgreSQL: `localhost:5432`
  - Redis: `localhost:6379`
  - RabbitMQ: `localhost:5672`

### Frontend
- React Application: `localhost:3000`

## Running the Frontend Locally

1. Install dependencies:
```bash
npm install
```

2. Build the project:
```bash
npm run build
```

3. Start the development server:
```bash
npm start
```
