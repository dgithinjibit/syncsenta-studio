# ChatDev for SyncSenta - Installation Guide

## What You've Built

A comprehensive **ChatDev Power** for holistic multi-agent software development of the SyncSenta Web4 Education OS. This power enables:

- **Multi-agent collaboration** with specialized AI agents (CEO, CTO, Programmers, Testers, AI Safety Engineers)
- **Complete SDLC automation** from requirements to deployment
- **AI safety-first workflows** implementing principles from "Life 3.0", "Mind Children", and "Superintelligence"
- **Web4-native development** with blockchain, IPFS, DID, and DAO governance
- **Ethical AI integration** with UNESCO and AU Continental AI Strategy principles

## Files Created

```
powers/chatdev-syncsenta/
├── POWER.md                                    # Main documentation (27KB)
├── steering/
│   ├── advanced-ai-safety.md                  # AI safety workflows (13KB)
│   └── web4-blockchain-workflows.md           # Web4 & blockchain workflows (18KB)
└── README.md                                   # This file
```

## Installation Steps

### Step 1: Install ChatDev Framework

```bash
# Clone ChatDev repository
git clone https://github.com/OpenBMB/ChatDev.git
cd ChatDev

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Step 2: Install the Power in Kiro

1. **Open Kiro Powers UI**
   - In Kiro, open the command palette (Cmd/Ctrl + Shift + P)
   - Type "Powers" and select "Open Powers Panel"
   - Or use the Powers icon in the sidebar

2. **Add Custom Power**
   - Click "Add Custom Power" button at the top
   - Select "Local Directory" option
   - Provide the full absolute path to this power directory:
     ```
     /home/web4ke/codes/sync/powers/chatdev-syncsenta
     ```
   - Click "Add" to install

3. **Activate the Power**
   - Once installed, the power will appear in your Powers list
   - Click on "ChatDev for SyncSenta" to activate it
   - Review the documentation and available steering files

### Step 3: Configure for SyncSenta

```bash
# Navigate to your SyncSenta workspace
cd /path/to/syncsenta-workspace

# Create ChatDev configuration directory
mkdir -p .chatdev

# Copy agent configurations from the power documentation
# (See POWER.md "Configuration" section for agent and workflow configs)
```

### Step 4: Test the Power

```bash
# Test ChatDev installation
python ChatDev/run.py --help

# Run a simple test task
python ChatDev/run.py \
  --task "Generate a simple React component for SyncSenta" \
  --name "test-component" \
  --org "SyncSenta"
```

## Quick Start Examples

### Example 1: Feature Development

```bash
python ChatDev/run.py \
  --task "Implement blockchain credential minting for SyncSenta" \
  --name "credential-minting" \
  --org "SyncSenta" \
  --config /path/to/syncsenta/.chatdev/agents.json \
  --workflow feature_development
```

### Example 2: AI Safety Feature

```bash
python ChatDev/run.py \
  --task "Implement value alignment system for Mwalimu AI" \
  --workflow ai_feature \
  --safety-mode strict \
  --output ./features/value-alignment
```

### Example 3: Smart Contract Development

```bash
python ChatDev/run.py \
  --task "Create ERC-721 credential contract with revocation" \
  --agents blockchain \
  --network polygon-mumbai \
  --output ./contracts/credentials
```

## Available Steering Files

After activating the power, you can access detailed workflow guides:

1. **advanced-ai-safety.md** - Advanced AI safety workflows
   - Value alignment implementation
   - Consciousness-aware AI design
   - Superintelligence preparedness
   - Ethical guardrails
   - Interpretability & explainability
   - Long-term safety mechanisms

2. **web4-blockchain-workflows.md** - Web4 & blockchain development
   - Smart contract development
   - IPFS integration
   - W3C DID authentication
   - Token economy implementation
   - DAO governance
   - Complete Web4 architecture integration

## Integration with SyncSenta Specs

The power is designed to work directly with your existing SyncSenta specs:

```bash
# Generate implementation from spec
python ChatDev/run.py \
  --spec .kiro/specs/syncsenta-education-os/requirements.md \
  --design .kiro/specs/syncsenta-education-os/design.md \
  --tasks .kiro/specs/syncsenta-education-os/tasks.md \
  --output ./implementation
```

## Key Features

### 1. Multi-Agent Collaboration
- CEO, CTO, Programmers (Frontend, Backend, Blockchain)
- AI Safety Engineer, Tester, Reviewer, Technical Writer
- Specialized agents for Web4, Education, and Ethics

### 2. Complete SDLC Automation
- Requirements → Design → Implementation → Testing → Review → Documentation
- Automated workflows for features, bugfixes, and AI components

### 3. AI Safety-First
- Value alignment mechanisms
- Consciousness-aware design
- Superintelligence preparedness
- Ethical guardrails (UNESCO, AU Continental AI Strategy)
- Interpretability and explainability

### 4. Web4-Native Development
- Blockchain smart contracts (Polygon)
- IPFS decentralized storage
- W3C DID authentication
- DAO governance
- Token economy

### 5. Ethical AI Integration
- Implements principles from "Life 3.0" (Max Tegmark)
- Follows "Mind Children" (Hans Moravec) consciousness concepts
- Applies "Superintelligence" (Nick Bostrom) safety principles
- UNESCO AI Ethics compliance
- AU Continental AI Strategy alignment

## Troubleshooting

### Issue: ChatDev not found

**Solution:**
```bash
# Ensure ChatDev is installed
cd ChatDev
python run.py --help
```

### Issue: Power not appearing in Kiro

**Solution:**
1. Verify the path is correct (absolute path required)
2. Check that POWER.md exists in the directory
3. Restart Kiro if needed
4. Check Kiro logs for errors

### Issue: Agents not collaborating

**Solution:**
1. Check `.chatdev/agents.json` configuration
2. Verify workflow configuration in `.chatdev/workflows.json`
3. Review ChatDev logs: `tail -f ChatDev/logs/chatdev.log`

## Next Steps

1. **Review the main documentation** in POWER.md
2. **Read the steering files** for detailed workflows
3. **Configure agents** for your specific needs
4. **Start with a simple task** to test the setup
5. **Integrate with your SyncSenta specs**
6. **Iterate and refine** based on results

## Resources

- **ChatDev GitHub**: https://github.com/OpenBMB/ChatDev
- **ChatDev Documentation**: https://chatdev.ai/docs
- **SyncSenta Specs**: `.kiro/specs/syncsenta-education-os/`
- **Power Documentation**: `POWER.md`
- **AI Safety Workflows**: `steering/advanced-ai-safety.md`
- **Web4 Workflows**: `steering/web4-blockchain-workflows.md`

## Support

For issues or questions:
1. Check the troubleshooting section in POWER.md
2. Review the steering files for specific workflows
3. Consult ChatDev documentation
4. Check SyncSenta specs for requirements

---

**Built with:** ChatDev by OpenBMB
**For:** SyncSenta Web4 Education OS
**Principles:** Ethical AI, User Sovereignty, Decentralization-First
