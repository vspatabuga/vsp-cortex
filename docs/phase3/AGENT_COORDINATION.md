# AGENT COORDINATION PROTOCOL
**Phase 3 Component**  
**Status:** Design  
**Last Updated:** 2026-03-10

## Protocol Specification: vsp-agent-protocol/1.0

### Overview
Protokol komunikasi standar untuk orkestrasi multi-agent dalam ekosistem VSP-Cortex.

### Endpoint Registry
```yaml
Channels:
  kanban_sync:
    endpoint: http://localhost:8001/sync
    type: status_streaming
    
  vault_bridge:
    endpoint: http://localhost:8002/vault
    type: secret_retrieval
    
  decision_bus:
    endpoint: http://localhost:8003/decisions
    type: command_queue
    
  archive_sync:
    endpoint: http://localhost:8004/archive
    type: data_sync
```

### Agent Registry
```yaml
Agents:
  copilot_cli:
    id: "copilot-v1"
    capabilities: ["code_execution", "git_operations", "api_calls"]
    status_endpoint: /agents/copilot/status
    max_parallelism: 5
    
  gemini_cli:
    id: "gemini-v1"
    capabilities: ["experimentation", "data_analysis", "ml_tasks"]
    status_endpoint: /agents/gemini/status
    max_parallelism: 3
    
  operator_vsp:
    id: "operator-human"
    capabilities: ["approval", "override", "configuration"]
    status_endpoint: /agents/operator/status
    max_parallelism: 1
```

### Message Queue Priority
```
Critical (P0)  → Immediate execution
High (P1)      → Within 30 seconds
Normal (P2)    → Within 5 minutes
Low (P3)       → Batch processing
```

### Example Communication Flow

#### Task Request
```
Operator → Decision Bus
{
  "type": "task_request",
  "from": "operator",
  "to": "decision_engine",
  "task": {
    "id": "TASK-001",
    "action": "clone_logseq_to_vsp_cortex",
    "priority": "high",
    "dependencies": []
  }
}

Decision Engine → Copilot
{
  "type": "task_assignment",
  "from": "decision_engine",
  "to": "copilot",
  "task": {
    "id": "TASK-001",
    "assigned_to": "copilot",
    "execute_at": "2026-03-10T11:10:00Z"
  }
}

Copilot → Decision Bus
{
  "type": "status_update",
  "from": "copilot",
  "to": "decision_engine",
  "task_id": "TASK-001",
  "status": "executing",
  "progress": 45
}

Copilot → Decision Bus (Complete)
{
  "type": "task_complete",
  "from": "copilot",
  "to": "decision_engine",
  "task_id": "TASK-001",
  "result": "success",
  "output": {
    "files_created": 5,
    "errors": 0,
    "duration_ms": 15000
  }
}
```

### Error Handling
```
Task Failure (3 retries)
         ↓
Conflict Detection (auto-resolve)
         ↓
Escalate to Operator (if unresolvable)
         ↓
Manual Override / Configuration Update
         ↓
Retry or Abort
```

### Implementation Details
- **Transport**: gRPC for low-latency, JSON-RPC for compatibility
- **Serialization**: JSON with schema validation
- **Authentication**: Vault-managed tokens per agent
- **Rate Limiting**: Token bucket per agent per channel
- **Retry Policy**: Exponential backoff 1s → 32s
- **Timeout**: 5 minutes per task
- **Logging**: All messages to archive-sync for audit trail
