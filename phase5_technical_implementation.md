# Phase 5 Technical Implementation Guide

## Overview
This guide provides detailed technical instructions for implementing Phase 5 using the available Claude skills.

## Part A: Advanced Features Implementation

### 1. Implementing Advanced Todo Features

Using `@skills/advanced-todo-features.md`:

#### Recurring Tasks Implementation:
```python
# In backend/src/models/task.py
from datetime import datetime, timedelta
from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional

class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Advanced features
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default="medium", sa_column_kwargs={"server_default": "medium"})
    tags: Optional[str] = None  # Comma-separated tags
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_end_date: Optional[datetime] = None
    
    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next occurrence of a recurring task"""
        if not self.recurrence_pattern:
            return None
            
        if not self.recurrence_end_date or datetime.now() < self.recurrence_end_date:
            # Calculate next occurrence based on pattern
            next_due_date = self._calculate_next_date()
            if next_due_date:
                new_task = Task(
                    title=self.title,
                    description=self.description,
                    user_id=self.user_id,
                    due_date=next_due_date,
                    recurrence_pattern=self.recurrence_pattern,
                    recurrence_end_date=self.recurrence_end_date
                )
                return new_task
        return None
    
    def _calculate_next_date(self) -> Optional[datetime]:
        """Calculate next occurrence date based on pattern"""
        if not self.due_date:
            return None
            
        if self.recurrence_pattern == RecurrencePattern.DAILY:
            return self.due_date + timedelta(days=1)
        elif self.recurrence_pattern == RecurrencePattern.WEEKLY:
            return self.due_date + timedelta(weeks=1)
        elif self.recurrence_pattern == RecurrencePattern.MONTHLY:
            # Simple monthly calculation (same day next month)
            import calendar
            year = self.due_date.year
            month = self.due_date.month + 1
            if month > 12:
                month = 1
                year += 1
            day = min(self.due_date.day, calendar.monthrange(year, month)[1])
            return self.due_date.replace(year=year, month=month, day=day)
        elif self.recurrence_pattern == RecurrencePattern.YEARLY:
            return self.due_date.replace(year=self.due_date.year + 1)
        return None
```

#### Due Dates & Reminders Implementation:
```python
# In backend/src/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional
import asyncio
from backend.src.models.task import Task, RecurrencePattern
from backend.src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from backend.src.services.task_service import TaskService
from backend.src.dependencies import get_current_user
from backend.src.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/tasks/upcoming", response_model=List[TaskResponse])
async def get_upcoming_tasks(
    days_ahead: int = 7,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Get tasks due in the next specified number of days"""
    cutoff_date = datetime.now() + timedelta(days=days_ahead)
    upcoming_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.completed == False,
        Task.due_date != None,
        Task.due_date <= cutoff_date
    ).order_by(Task.due_date).all()
    return upcoming_tasks

@router.get("/tasks/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Get overdue tasks"""
    now = datetime.now()
    overdue_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.completed == False,
        Task.due_date != None,
        Task.due_date < now
    ).order_by(Task.due_date).all()
    return overdue_tasks

# Background task for sending reminders
async def send_reminder_notifications():
    """Send reminder notifications for tasks due soon"""
    # Implementation would connect to notification service
    # Could use Kafka for event-driven notifications
    pass
```

### 2. Intermediate Features Implementation

Using `@skills/intermediate-todo-features.md`:

#### Priority, Tags, Search, Filter, Sort:
```python
# Enhanced Task API endpoints
@router.get("/tasks/search", response_model=List[TaskResponse])
async def search_tasks(
    query: str,
    priority: Optional[str] = None,
    tags: Optional[str] = None,  # Comma-separated
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Search tasks with filters and sorting"""
    query_obj = db.query(Task).filter(Task.user_id == current_user.id)
    
    # Apply search term
    if query:
        query_obj = query_obj.filter(Task.title.contains(query) | 
                                   Task.description.contains(query))
    
    # Apply priority filter
    if priority:
        query_obj = query_obj.filter(Task.priority == priority)
    
    # Apply tags filter
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            query_obj = query_obj.filter(Task.tags.contains(tag.strip()))
    
    # Apply sorting
    if sort_by == "due_date":
        if sort_order == "desc":
            query_obj = query_obj.order_by(Task.due_date.desc())
        else:
            query_obj = query_obj.order_by(Task.due_date.asc())
    elif sort_by == "priority":
        if sort_order == "desc":
            query_obj = query_obj.order_by(Task.priority.desc())
        else:
            query_obj = query_obj.order_by(Task.priority.asc())
    else:  # Default to created_at
        if sort_order == "desc":
            query_obj = query_obj.order_by(Task.created_at.desc())
        else:
            query_obj = query_obj.order_by(Task.created_at.asc())
    
    return query_obj.all()
```

## Part B: Event-Driven Architecture with Kafka

Using `@skills/event_driven_architecture_with_kafka.md` and `@skills/redpanda_cloud_kafka_setup.md`:

