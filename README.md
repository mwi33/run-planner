# 🏁 Run Planner

> *Per scientiam ad celeritatem — Through knowledge to speed.*

**Run Planner** is a data-driven coordination tool for sim-racing engineers and drivers.  
It structures the full testing workflow — from planning and setup tracking to telemetry integration and session analysis — ensuring every lap, file, and change is traceable.

Part of the **Optimised / Sim Dynamics** ecosystem.

---

## 🚦 Overview

Sim racing produces immense amounts of data: setups, telemetry, weather conditions, and driver feedback.  
Run Planner connects these into a single workflow — replacing spreadsheets and scattered notes with a coherent, auditable process that mirrors professional motorsport practice.

**Core capabilities include:**
- **Run Session Management:** Plan, execute, and review testing sessions.  
- **Setup Provenance:** Version and hash every configuration for traceability.  
- **Telemetry Integration:** Link MoTeC i2 Pro, CSV, or custom Python analysis.  
- **Qualitative Feedback:** Record driver feel and environment context.  
- **Comparative Analysis:** Quantify performance deltas between runs.  
- **Reporting:** Generate summaries that link goals, results, and insights.

---

## 🧱 Architecture

Run Planner is a **Python Flask** application with a modular structure:

