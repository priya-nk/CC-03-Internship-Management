# Internship Management System

A simple **microservices-based Internship Management System** built using **FastAPI, SQLite, Docker, and Docker Compose**.

The project is divided into three independent services. Each service has its own application, Docker image, and SQLite database.

## Services

| Service             | Purpose                        | Port |
| ------------------- | ------------------------------ | ---: |
| Authentication Service     | Authenticate student information     | 8001 |
| Student Service     | Manage student information     | 8002 |
| Internship Service  | Manage internship details      | 8003 |
| Application Service | Manage internship applications | 8004 |

Each service runs independently in its own Docker container.

## Architecture

<img width="983" height="282" alt="image" src="https://github.com/user-attachments/assets/153aa257-9eef-41d2-970c-05177abecfe3" />



## Project Structure

```text
CC-03-Internship-Management/
├── application-service/
│   ├── __pycache__/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── authentication-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── internship-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── student-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── .env
├── docker-compose.yml
├── authentication_locustfile.py
├── application_locustfile.py
├── student_locustfile.py
├── internship_locustfile.py
└── README.md

```

## Technologies Used

* **Language & Framework:** Python, FastAPI, Pydantic, SQLAlchemy
* **Database & Persistence:** SQLite, Docker Named Volumes
* **Containerization & Orchestration:** Docker, Docker Compose
* **Version Control & Registry:** Git, GitHub, Docker Hub
* **Workload Testing:** Locust

---

## Prerequisites

Ensure the following tools are installed on your host system:
* Git
* Docker Desktop

### Verify Installations

```bash
git --version
docker --version
docker compose version
```

---

## Checkpoint 1: Design and Develop the Microservices

Each service is an independent FastAPI application with dedicated endpoints and isolated SQLite persistence.

### API Specifications & Interactive Documentation

