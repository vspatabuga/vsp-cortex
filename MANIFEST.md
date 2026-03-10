# PROJECT MANIFEST: VSP-CORTEX
**Status:** ACTIVE / DEVELOPMENT
**Version:** 1.0.0
**Owner:** vspatabuga
**Repository:** vsp-cortex

## 1. PROJECT IDENTITY & SYSTEM CONTEXT (C4 Level 1)
- **Vision:** Sistem Pencatatan dan Perencanaan Terpadu Berbasis Logika.
- **Core Purpose:** Bertindak sebagai **Mesin Logika (Logic Engine)** pusat yang memproses alur kerja, data, dan koordinasi antar sistem.
- **Actors:** Operator VSP, Gemini CLI, Copilot CLI.
- **External Systems:**
  - **vsp-vault (GitHub):** Vault pusat untuk penyimpanan rahasia dan kredensial.
  - **vsp-docs:** Media pengarsipan permanen berbasis `.md`, mendukung format Wiki dan Logseq.
  - **GitHub Kanban:** Integrasi manajemen tugas pada setiap repository yang berkaitan.
- **Technical Stack:**
  - Logic Engine: vsp-cortex
  - Archiving: Markdown / Wiki / Logseq
  - Infrastructure: Local Configuration Host & GitHub Cloud

## 2. CONTAINERS & INFRASTRUCTURE (C4 Level 2)
- **vsp-cortex (Logic Container):** Mesin pemrosesan logika dan aturan sistem.
- **vsp-docs (Storage Container):** Penyimpanan data persisten berbasis file Markdown.
- **vsp-vault (Security Container):** GitHub-hosted vault, namun konfigurasinya dikelola di host lokal ini.
- **Kanban Interface:** Integrasi API GitHub untuk sinkronisasi papan tugas (Project Board).
- **Local Host:** Environment tempat konfigurasi aktif dijalankan.

## 3. COMPONENT BREAKDOWN & CAPABILITY MAP (C4 Level 3)
| Component ID | Description (Responsibility) | Status | Branch |
|:---|:---|:---|:---|
| LOGIC-001 | Core Logic Processor - Mesin utama vsp-cortex | Active | main |
| SYNC-001 | Kanban Sync Provider - Integrasi tugas antar repo | In-Progress | main |
| ARCH-001 | Doc Archiver - Pengelola arsip .md di vsp-docs | Active | main |
| SEC-001 | Vault Bridge - Konektor konfigurasi ke vsp-vault | Active | main |

## 4. DEVELOPMENT PHASES & ROADMAP
### Phase 1: Foundation (Logic & Sync)
- [x] Inisialisasi Arsitektur C4 & Manifest
- [ ] Integrasi Sinkronisasi Kanban antar Repository
- [ ] Setup Bridge Konfigurasi Host ke vsp-vault

### Phase 2: Knowledge Integration
- [ ] Automasi Pengarsipan dari Cortex ke vsp-docs
- [ ] Optimasi format Wiki/Logseq untuk interoperabilitas data

### Phase 3: Intelligence Layer
- [ ] Implementasi AI Logic untuk perencanaan otomatis

## 5. ARCHITECTURAL DECISIONS (ADR Reference)
| Date | Decision | Rationale | Status |
|:---|:---|:---|:---|
| 2026-03-10 | C4 Model Implementation | Standarisasi visualisasi sistem agar scalable dan mudah dipahami AI/Operator. | Approved |
| 2026-03-10 | Separated Storage (vsp-docs) | Memisahkan logika (Cortex) dari data (Docs) untuk integritas jangka panjang. | Approved |

## 6. COMPLIANCE & STANDARDS
- **Architecture Standard:** C4 Model (Context, Containers, Components)
- **Data Format:** CommonMark / Logseq Flavored Markdown
- **Sync Policy:** Kanban-driven development

## 7. BRANCHING & SYNC POLICY
- **Main Branch:** Produksi dan Logika Stabil.
- **Feature Branches:** `feature/[component-id]` - Wajib memperbarui status Manifest sebelum integrasi ke main.

---
**Last Updated:** 2026-03-10
**Operator:** Gemini CLI
