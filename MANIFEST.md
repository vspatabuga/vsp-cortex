# PROJECT MANIFEST: VSP-CORTEX
**Status:** ACTIVE / DEVELOPMENT  
**Version:** 2.0.0  
**Owner:** vspatabuga  
**Repository:** vsp-cortex  
**Last Updated:** 2026-03-10T11:10:00Z

## 1. PROJECT IDENTITY & SYSTEM CONTEXT (C4 Level 1)
- **Vision:** Sistem Pencatatan dan Perencanaan Terpadu Berbasis Logika dengan Kapabilitas AI.
- **Core Purpose:** Bertindak sebagai **Mesin Logika (Logic Engine)** pusat yang memproses alur kerja, data, dan koordinasi antar sistem dengan automasi & intelligence.
- **Actors:** Operator VSP, Gemini CLI, Copilot CLI.
- **External Systems:**
  - **vsp-vault (GitHub):** Vault pusat untuk penyimpanan rahasia dan kredensial.
  - **vsp-docs:** Media pengarsipan permanen berbasis `.md`, mendukung format Wiki dan Logseq.
  - **GitHub Kanban:** Integrasi manajemen tugas pada setiap repository yang berkaitan.
- **Technical Stack:**
  - Logic Engine: vsp-cortex (Clojure/ClojureScript base from logseq)
  - Archiving: Markdown / Wiki / Logseq
  - Intelligence: AI Decision Engine + Learning Module
  - Infrastructure: Local Configuration Host & GitHub Cloud

## 2. CONTAINERS & INFRASTRUCTURE (C4 Level 2)
- **vsp-cortex (Logic Container):** Mesin pemrosesan logika, orkestra multi-agent, decision engine.
- **vsp-docs (Storage Container):** Penyimpanan data persisten berbasis file Markdown.
- **vsp-vault (Security Container):** GitHub-hosted vault, konfigurasinya dikelola di host lokal.
- **Kanban Interface:** Integrasi API GitHub untuk sinkronisasi papan tugas.
- **Local Host:** Environment tempat konfigurasi aktif & intelligence layer dijalankan.

## 3. COMPONENT BREAKDOWN & CAPABILITY MAP (C4 Level 3)
| Component ID | Description | Status | Phase |
|:---|:---|:---|:---|
| LOGIC-001 | Core Logic Processor | Active | Phase 1 |
| SYNC-001 | Kanban Sync Provider | In-Progress | Phase 1 |
| ARCH-001 | Doc Archiver | In-Progress | Phase 2 |
| SEC-001 | Vault Bridge | In-Progress | Phase 1 |
| LOGIC-INTEL | Intelligence Layer | In-Progress | Phase 3 |
| AGENT-COORD | Agent Coordination Protocol | Design | Phase 3 |
| DECISION-ENGINE | Automated Decision Engine | Scaffold | Phase 3 |
| LEARN-MODULE | Learning Module | Architecture | Phase 3 |

## 4. DEVELOPMENT PHASES & ROADMAP

### Phase 1: Foundation (Logic & Sync) ✓ IN-PROGRESS
- [x] Inisialisasi Arsitektur C4 & Manifest
- [x] Dokumentasi Kanban Sync Provider (SYNC-001)
- [x] Dokumentasi Vault Bridge (SEC-001)
- [ ] Implementasi sync engine
- [ ] Setup bridge ke vsp-vault
- [ ] Testing sinkronisasi

### Phase 2: Knowledge Integration ✓ IN-PROGRESS
- [x] Dokumentasi Archiving Automation (ARCH-001)
- [x] Script archive-sync.sh
- [x] Dokumentasi Format Optimization
- [ ] Implementasi automation
- [ ] Setup archive directories
- [ ] Testing format interoperability

### Phase 3: Intelligence Layer ✓ IN-PROGRESS
- [x] Dokumentasi Intelligence Layer
- [x] Agent Coordination Protocol spec
- [x] Decision Engine scaffold
- [x] Learning Module architecture
- [ ] Implementasi decision logic
- [ ] Setup agent registry
- [ ] Testing coordination
- [ ] Deploy learning

## 5. ARCHITECTURAL DECISIONS (ADR Reference)
| Date | Decision | Rationale | Status |
|:---|:---|:---|:---|
| 2026-03-10 | C4 Model + AI Logic | Standarisasi & scalability dengan intelligence | Approved |
| 2026-03-10 | Separated Storage | Data integrity & longevity | Approved |
| 2026-03-10 | Multi-Agent Coordination | Optimal resource utilization | Approved |
| 2026-03-10 | Learning-Driven Optimization | Continuous improvement | Approved |

## 6. COMPLIANCE & STANDARDS
- **Architecture:** C4 Model + AI Decision Logic
- **Data Format:** CommonMark / Logseq Markdown
- **Agent Protocol:** vsp-agent-protocol/1.0
- **Security:** Vault-managed credentials + audit trail

## 7. BRANCHING & SYNC POLICY
- **Main Branch:** Produksi Stabil
- **Feature Branches:** `feature/[component-id]`
- **Phase Branches:** `phase/[1|2|3]-feature`

---
**Last Updated:** 2026-03-10T11:10:00Z  
**Operator:** Copilot CLI  
**Version History:** v1.0 → v2.0 (Phase 3 Intelligence Layer added)
