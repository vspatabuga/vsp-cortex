# knowledge-orchestrator-management

## Overview
Sistem orchestrasi pengetahuan AI (sebelumnya `vsp-cortex`) yang mengatur pipeline vector database, retrievers, dan agent flows. Repo ini hanya menyimpan Data Plane (wrapper Python/Go) dan mengandalkan dokumentasi di [pes-docs/projects/ai-governance-orchestrator](https://github.com/vspatabuga/pes-docs/tree/main/projects/ai-governance-orchestrator).

## Tech Stack
- **Vector store**: Chroma/FAISS via custom scripts.
- **Orchestration**: Python + shell scripts memanggil agent, LLM, dan scheduler.
- **Security**: Proprietary license + Dependabot scans.

## Getting Started
```bash
git clone git@github.com:vspatabuga/knowledge-orchestrator-management.git
cd knowledge-orchestrator-management
pip install -r requirements.txt
python run_pipeline.py
```

## Docs & Operation
- Perubahan besar dicatat di `pes-docs`.
- Gunakan `scripts/` untuk modul orchestrasi dan `config/` untuk environment.

## Security
- Dependabot memantau `pip` dependencies.
- Secrets (API keys, DB credentials) disimpan di Vault atau `~/.secrets/`.
- Laporkan kerentanan melalui GitHub Issue label `security` atau email `sc@vspatabuga.io`.

## License
Apache License 2.0 © 2026 Virgiawan Sagarmata Patabuga.
