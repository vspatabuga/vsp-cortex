#!/bin/bash
# ARCHIVING SYNC SCRIPT - PRODUCTION VERSION
# Component: ARCH-001 Phase 2
# Purpose: Sync vsp-cortex data to vsp-docs for persistent storage
# Usage: ./archive-sync.sh [--dry-run] [--force] [--verbose]

set -euo pipefail

# ============ CONFIGURATION ============
SOURCE_DIR="/home/vsp/vsp-cortex"
TARGET_DIR="/home/vsp/vsp-docs/archive/vsp-cortex"
ARCHIVE_LOG="/home/vsp/vsp-cortex/log/archive-sync.log"
SYNC_STATE="/home/vsp/vsp-cortex/.archive-sync-state.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_START_TIME=$(date +%s)

# Modes & Flags
DRY_RUN=false
FORCE=false
VERBOSE=false
RSYNC_OPTS="-av --delete --checksum"

# Statistics
TOTAL_FILES=0
SYNCED_FILES=0
ERRORS=0

# ============ FUNCTIONS ============

# Enhanced logging with levels
log() {
  local level=$1
  shift
  local message="$@"
  echo "[${TIMESTAMP}] [${level}] ${message}" | tee -a "$ARCHIVE_LOG"
}

# Verbose logging (only if --verbose)
vlog() {
  if [ "$VERBOSE" = true ]; then
    log "DEBUG" "$@"
  fi
}

# Error handler
error_exit() {
  log "ERROR" "$1"
  ((ERRORS++))
  if [ "${2:-false}" = "fatal" ]; then
    exit 1
  fi
}

# Parse command line arguments
parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --dry-run)
        DRY_RUN=true
        RSYNC_OPTS="${RSYNC_OPTS} --dry-run"
        log "INFO" "DRY-RUN mode enabled"
        shift
        ;;
      --force)
        FORCE=true
        log "INFO" "FORCE mode enabled (will overwrite)"
        shift
        ;;
      --verbose)
        VERBOSE=true
        shift
        ;;
      *)
        error_exit "Unknown option: $1" "fatal"
        ;;
    esac
  done
}

# Create and setup target directories
setup_directories() {
  log "INFO" "Setting up archive directories..."
  
  local dirs=(
    "$TARGET_DIR"
    "$TARGET_DIR/experiments"
    "$TARGET_DIR/logs"
    "$TARGET_DIR/decisions"
    "$TARGET_DIR/knowledge"
  )
  
  for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
      vlog "Directory exists: $dir"
    else
      mkdir -p "$dir" || error_exit "Failed to create: $dir"
      vlog "Created directory: $dir"
    fi
  done
  
  log "INFO" "Archive directories ready"
}

# Sync documentation files (architecture decisions)
sync_docs() {
  log "INFO" "Syncing documentation files..."
  
  if [ -d "$SOURCE_DIR/docs" ]; then
    local doc_count=$(find "$SOURCE_DIR/docs" -name "*.md" | wc -l)
    vlog "Found $doc_count documentation files"
    
    if [ $DRY_RUN = false ]; then
      mkdir -p "$TARGET_DIR/decisions"
      find "$SOURCE_DIR/docs" -name "*.md" -type f | while read -r file; do
        cp "$file" "$TARGET_DIR/decisions/$(basename "$file")" || error_exit "Failed to copy: $file"
        ((SYNCED_FILES++))
      done
    else
      SYNCED_FILES=$doc_count
    fi
  fi
}

# Sync experiments
sync_experiments() {
  log "INFO" "Syncing experiments from /exp..."
  
  if [ -d "$SOURCE_DIR/exp" ]; then
    local exp_count=$(find "$SOURCE_DIR/exp" -type f | wc -l)
    vlog "Found $exp_count experiment files"
    
    if [ $DRY_RUN = false ]; then
      rsync $RSYNC_OPTS "$SOURCE_DIR/exp/" "$TARGET_DIR/experiments/" || error_exit "Failed to sync experiments"
    fi
    SYNCED_FILES=$((SYNCED_FILES + exp_count))
  fi
}

# Sync logs
sync_logs() {
  log "INFO" "Syncing logs from /log..."
  
  if [ -d "$SOURCE_DIR/log" ]; then
    local log_count=$(find "$SOURCE_DIR/log" -type f | wc -l)
    vlog "Found $log_count log files"
    
    if [ $DRY_RUN = false ]; then
      rsync $RSYNC_OPTS "$SOURCE_DIR/log/" "$TARGET_DIR/logs/" || error_exit "Failed to sync logs"
    fi
    SYNCED_FILES=$((SYNCED_FILES + log_count))
  fi
}