### 1. Kafka Producer Implementation:
```python
# backend/src/services/kafka_producer.py
from kafka import KafkaProducer
import json
import os
from typing import Dict, Any
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

class KafkaTaskProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVERS')],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
            sasl_mechanism=os.getenv('KAFKA_SASL_MECHANISM'),
            sasl_plain_username=os.getenv('KAFKA_USERNAME'),
            sasl_plain_password=os.getenv('KAFKA_PASSWORD')
        )
    
    def send_task_event(self, event_type: str, task_data: Dict[str, Any]):
        """Send a task-related event to Kafka"""
        event = {
            'event_type': event_type,
            'timestamp': str(datetime.utcnow()),
            'task_data': task_data
        }
        
        topic = f"task-{event_type}"
        self.producer.send(topic, value=event)
        self.producer.flush()
    
    def close(self):
        self.producer.close()

# Initialize global producer
kafka_producer = KafkaTaskProducer()
```

### 2. Kafka Consumer Implementation:
```python
# backend/src/services/kafka_consumer.py
from kafka import KafkaConsumer
import json
import os
from typing import Callable
import threading
from backend.src.services.task_service import TaskService
from backend.src.database import get_session

class KafkaTaskConsumer:
    def __init__(self, task_service: TaskService):
        self.consumer = KafkaConsumer(
            'task-created', 'task-updated', 'task-deleted',
            bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVERS')],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
            sasl_mechanism=os.getenv('KAFKA_SASL_MECHANISM'),
            sasl_plain_username=os.getenv('KAFKA_USERNAME'),
            sasl_plain_password=os.getenv('KAFKA_PASSWORD'),
            group_id='task-processing-group'
        )
        self.task_service = task_service
    
    def start_consuming(self):
        """Start consuming messages from Kafka"""
        for message in self.consumer:
            event = message.value
            event_type = event.get('event_type')
            
            if event_type == 'created':
                self.handle_task_created(event['task_data'])
            elif event_type == 'updated':
                self.handle_task_updated(event['task_data'])
            elif event_type == 'deleted':
                self.handle_task_deleted(event['task_data'])
    
    def handle_task_created(self, task_data):
        # Process task creation event
        print(f"Processing task creation: {task_data}")
        # Could trigger notifications, analytics, etc.
    
    def handle_task_updated(self, task_data):
        # Process task update event
        print(f"Processing task update: {task_data}")
    
    def handle_task_deleted(self, task_data):
        # Process task deletion event
        print(f"Processing task deletion: {task_data}")

# Start consumer in a separate thread
def start_kafka_consumer(task_service: TaskService):
    consumer = KafkaTaskConsumer(task_service)
    consumer_thread = threading.Thread(target=consumer.start_consuming)
    consumer_thread.daemon = True
    consumer_thread.start()
```

## Part C: Dapr Implementation

Using `@skills/dapr_implementation.md`:

### 1. Dapr Configuration Files:

#### pubsub.yaml (for message broker):
```yaml
# configs/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "{{ .Values.kafka.brokers }}"
  - name: consumerGroup
    value: "taskflow-consumer-group"
  - name: clientID
    value: "taskflow-client"
  - name: clientSecret
    value: "{{ .Values.kafka.clientSecret }}"
```

#### statestore.yaml (for state management):
```yaml
# configs/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "{{ .Values.redis.host }}:{{ .Values.redis.port }}"
  - name: redisPassword
    value: "{{ .Values.redis.password }}"
  - name: actorStateStore
    value: "true"
```

### 2. Dapr Integration in Application:

```python
# backend/src/services/dapr_service.py
import dapr.clients
from dapr.clients import DaprClient
import json
from typing import Dict, Any, Optional

class DaprTaskService:
    def __init__(self):
        self.dapr_client = DaprClient()
    
    def save_task_state(self, task_id: str, task_data: Dict[str, Any]):
        """Save task state using Dapr state store"""
        with self.dapr_client as client:
            client.save_state(
                store_name="statestore",
                key=f"task_{task_id}",
                value=json.dumps(task_data)
            )
    
    def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve task state from Dapr state store"""
        with self.dapr_client as client:
            response = client.get_state(
                store_name="statestore",
                key=f"task_{task_id}"
            )
            if response.data:
                return json.loads(response.data.decode('utf-8'))
        return None
    
    def publish_task_event(self, event_type: str, task_data: Dict[str, Any]):
        """Publish task event using Dapr pub/sub"""
        with self.dapr_client as client:
            client.publish_event(
                pubsub_name="pubsub",
                topic_name=f"task-{event_type}",
                data=json.dumps({
                    'event_type': event_type,
                    'task_data': task_data,
                    'timestamp': str(datetime.utcnow())
                }),
                data_content_type='application/json'
            )
    
    def invoke_reminder_service(self, user_id: str, reminder_data: Dict[str, Any]):
        """Invoke reminder service using Dapr service invocation"""
        with self.dapr_client as client:
            response = client.invoke_method(
                app_id="reminder-service",
                method_name="schedule_reminder",
                data=json.dumps(reminder_data),
                http_verb='POST'
            )
            return response.text()
```