* **Student Service API:** [http://localhost:8002/docs](http://localhost:8002/docs)
* **Internship Service API:** [http://localhost:8003/docs](http://localhost:8003/docs)
* **Application Service API:** [http://localhost:8004/docs](http://localhost:8004/docs)

### Sample Endpoints & Payloads

#### 1. Register Student (`POST /students`)
```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "department": "CSE",
  "year": 3
}
```

#### 2. Create Internship Listing (`POST /internships`)
```json
{
  "title": "Backend Intern",
  "company": "Example Ltd",
  "location": "Remote",
  "description": "Python backend internship"
}
```

#### 3. Submit Application (`POST /applications`)
```json
{
  "student_id": 1,
  "internship_id": 1
}
```

#### 4. Update Application Status (`PATCH /applications/{id}/status`)
```json
{
  "status": "accepted"
}
```
> **Note:** Allowed statuses are `pending`, `accepted`, and `rejected`.

---

## Checkpoint 2: Containerize and Deploy the Application

Each service contains its own `Dockerfile` and builds into a standalone image.

### Docker Hub Image Repositories
* **Authentication Service:** `soumyasurpur/authentication-service:latest`
* **Student Service:** `ananyaabhat/student-service:latest`
* **Internship Service:** `bhagyashree028/internship-service:v1`
* **Application Service:** `priya721k/application-service:v1`

#### Pull pre-built images from Docker Hub:
```bash
docker pull soumyasurpur/authentication-service:latest
docker pull ananyaabhat/student-service:latest
docker pull bhagyashree028/internship-service:v1
docker pull priya721k/application-service:v1
```

### Deployment via Docker Compose

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd CC-03-Internship-Management
   ```

2. Launch all microservices:
   ```bash
   docker compose up --build -d
   ```

3. Verify running containers:
   ```bash
   docker ps
   ```

---

## Checkpoint 3: Establish and Demonstrate Microservice Communication

Inter-service communication is enabled through a dedicated Docker bridge network created automatically by Docker Compose.

```
 Client Request
       │
       ▼
┌──────────────┐      Internal HTTP       ┌──────────────┐
│ Application  ├─────────────────────────►│   Student    │
│   Service    │  http://student:8000/    │   Service    │
│  (Port 8004) │                          └──────────────┘
│              │      Internal HTTP       ┌──────────────┐
│              ├─────────────────────────►│  Internship  │
│              │ http://internship:8000/  │   Service    │
└──────────────┘                          └──────────────┘
```

* **Service Discovery:** Microservices reference each other using container service names (`http://student:8000` and `http://internship:8000`) instead of hardcoded local IP addresses.
* **End-to-End Flow:** When creating an application via `POST /applications`, the `application-service` validates `student_id` and `internship_id` across the internal network before persisting the entry.

---

## Checkpoint 4: Generate Varying Workloads and Monitor Performance

Load testing is conducted against target service endpoints using **Locust** while concurrently tracking resource consumption via `docker stats`.

### Execution Steps

1. Start the container stack:
   ```bash
   docker compose up -d
   ```

2. Run Locust against the Authentication Service:
   ```bash
   locust -f locustfile.py --host http://localhost:8001
   ```

3. Open [http://localhost:8089](http://localhost:8089) in your browser and execute tests across 5 concurrency levels (1, 2, 4, 8, and 16 concurrent users).

4. Monitor CPU and Memory metrics in real time:
   ```bash
   docker stats
   ```

5. Repeat steps 2 to 4 for
   Student service:
      ```bash
     locust -f locustfile.py --host http://localhost:8002
     ```
   Internship service:
      ```bash
     locust -f locustfile.py --host http://localhost:8003
     ```
      Application Service:
      ```bash
     locust -f locustfile.py --host http://localhost:8004
     ```


### Performance Observation Table - Authentication Service
| Workload Level | Concurrent Requests | Avg Response Time (ms) | Throughput (RPS) | Failed Requests | CPU Utilization (%) | Memory Utilization (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | 1 | 8.02 | 3.3 | 0 | 2.1 | 52.05 |
| **W2** | 2 | 8.95 | 5.9 | 0 | 2.75 | 53.2 |
| **W3** | 4 | 9.07 | 12.3 | 0 | 4.0 | 54.5 |
| **W4** | 8 | 9.1 | 26 | 0 | 9.56 | 54.5 |
| **W5** | 16 | 10.49 | 50 | 0 | 10.0 | 55.7 |


### Performance Observation Table - Student Service

| Workload Level | Concurrent Requests | Avg Response Time (ms) | Throughput (RPS) | Failed Requests | CPU Utilization (%) | Memory Utilization (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | 1 | 10.53 | 3.1 | 0 | 1 | 55.2 |
| **W2** | 2 | 10.45 | 5.8 | 0 | 2.60 | 55.48 |
| **W3** | 4 | 10.27 | 12.4 | 0 | 5.14 | 55.14 |
| **W4** | 8 | 10.19 | 25.6 | 0 | 3.93 | 55.14 |
| **W5** | 16 | 10.4 | 50.6 | 0 | 3.93 | 55.14 |


### Performance Observation Table - Internship Service

| Workload Level | Concurrent Requests | Avg Response Time (ms) | Throughput (RPS) | Failed Requests | CPU Utilization (%) | Memory Utilization (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | 1 | 9.25 | 3.1 | 0 | 1.70 | 53.95 |
| **W2** | 2 | 8.96 | 6.4 | 0 | 2.55 | 54.29 |
| **W3** | 4 | 9.4 | 13.6 | 0 | 5.54 | 54.48 |
| **W4** | 8 | 11.23 | 26.4 | 0 | 10.87 | 55.46 |
| **W5** | 16 | 11.74 | 50.8 | 0 | 19.20 | 56.14 |


### Performance Observation Table - Application Service

| Workload Level | Concurrent Requests | Avg Response Time (ms) | Throughput (RPS) | Failed Requests | CPU Utilization (%) | Memory Utilization (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W1** | 1 | 7.98 | 3 | 0 | 2.10 | 53.17 |
| **W2** | 2 | 8.95 | 6.9 | 0 | 2.98 | 53.9 |
| **W3** | 4 | 9.15 | 11.6 | 0 | 4.94 | 55.03 |
| **W4** | 8 | 9.41 | 25.7 | 0 | 11.11 | 54.98 |
| **W5** | 16 | 10.51 | 50.4 | 0 | 16.31 | 54.16 |

---

## Graphs:
### Concurrent requests vs Average Response Time
<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/cac14af2-0a10-42c0-b0fd-27ca4f8ad4b5" />

### Concurrent requests vs Throughput
<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/0ebde50d-b0ae-4abf-85ee-a09a0d133f3d" />

### Concurrent requests vs CPU Utilization
<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/827a3d95-a808-4176-baf2-b740a251f362" />

### Concurrent requests vs Memory Utilization
<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/f2d6e345-abed-4220-a5fb-be550823b429" />


## Checkpoint 5: Analyze and Present the Results

### Data Persistence & Volume Management

Each microservice maintains data isolation via dedicated SQLite databases and Docker named volumes:

```
Student Service        ──► students.db     ──► Volume: student_data
Internship Service     ──► internships.db  ──► Volume: internship_data
Application Service    ──► applications.db ──► Volume: application_data
```

### Useful Management Commands

* **View container logs:**
  ```bash
  docker compose logs -f
  ```
* **View logs for a single service:**
  ```bash
  docker compose logs application
  ```
* **Restart container stack:**
  ```bash
  docker compose restart
  ```
* **Stop containers while preserving volume data:**
  ```bash
  docker compose down
  ```
* **Tear down environment and delete database volumes:**
  ```bash
  docker compose down -v
  ```

---
## Key Performance Insights
1. Throughput Scales Linearly with ConcurrencyAs concurrent users increase from 1 (W1) to 16 (W5), throughput increases nearly 17x (from 3 RPS to 50.4 RPS).   This shows that your FastAPI microservice stack and Docker network handle concurrent requests efficiently without hitting a early performance bottleneck.
2. Extremely Low Latency DegradationAverage response time remains virtually flat, increasing by only ~2.5 ms under 16x load (from 7.98 ms at W1 to 10.51 ms at W5).   The asynchronous nature of FastAPI/Uvicorn allows request queuing and execution to stay highly responsive under load.  
3.  Resource Utilization EfficiencyCPU Utilization: Scales predictably with request volume, rising from 2.10% at baseline up to 16.31% at 16 concurrent users.   Memory Utilization: Remains exceptionally stable around ~53–55 MB across all test runs. SQLite in memory/file mode combined with lightweight Python processes keeps the overall container footprint minimal.
4. Zero Failures Across All WorkloadsFailed Requests = 0 across all 5 test levels, demonstrating 100% service availability and stability under load.  



---

## Git Workflow

```bash
git status
git add .
git commit -m "Update microservice stack"
git push origin main
```