# Sync MANIFEST.md and key docs
sync_manifest() {
  log "INFO" "Syncing MANIFEST.md and key documentation..."
  
  local key_files=(
    "$SOURCE_DIR/MANIFEST.md"
    "$SOURCE_DIR/README.md"
    "$SOURCE_DIR/CONTRIBUTING.md"
  )
  
  if [ $DRY_RUN = false ]; then
    mkdir -p "$TARGET_DIR/knowledge"
    for file in "${key_files[@]}"; do
      if [ -f "$file" ]; then
        cp "$file" "$TARGET_DIR/knowledge/$(basename "$file")" || error_exit "Failed to copy: $file"
        ((SYNCED_FILES++))
        vlog "Synced: $(basename "$file")"
      fi
    done
  fi
}

# Generate comprehensive archive index
generate_index() {
  log "INFO" "Generating archive index..."
  
  local exec_time=$(($(date +%s) - SCRIPT_START_TIME))
  local exp_count=$(find "$TARGET_DIR/experiments" -type f 2>/dev/null | wc -l)
  local log_count=$(find "$TARGET_DIR/logs" -type f 2>/dev/null | wc -l)
  local dec_count=$(find "$TARGET_DIR/decisions" -type f 2>/dev/null | wc -l)
  local know_count=$(find "$TARGET_DIR/knowledge" -type f 2>/dev/null | wc -l)
  
  cat > "$TARGET_DIR/INDEX.md" << EOF
# Archive Index: vsp-cortex
**Generated:** $TIMESTAMP
**Execution Time:** ${exec_time}s
**Source:** vsp-cortex (Production Sync)
**Format:** Markdown + Logseq Compatible

## Archive Statistics
- Experiments: $exp_count files
- Logs: $log_count files
- Decisions/ADR: $dec_count files
- Knowledge: $know_count files
- **Total:** $((exp_count + log_count + dec_count + know_count)) files

## Sync Metadata
- Sync Mode: $([ "$DRY_RUN" = true ] && echo "DRY-RUN" || echo "LIVE")
- Files Synced: $SYNCED_FILES
- Errors: $ERRORS
- Operator: $(whoami)
- Timestamp: $TIMESTAMP

## Contents

### Experiments (/experiments)
Contains AI experimentation logs and sandbox results from Gemini/Copilot agents.

### Logs (/logs)
Operational logs from vsp-cortex execution, decision-making, and system events.

### Decisions (/decisions)
Architectural Decision Records (ADR) and manifesto documentation from Phase 1-3.

### Knowledge (/knowledge)
Core project documentation: MANIFEST.md, README.md, CONTRIBUTING.md

---
**Last Updated:** $TIMESTAMP  
**Next Sync:** Automated daily (via CI/CD) or manual
EOF
  
  log "INFO" "Index generated: $TARGET_DIR/INDEX.md"
}

# Save sync state for audit trail
save_sync_state() {
  log "INFO" "Saving sync state..."
  
  cat > "$SYNC_STATE" << EOF
{
  "last_sync": "$TIMESTAMP",
  "mode": "$([ "$DRY_RUN" = true ] && echo "dry-run" || echo "live")",
  "files_synced": $SYNCED_FILES,
  "errors": $ERRORS,
  "target": "$TARGET_DIR",
  "execution_time_seconds": $(($(date +%s) - SCRIPT_START_TIME))
}
EOF
  
  vlog "State saved to: $SYNC_STATE"
}

# Verification
verify_sync() {
  log "INFO" "Verifying sync integrity..."
  
  if [ ! -d "$TARGET_DIR" ]; then
    error_exit "Target directory doesn't exist: $TARGET_DIR" "fatal"
  fi
  
  local target_count=$(find "$TARGET_DIR" -type f 2>/dev/null | wc -l)
  log "INFO" "Target has $target_count files"
  
  if [ $target_count -gt 0 ]; then
    log "INFO" "✓ Sync verification successful"
  else
    error_exit "No files in target directory" "fatal"
  fi
}

# ============ MAIN EXECUTION ============

main() {
  log "INFO" "=== Archive Sync v1.0 Started ==="
  log "INFO" "Source: $SOURCE_DIR"
  log "INFO" "Target: $TARGET_DIR"
  log "INFO" "Timestamp: $TIMESTAMP"
  
  parse_arguments "$@"
  
  if [ "$DRY_RUN" = true ]; then
    log "WARN" "Running in DRY-RUN mode (no changes will be made)"
  fi
  
  # Execute sync steps
  setup_directories || error_exit "Directory setup failed" "fatal"
  sync_manifest
  sync_docs
  sync_experiments
  sync_logs
  generate_index
  save_sync_state
  verify_sync
  
  # Summary
  log "INFO" "=== Archive Sync Completed ==="
  log "INFO" "Files synced: $SYNCED_FILES"
  log "INFO" "Errors: $ERRORS"
  log "INFO" "Execution time: $(($(date +%s) - SCRIPT_START_TIME))s"
  
  if [ $ERRORS -gt 0 ]; then
    exit 1
  fi
}

# Execute main
main "$@"
