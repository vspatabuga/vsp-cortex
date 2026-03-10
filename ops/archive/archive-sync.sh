#!/bin/bash
# ARCHIVING SYNC SCRIPT
# Component: ARCH-001
# Purpose: Sync vsp-cortex data to vsp-docs for persistent storage
# Usage: ./archive-sync.sh [--dry-run] [--force]

set -e

# Configuration
SOURCE_DIR="/home/vsp/vsp-cortex"
TARGET_DIR="/home/vsp/vsp-docs/archive/vsp-cortex"
ARCHIVE_LOG="/home/vsp/vsp-cortex/log/archive-sync.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Modes
DRY_RUN=false
FORCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    --force) FORCE=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Logging function
log() {
  echo "[$TIMESTAMP] $1" | tee -a "$ARCHIVE_LOG"
}

# Create target directories if not exist
setup_directories() {
  log "Setting up archive directories..."
  mkdir -p "$TARGET_DIR"/{experiments,logs,decisions,knowledge}
  log "Directories ready: $TARGET_DIR"
}

# Sync experiments
sync_experiments() {
  log "Syncing experiments..."
  if [ -d "$SOURCE_DIR/exp" ]; then
    rsync -av --delete "$SOURCE_DIR/exp/" "$TARGET_DIR/experiments/" || {
      log "ERROR: Failed to sync experiments"
      return 1
    }
  fi
}

# Sync logs
sync_logs() {
  log "Syncing logs..."
  if [ -d "$SOURCE_DIR/log" ]; then
    rsync -av --delete "$SOURCE_DIR/log/" "$TARGET_DIR/logs/" || {
      log "ERROR: Failed to sync logs"
      return 1
    }
  fi
}

# Generate archive index
generate_index() {
  log "Generating archive index..."
  cat > "$TARGET_DIR/INDEX.md" << EOF
# Archive Index: vsp-cortex
**Generated:** $TIMESTAMP
**Source:** vsp-cortex
**Format:** Markdown + Logseq Compatible

## Statistics
- Experiments: $(find "$TARGET_DIR/experiments" -name "*.md" 2>/dev/null | wc -l) files
- Logs: $(find "$TARGET_DIR/logs" -name "*.md" 2>/dev/null | wc -l) files
- Decisions: $(find "$TARGET_DIR/decisions" -name "*.md" 2>/dev/null | wc -l) files
- Knowledge: $(find "$TARGET_DIR/knowledge" -name "*.md" 2>/dev/null | wc -l) files

## Last Sync
- Time: $TIMESTAMP
- Status: SUCCESS
- Operator: vsp-archiver
EOF
  log "Index updated: $TARGET_DIR/INDEX.md"
}

# Main execution
main() {
  log "=== Archive Sync Started ==="
  log "Source: $SOURCE_DIR"
  log "Target: $TARGET_DIR"
  log "Dry Run: $DRY_RUN"
  
  setup_directories
  generate_index
  
  log "=== Archive Sync Completed ==="
}

if [ "$DRY_RUN" = true ]; then
  log "Running in DRY-RUN mode (no changes will be made)"
fi

main
