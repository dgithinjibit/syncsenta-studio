# SyncSenta Repository Collection

This folder contains all the external repositories that contribute to the SyncSenta Education OS ecosystem.

## Repository Organization

### 🎯 Core Infrastructure
- `candle/` - Rust ML framework for AI inference
- `thrml/` - Probabilistic graphical models for adaptive learning

### 🤖 AI & Content Generation  
- `ChatDev/` - Multi-agent platform for automated content creation
- `igbo-bilingual-chat/` - Multilingual AI model template
- `aditicha/` - Critical thinking activities generator

### 🌍 Localization & Translation
- `LughaBridge/` - Real-time voice translation (Kikuyu ↔ English)

### 📚 Educational Content
- `WisdomEdu/` - Live LMS foundation and adaptive engine
- `scheme-genie/` - CBC curriculum generator
- `scheme-scribe-ai/` - AI-powered educational content writer

### 🛡️ Security & Development
- `hexstrike-ai/` - Cybersecurity testing platform
- `best-of-ml-rust/` - Curated Rust ML libraries

### 🌍 Policy & Governance
- `africaAIPolicyResources/` - African AI policy research

### 🔧 Development Tools
- `Syncsenta_local/` - Local development utilities
- `powers/` - Kiro power extensions

## Integration Strategy

Each repository serves a specific purpose in the SyncSenta ecosystem:

1. **Core SyncSenta** (root folder) - Main education platform
2. **AI Infrastructure** - Candle + THRML for ML capabilities  
3. **Content Generation** - ChatDev + Scheme tools for curriculum
4. **Localization** - LughaBridge for multilingual support
5. **Security** - HexStrike for platform protection
6. **Research** - Policy resources for compliance

## Usage

To work with any repository:

```bash
cd repos/[repository-name]
# Follow that repository's setup instructions
```

To integrate with main SyncSenta:

```bash
# From project root
cargo build  # For Rust components
npm run build  # For frontend components
```