# Monitoring and Alerting Guide

**Last Updated**: 2025-01-27  
**Version**: 1.0

---

## Overview

This document describes the monitoring and alerting setup for ResearchOps Agent in production. It covers Prometheus metrics, Grafana dashboards, and alerting rules.

---

## Architecture

```
┌─────────────────┐
│  Prometheus     │ ← Scrapes metrics from services
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  AlertManager   │ ← Evaluates alert rules
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Grafana        │ ← Visualization and dashboards
└─────────────────┘
```

---

## Prometheus Metrics

### Available Metrics

The system exposes the following Prometheus metrics:

#### Request Metrics
- `research_ops_requests_total` - Total requests (labels: `status`)
- `research_ops_request_duration_seconds` - Request duration histogram
- `research_ops_active_requests` - Currently active requests (gauge)

#### Agent Metrics
- `research_ops_agent_decisions_total` - Agent decisions (labels: `agent`, `decision_type`)
- `research_ops_papers_analyzed_total` - Papers analyzed (labels: `source`)

#### NIM Metrics
- `research_ops_nim_requests_total` - NIM API requests (labels: `nim_type`, `endpoint`, `status`)
- `research_ops_nim_duration_seconds` - NIM request duration (labels: `nim_type`, `endpoint`)

#### Cache Metrics
- `research_ops_cache_hits_total` - Cache hits (labels: `cache_type`)
- `research_ops_cache_misses_total` - Cache misses (labels: `cache_type`)

#### Quality Metrics
- `research_ops_quality_scores` - Quality score distribution

### Accessing Metrics

```bash
# Metrics endpoint
curl http://agent-orchestrator.research-ops.svc.cluster.local:8080/metrics

# Example output
# HELP research_ops_requests_total Total number of research requests
# TYPE research_ops_requests_total counter
research_ops_requests_total{status="success"} 1234
research_ops_requests_total{status="error"} 45
```

---

## Alerting Rules

### Alert Configuration

```yaml
# k8s/monitoring/alert-rules.yaml
groups:
  - name: research_ops_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(research_ops_requests_total{status="error"}[5m]) /
          rate(research_ops_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
          service: research-ops
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
      
      # High request latency
      - alert: HighRequestLatency
        expr: |
          histogram_quantile(0.95, 
            rate(research_ops_request_duration_seconds_bucket[5m])
          ) > 30
        for: 5m
        labels:
          severity: warning
          service: research-ops
        annotations:
          summary: "High request latency"
          description: "P95 latency is {{ $value }}s (threshold: 30s)"
      
      # Circuit breaker open
      - alert: CircuitBreakerOpen
        expr: |
          research_ops_circuit_breaker_state{state="open"} == 1
        for: 1m
        labels:
          severity: critical
          service: research-ops
        annotations:
          summary: "Circuit breaker is OPEN"
          description: "Circuit breaker {{ $labels.circuit_name }} is open"
      
      # NIM service unavailable
      - alert: NIMServiceUnavailable
        expr: |
          rate(research_ops_nim_requests_total{status="error"}[5m]) >
          rate(research_ops_nim_requests_total[5m]) * 0.1
        for: 5m
        labels:
          severity: critical
          service: research-ops
        annotations:
          summary: "NIM service unavailable"
          description: "NIM {{ $labels.nim_type }} error rate is {{ $value | humanizePercentage }}"
      
      # Low cache hit rate
      - alert: LowCacheHitRate
        expr: |
          rate(research_ops_cache_hits_total[5m]) /
          (rate(research_ops_cache_hits_total[5m]) + 
           rate(research_ops_cache_misses_total[5m])) < 0.5
        for: 10m
        labels:
          severity: warning
          service: research-ops
        annotations:
          summary: "Low cache hit rate"
          description: "Cache hit rate is {{ $value | humanizePercentage }} (threshold: 50%)"
      
      # High active requests
      - alert: HighActiveRequests
        expr: research_ops_active_requests > 100
        for: 5m
        labels:
          severity: warning
          service: research-ops
        annotations:
          summary: "High number of active requests"
          description: "{{ $value }} active requests (threshold: 100)"
      
      # Pod crash loop
      - alert: PodCrashLoop
        expr: |
          kube_pod_container_status_restarts_total > 5
        for: 5m
        labels:
          severity: critical
          service: research-ops
        annotations:
          summary: "Pod in crash loop"
          description: "Pod {{ $labels.pod }} has restarted {{ $value }} times"
      
      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (container_memory_usage_bytes{pod=~"research-ops.*"} /
           container_spec_memory_limit_bytes{pod=~"research-ops.*"}) > 0.9
        for: 5m
        labels:
          severity: warning
          service: research-ops
        annotations:
          summary: "High memory usage"
          description: "Pod {{ $labels.pod }} memory usage is {{ $value | humanizePercentage }}"
      
      # High CPU usage
      - alert: HighCPUUsage
        expr: |
          rate(container_cpu_usage_seconds_total{pod=~"research-ops.*"}[5m]) >
          container_spec_cpu_quota{pod=~"research-ops.*"} * 0.9
        for: 5m
        labels:
          severity: warning
          service: research-ops
        annotations:
          summary: "High CPU usage"
          description: "Pod {{ $labels.pod }} CPU usage is high"
```

### Apply Alert Rules

```bash
# Create ConfigMap with alert rules
kubectl create configmap prometheus-alert-rules \
  --from-file=alert-rules.yaml=k8s/monitoring/alert-rules.yaml \
  -n monitoring

# Update Prometheus to use ConfigMap
# (Configuration depends on your Prometheus setup)
```

