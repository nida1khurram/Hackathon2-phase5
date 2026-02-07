# Phase 5: Claude Agent Execution Guide

## Overview
This guide explains how to use Claude agents to execute the Phase 5 implementation plan.

## Agent Activation Sequence

### 1. Start with the DevOps Agent
Activate `@agents/devops-agent.md` to orchestrate the entire Phase 5 process:

```
@agents/devops-agent.md

Follow the Phase IV Orchestration Workflow (which extends to Phase V):
1. Coordinate with specialized agents
2. Document all AI interactions in PHRs
3. Ensure quality checklist completion
```

### 2. Activate the Docker Agent
Use `@agents/docker-agent.md` to handle containerization with Dapr integration:

```
@agents/docker-agent.md

Focus on:
- Generate Dockerfiles with Dapr sidecar support
- Optimize images for Dapr-enabled deployments
- Add health check endpoints compatible with Dapr
- Ensure security best practices with non-root users
```

### 3. Activate the Helm Agent
Use `@agents/helm-agent.md` to create Dapr-aware Helm charts:

```
@agents/helm-agent.md

Focus on:
- Generate Helm charts with Dapr annotations
- Create templates for pub/sub, state management
- Configure secrets for Kafka/Redpanda connection
- Set up service invocation patterns
```

### 4. Activate the Kubernetes Agent
Use `@agents/kubernetes-agent.md` for deployment:

```
@agents/kubernetes-agent.md

Focus on:
- Deploy to Minikube with Dapr
- Configure health checks for Dapr sidecars
- Troubleshoot Dapr-related issues
- Implement rolling updates for Dapr-enabled apps
```

## Skill Invocation Examples

### For Advanced Features Implementation:
```
@skills/advanced-todo-features.md

Input: Implement recurring tasks with due dates and reminders
Output: Complete Task model with recurrence patterns and reminder logic
```

```
@skills/intermediate-todo-features.md

Input: Add priority, tags, search, filter, and sort capabilities
Output: Enhanced API endpoints and database schema
```

### For Kafka Integration:
```
@skills/event_driven_architecture_with_kafka.md

Input: Design event-driven architecture for task notifications
Output: Kafka producer/consumer implementations for task events
```

```
@skills/redpanda_cloud_kafka_setup.md

Input: Configure connection to Redpanda Cloud for production
Output: Connection parameters and security configuration
```

### For Dapr Implementation:
```
@skills/dapr_implementation.md

Input: Design Dapr components for pub/sub, state, bindings, secrets, service invocation
Output: Complete Dapr configuration files and application integration code
```

### For Cloud Deployment:
```
@skills/cloud_kubernetes_deployment.md

Input: Deploy to DigitalOcean Kubernetes with Dapr and Redpanda
Output: Terraform/IaC files and deployment scripts
```

### For CI/CD Pipeline:
```
@skills/ci_cd_pipeline_github_actions.md

Input: Create pipeline for automated deployment with Dapr awareness
Output: GitHub Actions workflow files
```

## Execution Workflow

### Phase 1: Feature Development
1. Activate `@agents/fastapi-backend-agent.md` to implement backend features
2. Use `@skills/advanced-todo-features.md` for recurring tasks
3. Use `@skills/intermediate-todo-features.md` for priorities/tags/search
4. Use `@skills/sqlmodel_schema_design.md` for database schema updates
5. Document progress in PHR

### Phase 2: Event Architecture
1. Activate `@agents/docker-agent.md` to containerize with Kafka clients
2. Use `@skills/event_driven_architecture_with_kafka.md` for event design
3. Use `@skills/redpanda_cloud_kafka_setup.md` for cloud connection
4. Test locally with Docker Compose
5. Document in PHR

### Phase 3: Dapr Integration
1. Use `@skills/dapr_implementation.md` to design Dapr components
2. Update Dockerfiles with Dapr sidecar support
3. Update Helm charts with Dapr annotations
4. Test Dapr functionality locally
5. Document in PHR

### Phase 4: Local Deployment
1. Activate `@agents/kubernetes-agent.md` for Minikube deployment
2. Use `@skills/minikube_deployment.md` for setup
3. Deploy with Dapr and Kafka integration
4. Verify all functionality
5. Document in PHR

### Phase 5: Cloud Preparation
1. Use `@skills/cloud_kubernetes_deployment.md` for cloud setup
2. Prepare infrastructure as code
3. Configure for production security
4. Document in PHR

### Phase 6: Pipeline Creation
1. Use `@skills/ci_cd_pipeline_github_actions.md` for pipeline
2. Add monitoring with `@skills/monitoring_logging_configuration.md`
3. Test pipeline end-to-end
4. Document in PHR

## Quality Assurance with Agents

### Using kubectl-ai (via @skills/kubectl-ai-wrapper.md):
```
kubectl-ai "deploy taskflow backend with dapr annotation"
kubectl-ai "scale backend to 3 replicas with dapr sidecars"
kubectl-ai "show me dapr sidecar status for all pods"
```

### Using kagent for analysis:
```
kagent analyze cluster for dapr deployments
kagent optimize resources for dapr-enabled apps
kagent check security of dapr configuration
```

### Using Gordon (Docker AI) for optimization:
```
docker ai "optimize this dockerfile for dapr integration"
docker ai "reduce image size while keeping dapr functionality"
```

## PHR Documentation Requirements

For each agent interaction, create PHRs documenting:

1. **Agent/Skill Used**: Which agent or skill was invoked
2. **Input Provided**: What requirements or parameters were given
3. **Output Generated**: What code/configuration was produced
4. **Verification**: How the output was tested/validated
5. **Issues Encountered**: Any problems and solutions
6. **Next Steps**: What to do with the generated output

### Example PHR Entry:
```
## Agent: @agents/docker-agent.md
**Date**: 2026-02-07
**Task**: Generate Dockerfile with Dapr integration
**Input**: 
- Service: backend
- Requirements: Dapr sidecar, non-root user, health check
**Output**: 
- Generated Dockerfile with dapr run command
- Added dapr CLI installation
- Maintained security best practices
**Verification**: 
- Built successfully
- Ran with dapr sidecar locally
- Health check working
**Next Steps**: 
- Update Helm chart with dapr annotations
- Test in Minikube environment
```

## Success Metrics

The implementation is successful when:

1. ✅ All advanced features (recurring tasks, due dates, reminders) implemented
2. ✅ All intermediate features (priorities, tags, search, filter, sort) implemented  
3. ✅ Kafka integration with Redpanda Cloud working
4. ✅ Dapr implementation with all components (pub/sub, state, bindings, secrets, service invocation)
5. ✅ Successful deployment to Minikube with Dapr
6. ✅ Cloud deployment preparation complete
7. ✅ CI/CD pipeline configured
8. ✅ Monitoring and logging configured
9. ✅ All PHRs properly documented
10. ✅ Code quality meets standards

## Troubleshooting with Agents

When encountering issues:

1. Use `@agents/debugging-agent.md` for systematic troubleshooting
2. Use `@skills/troubleshooting-workflow.md` (if available) for structured approach
3. Consult specific agents for domain expertise:
   - `@agents/kubernetes-agent.md` for deployment issues
   - `@agents/docker-agent.md` for containerization issues
   - `@agents/fastapi-backend-agent.md` for backend issues
   - `@agents/nextjs-frontend-agent.md` for frontend issues

This guide provides a structured approach to using Claude agents and skills to successfully implement Phase 5 of the project.