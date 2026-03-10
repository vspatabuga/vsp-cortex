# KANBAN SYNC PROVIDER
**Component ID:** SYNC-001  
**Status:** In-Progress  
**Last Updated:** 2026-03-10

## Objective
Integrasi sinkronisasi Kanban board antar repository untuk koordinasi tugas terpadu antara Copilot CLI, Gemini CLI, dan Operator VSP.

## Architecture

### Connected Repositories
- `copilot-ops`: Operasi Copilot CLI
- `gemini-ops`: Operasi Gemini CLI
- `vsp-cortex`: Logic Engine (hub central)
- `vsp-docs`: Knowledge Storage

### Sync Flow
```
GitHub Project Boards
       ↓
   gh api cli
       ↓
vsp-cortex (SYNC-001 Processor)
       ↓
Local Kanban State (.json)
       ↓
Update Board & Notify Actors
```

## Implementation Steps

### Step 1: Collect Kanban Endpoints
- [ ] copilot-ops: GitHub Project Board ID
- [ ] gemini-ops: GitHub Project Board ID
- [ ] vsp-cortex: GitHub Project Board ID
- [ ] Setup GitHub Personal Access Token (from vsp-vault)

### Step 2: Build Sync Engine
- [ ] Create kanban-sync.js/ts script
- [ ] Implement state tracking (.json)
- [ ] Add cron scheduler for periodic sync

### Step 3: Integration
- [ ] Link to copilot-ops workflow
- [ ] Link to gemini-ops workflow
- [ ] Setup webhook for real-time updates

## Configuration Required
```yaml
github_token: ${VSP_VAULT_GITHUB_TOKEN}
project_boards:
  - repo: copilot-ops
    project_id: XXX
  - repo: gemini-ops
    project_id: XXX
  - repo: vsp-cortex
    project_id: XXX
sync_interval: 300s
```

## Output Format
Local state stored in: `/home/vsp/copilot-ops/tmp/kanban-state.json`