## Part D: Docker Configuration with Dapr

Using `@skills/dockerfile-builder.md`:

### Enhanced Dockerfile for Dapr:
```dockerfile
# backend/Dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM python:3.13-slim AS deps
WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.13-slim AS runner
WORKDIR /app

# Install Dapr CLI
RUN apt-get update && apt-get install -y wget gnupg && \
    wget -qO - https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --uid 1001 --create-home appuser

# Copy dependencies from deps stage
COPY --from=deps --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["dapr", "run", "--app-id", "taskflow-backend", "--app-port", "8000", "--dapr-http-port", "3500", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Part E: Helm Chart with Dapr Annotations

Using `@skills/helm-chart-builder.md`:

### Deployment with Dapr sidecar:
```yaml
# charts/todo-app/templates/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-backend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app.kubernetes.io/component: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  strategy:
    {{- toYaml .Values.backend.strategy | nindent 4 }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: backend
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "taskflow-backend"
        dapr.io/app-port: "8000"
        dapr.io/config: "dapr-config"
        dapr.io/log-level: "info"
        {{- with .Values.backend.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: backend
        {{- with .Values.backend.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.backend.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "todo-app.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.backend.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}-backend
          securityContext:
            {{- toYaml .Values.backend.securityContext | nindent 12 }}
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-app.secretName" . }}
                  key: database_url
            - name: DAPR_HTTP_PORT
              value: "3500"
            - name: DAPR_GRPC_PORT
              value: "50001"
          livenessProbe:
            {{- toYaml .Values.backend.livenessProbe | nindent 12 }}
          readinessProbe:
            {{- toYaml .Values.backend.readinessProbe | nindent 12 }}
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
          {{- with .Values.backend.volumeMounts }}
          volumeMounts:
            {{- toYaml . | nindent 12 }}
          {{- end }}
      {{- with .Values.backend.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## Part F: Minikube Deployment with Dapr

Using `@skills/minikube_deployment.md`:

### 1. Install Dapr on Minikube:
```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | sh

# Initialize Dapr on Minikube
minikube start --cpus=4 --memory=8192
dapr init -k
```

### 2. Deploy Application:
```bash
# Build and load Docker images to Minikube
eval $(minikube -p minikube docker-env)
docker build -t taskflow-backend:latest ./backend
docker build -t taskflow-frontend:latest ./frontend

# Deploy using Helm
helm install todo-app ./charts/todo-app -f local-values.yaml
```

## Part G: Cloud Deployment Preparation

Using `@skills/cloud_kubernetes_deployment.md`:

### 1. Infrastructure as Code (Terraform example):
```hcl
# terraform/doks-cluster.tf (for DigitalOcean)
resource "digitalocean_kubernetes_cluster" "taskflow" {
  name    = "taskflow-doks"
  region  = var.region
  version = var.kubernetes_version

  node_pool {
    name       = "default"
    size       = var.node_size
    auto_scale = true
    min_nodes  = var.min_nodes
    max_nodes  = var.max_nodes
  }
}

# Install Dapr on cluster
resource "kubectl_manifest" "dapr" {
  yaml_body = file("${path.module}/manifests/dapr-system.yaml")
  depends_on = [digitalocean_kubernetes_cluster.taskflow]
}
```

## Part H: CI/CD Pipeline

Using `@skills/ci_cd_pipeline_github_actions.md`:

### GitHub Actions Workflow:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push backend
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        push: true
        tags: ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Build and push frontend
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        push: true
        tags: ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'
    
    - name: Set up Dapr
      run: |
        wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
        dapr status -k
    
    - name: Deploy to Kubernetes
      run: |
        # Update image tags in Helm values
        sed -i "s|tag: latest|tag: ${{ github.sha }}|g" deploy/values-prod.yaml
        
        # Deploy with Helm
        helm upgrade --install todo-app ./charts/todo-app \
          -f deploy/values-prod.yaml \
          --set backend.image.repository=ghcr.io/${{ github.repository }}/backend \
          --set frontend.image.repository=ghcr.io/${{ github.repository }}/frontend
```

## Summary

This implementation guide shows how to use the available Claude skills to accomplish Phase 5 objectives:

1. **Advanced Features**: Using `@skills/advanced-todo-features.md` and `@skills/intermediate-todo-features.md`
2. **Event-Driven Architecture**: Using `@skills/event_driven_architecture_with_kafka.md` and `@skills/redpanda_cloud_kafka_setup.md`
3. **Dapr Implementation**: Using `@skills/dapr_implementation.md`
4. **Containerization**: Using `@skills/dockerfile-builder.md`
5. **Kubernetes Deployment**: Using `@skills/minikube_deployment.md` and `@skills/cloud_kubernetes_deployment.md`
6. **Helm Charts**: Using `@skills/helm-chart-builder.md`
7. **CI/CD Pipeline**: Using `@skills/ci_cd_pipeline_github_actions.md`

Each skill is applied in the appropriate context to build a robust, scalable, and feature-rich todo application with advanced capabilities.