---

## Grafana Dashboards

### Dashboard 1: System Overview

**Key Panels**:
- Request rate (requests/sec)
- Error rate (%)
- P50, P95, P99 latency
- Active requests
- Circuit breaker status

**Query Examples**:
```promql
# Request rate
rate(research_ops_requests_total[5m])

# Error rate
rate(research_ops_requests_total{status="error"}[5m]) /
rate(research_ops_requests_total[5m])

# P95 latency
histogram_quantile(0.95, 
  rate(research_ops_request_duration_seconds_bucket[5m])
)
```

### Dashboard 2: Agent Performance

**Key Panels**:
- Decisions per agent
- Papers analyzed over time
- Decision types distribution
- Quality score distribution

**Query Examples**:
```promql
# Decisions by agent
sum by (agent) (rate(research_ops_agent_decisions_total[5m]))

# Papers analyzed
sum by (source) (research_ops_papers_analyzed_total)
```

### Dashboard 3: NIM Performance

**Key Panels**:
- NIM request rate
- NIM error rate
- NIM latency (P95)
- NIM request distribution

**Query Examples**:
```promql
# NIM request rate
sum by (nim_type) (rate(research_ops_nim_requests_total[5m]))

# NIM error rate
rate(research_ops_nim_requests_total{status="error"}[5m]) /
rate(research_ops_nim_requests_total[5m])
```

### Dashboard 4: Cache Performance

**Key Panels**:
- Cache hit rate
- Cache hits/misses over time
- Cache effectiveness by type

**Query Examples**:
```promql
# Cache hit rate
rate(research_ops_cache_hits_total[5m]) /
(rate(research_ops_cache_hits_total[5m]) + 
 rate(research_ops_cache_misses_total[5m]))
```

### Dashboard 5: Infrastructure

**Key Panels**:
- Pod status
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

---

## AlertManager Configuration

### Alert Routing

```yaml
# alertmanager-config.yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'on-call'
    - match:
        severity: warning
      receiver: 'team-slack'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#research-ops-alerts'
        title: 'ResearchOps Alert'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
  
  - name: 'on-call'
    slack_configs:
      - channel: '#research-ops-oncall'
        title: '🚨 CRITICAL: ResearchOps Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
  
  - name: 'team-slack'
    slack_configs:
      - channel: '#research-ops-team'
        title: 'ResearchOps Warning'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

### Apply AlertManager Config

```bash
# Create secret with AlertManager config
kubectl create secret generic alertmanager-config \
  --from-file=alertmanager.yml=alertmanager-config.yaml \
  -n monitoring
```

---

## Log Aggregation

### Structured Logging

Ensure applications log in structured format:

```python
import logging
import json

logger = logging.getLogger(__name__)

# Structured log
logger.info("Research synthesis started", extra={
    "query": query,
    "max_papers": max_papers,
    "user_id": user_id,
    "trace_id": trace_id
})
```

### Log Collection

Recommend using **Fluentd** or **Fluent Bit** for log aggregation:

```yaml
# fluentd-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: research-ops
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*research-ops*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
      </parse>
    </source>
    
    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name research-ops
      type_name _doc
    </match>
```

---

## Observability Best Practices

### 1. Distributed Tracing

Add trace IDs to all requests:

```python
import uuid

trace_id = str(uuid.uuid4())
logger.info("Request started", extra={"trace_id": trace_id})

# Pass trace_id through all service calls
headers = {"X-Trace-ID": trace_id}
```

### 2. Health Checks

Implement comprehensive health checks:

```python
@app.get("/health")
async def health():
    checks = {
        "reasoning_nim": await check_nim_health("reasoning"),
        "embedding_nim": await check_nim_health("embedding"),
        "qdrant": await check_qdrant_health(),
        "redis": await check_redis_health()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks
    }, status_code
```

### 3. Performance Profiling

Use metrics to identify bottlenecks:

```python
with metrics.request_duration.time():
    # Operation to measure
    result = await expensive_operation()
```

---

## Monitoring Checklist

- [ ] Prometheus installed and scraping metrics
- [ ] Alert rules configured and tested
- [ ] AlertManager configured with notifications
- [ ] Grafana dashboards created
- [ ] Log aggregation configured
- [ ] Health check endpoints implemented
- [ ] Distributed tracing configured (optional)
- [ ] On-call rotation configured
- [ ] Alert runbooks documented

---

## Troubleshooting

### Metrics Not Appearing

```bash
# Check ServiceMonitor
kubectl get servicemonitor -n research-ops

# Check Prometheus targets
curl http://prometheus.monitoring.svc.cluster.local:9090/api/v1/targets

# Check metrics endpoint directly
curl http://agent-orchestrator.research-ops.svc.cluster.local:8080/metrics
```

### Alerts Not Firing

```bash
# Check AlertManager status
curl http://alertmanager.monitoring.svc.cluster.local:9093/api/v2/alerts

# Check alert rules
kubectl get prometheusrule -n monitoring

# Test alert expression
curl -G 'http://prometheus.monitoring.svc.cluster.local:9090/api/v1/query' \
  --data-urlencode 'query=rate(research_ops_requests_total[5m])'
```

---

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)

---

**Next Steps**:
1. Deploy Prometheus and Grafana
2. Configure alert rules
3. Set up notification channels
4. Create dashboards
5. Test alerting end-to-end

