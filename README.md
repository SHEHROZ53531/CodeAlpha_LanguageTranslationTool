# CodeAlpha: Language Translation Tool with Text-to-Speech

A modular AI Language Translation application engineered during the CodeAlpha Artificial Intelligence Internship. This project features a dual-interface architecture: a modern dark-mode desktop GUI built with CustomTkinter and a cloud-ready web application deployed on Hugging Face Spaces using Gradio.

The core translation layer is fully isolated from the presentation views, integrating a translation API alongside layout mechanics to correctly shape and align Right-to-Left (RTL) complex scripts (like Urdu and Arabic) natively on Linux systems.

## ✨ Features
- **Multi-Language Support:** Fluid bidirectional translation across English, Urdu, French, Spanish, Arabic, German, Chinese, and Hindi.
- **Asynchronous Text-to-Speech:** Generates localized spoken audio natively without blocking or freezing the primary user interface threads.
- **Advanced Linux RTL Formatting:** Dynamically restructures, text-aligns, and visually shapes Urdu/Arabic script orientations to bypass standard desktop rendering limitations.
- **One-Click Clipboard Actions:** Instant localized copying mechanism that preserves proper reading orientations.
- **Dual-Deployment Mode:** Runs locally via a sleek desktop container or globally via an optimized browser web application pipeline.

## 🛠️ System Architecture & Files
- `translator_engine.py` - Core translation layer wrapping the underlying API interfaces cleanly.
- `config.py` - Language code mappings, data tables, and structural settings.
- `gui.py` - CustomTkinter application container optimized for native Linux execution.
- `app.py` - Production Gradio web UI script serving as the cloud deployment entry point.
- `requirements.txt` - Complete dependency manifest list tracking required packages.

## 🚀 Local Setup Instructions

Ensure you are using a Linux/Ubuntu distribution environment with Python 3 installed.

```bash
# Clone the repository
git clone [https://github.com/YOUR-USERNAME/CodeAlpha_Language_Translation_Tool.git](https://github.com/YOUR-USERNAME/CodeAlpha_Language_Translation_Tool.git)
cd CodeAlpha_Language_Translation_Tool

# Setup isolated runtime environment
python3 -m venv venv
source venv/bin/activate

# Install application dependencies
pip install -r requirements.txt

# Launch Desktop GUI 
python3 gui.py

# Launch Local Web UI
python3 app.py
