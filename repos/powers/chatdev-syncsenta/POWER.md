---
name: "chatdev-syncsenta"
displayName: "ChatDev for SyncSenta"
description: "Holistic multi-agent software development framework for SyncSenta Education OS. Simulates a virtual software company with specialized AI agents (CEO, CTO, Programmer, Tester) collaborating through the entire development lifecycle - from requirements to deployment."
keywords: ["chatdev", "multi-agent", "syncsenta", "web4", "education", "dapp", "development", "automation", "ai-agents"]
author: "SyncSenta Team"
---

# ChatDev for SyncSenta

## Overview

**ChatDev for SyncSenta** is a comprehensive multi-agent development framework specifically tailored for building the SyncSenta Web4 Education Operating System. It simulates a complete virtual software company powered by Large Language Models (LLMs), orchestrating specialized AI agents to collaborate through the entire software development lifecycle.

This power brings the full capabilities of the ChatDev framework to your SyncSenta dApp development, enabling:

- **Multi-Agent Collaboration**: CEO, CTO, Programmer, Tester, Designer, and more agents working together
- **Complete SDLC Automation**: From requirements gathering to deployment
- **Specialized for SyncSenta**: Pre-configured for React, Rust, Blockchain, IPFS, and Web4 architecture
- **Ethical AI Integration**: Built-in safety checks aligned with SyncSenta's AI ethics framework
- **Decentralized Development**: Supports Web4-native development patterns

### Key Capabilities

1. **Requirements Analysis**: CEO and Product Manager agents analyze and refine feature requirements
2. **Technical Design**: CTO and Architect agents design system architecture and component structure
3. **Code Generation**: Programmer agents generate React components, Rust backend code, smart contracts
4. **Testing & QA**: Tester agents create and run property-based tests, unit tests, and E2E tests
5. **Code Review**: Reviewer agents ensure code quality, security, and adherence to best practices
6. **Documentation**: Technical Writer agents generate comprehensive documentation
7. **Deployment**: DevOps agents handle deployment to Vercel, Fly.io, and blockchain networks

## Onboarding

### Prerequisites

**System Requirements:**
- Node.js 18+ (for ChatDev framework)
- Python 3.9+ (for ChatDev core)
- Git (for version control)
- Docker (optional, for containerized development)

**SyncSenta-Specific Requirements:**
- Rust toolchain (for backend development)
- Polygon RPC endpoint (for blockchain integration)
- IPFS node or gateway access
- OpenAI API key or compatible LLM endpoint

**Development Environment:**
- VS Code or similar IDE
- Terminal access
- Kiro IDE (you're already here!)

### Installation

#### Step 1: Install ChatDev Framework

```bash
# Clone ChatDev repository
git clone https://github.com/OpenBMB/ChatDev.git
cd ChatDev

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key or LLM endpoint
```

#### Step 2: Configure for SyncSenta

```bash
# Navigate to your SyncSenta workspace
cd /path/to/syncsenta-workspace

# Create ChatDev configuration
mkdir -p .chatdev
cd .chatdev

# Create SyncSenta-specific agent configurations
# (We'll provide templates in the Configuration section below)
```

#### Step 3: Verify Installation

```bash
# Test ChatDev installation
python ChatDev/run.py --help

# Expected output: ChatDev command-line interface help
```

### Configuration

#### Agent Configuration for SyncSenta

Create `.chatdev/agents.json` in your SyncSenta workspace:

```json
{
  "agents": {
    "ceo": {
      "role": "Chief Executive Officer",
      "expertise": ["product vision", "stakeholder management", "strategic planning"],
      "context": "SyncSenta Web4 Education OS - decentralized, AI-driven learning platform",
      "constraints": ["ethical AI", "user sovereignty", "educational equity"]
    },
    "cto": {
      "role": "Chief Technology Officer",
      "expertise": ["system architecture", "Web4 infrastructure", "blockchain", "IPFS"],
      "tech_stack": ["React", "TypeScript", "Rust", "Axum", "Polygon", "IPFS", "W3C DID"],
      "constraints": ["decentralization-first", "scalability", "security"]
    },
    "programmer_frontend": {
      "role": "Frontend Developer",
      "expertise": ["React", "TypeScript", "Tailwind CSS", "Shadcn/UI", "Web3", "ethers.js"],
      "focus": ["component development", "state management", "PWA", "accessibility"]
    },
    "programmer_backend": {
      "role": "Backend Developer",
      "expertise": ["Rust", "Axum", "PostgreSQL", "Redis", "sqlx", "async programming"],
      "focus": ["API development", "database design", "performance optimization"]
    },
    "programmer_blockchain": {
      "role": "Blockchain Developer",
      "expertise": ["Solidity", "Smart Contracts", "Polygon", "ethers-rs", "Web3"],
      "focus": ["credential contracts", "token economy", "on-chain governance"]
    },
    "ai_safety_engineer": {
      "role": "AI Safety Engineer",
      "expertise": ["AI alignment", "value learning", "interpretability", "safety monitoring"],
      "focus": ["Mwalimu AI safety", "bias detection", "ethical guardrails"],
      "frameworks": ["UNESCO AI Ethics", "AU Continental AI Strategy"]
    },
    "tester": {
      "role": "Quality Assurance Engineer",
      "expertise": ["property-based testing", "unit testing", "E2E testing", "security testing"],
      "tools": ["proptest", "fast-check", "Vitest", "Playwright"],
      "focus": ["correctness properties", "edge cases", "security vulnerabilities"]
    },
    "reviewer": {
      "role": "Code Reviewer",
      "expertise": ["code quality", "security review", "best practices", "performance"],
      "focus": ["WCAG compliance", "DPA 2019 compliance", "Web4 patterns"]
    },
    "technical_writer": {
      "role": "Technical Writer",
      "expertise": ["documentation", "API docs", "user guides", "architecture diagrams"],
      "focus": ["clarity", "completeness", "accessibility"]
    }
  }
}
```

#### Workflow Configuration

Create `.chatdev/workflows.json`:

```json
{
  "workflows": {
    "feature_development": {
      "phases": [
        {
          "name": "requirements",
          "agents": ["ceo", "cto"],
          "output": "requirements.md"
        },
        {
          "name": "design",
          "agents": ["cto", "programmer_frontend", "programmer_backend", "programmer_blockchain"],
          "output": "design.md"
        },
        {
          "name": "implementation",
          "agents": ["programmer_frontend", "programmer_backend", "programmer_blockchain"],
          "output": "code"
        },
        {
          "name": "ai_safety_review",
          "agents": ["ai_safety_engineer"],
          "output": "safety_report.md"
        },
        {
          "name": "testing",
          "agents": ["tester"],
          "output": "tests"
        },
        {
          "name": "review",
          "agents": ["reviewer"],
          "output": "review_report.md"
        },
        {
          "name": "documentation",
          "agents": ["technical_writer"],
          "output": "docs"
        }
      ]
    },
    "bugfix": {
      "phases": [
        {
          "name": "diagnosis",
          "agents": ["tester", "programmer_frontend", "programmer_backend"],
          "output": "bug_analysis.md"
        },
        {
          "name": "fix",
          "agents": ["programmer_frontend", "programmer_backend", "programmer_blockchain"],
          "output": "fix_code"
        },
        {
          "name": "verification",
          "agents": ["tester"],
          "output": "test_results"
        },
        {
          "name": "review",
          "agents": ["reviewer"],
          "output": "review_report.md"
        }
      ]
    },
    "ai_feature": {
      "phases": [
        {
          "name": "requirements",
          "agents": ["ceo", "ai_safety_engineer"],
          "output": "ai_requirements.md"
        },
        {
          "name": "safety_design",
          "agents": ["ai_safety_engineer", "cto"],
          "output": "safety_design.md"
        },
        {
          "name": "implementation",
          "agents": ["programmer_backend", "ai_safety_engineer"],
          "output": "code"
        },
        {
          "name": "safety_testing",
          "agents": ["ai_safety_engineer", "tester"],
          "output": "safety_tests"
        },
        {
          "name": "ethics_review",
          "agents": ["ai_safety_engineer", "reviewer"],
          "output": "ethics_report.md"
        }
      ]
    }
  }
}
```

## Common Workflows

### Workflow 1: Feature Development with Multi-Agent Collaboration

**Goal:** Develop a new feature for SyncSenta using the full ChatDev agent team.

**Steps:**

1. **Initialize ChatDev Session**
   ```bash
   cd /path/to/ChatDev
   python run.py --task "Implement blockchain credential minting for SyncSenta" \
                 --name "credential-minting" \
                 --org "SyncSenta" \
                 --config /path/to/syncsenta/.chatdev/agents.json
   ```

2. **Requirements Phase (CEO + CTO)**
   - CEO agent analyzes business requirements
   - CTO agent translates to technical requirements
   - Output: `requirements.md` with acceptance criteria

3. **Design Phase (CTO + Architects)**
   - System architecture design
   - Component structure
   - API contracts
   - Database schema
   - Output: `design.md` with diagrams

4. **Implementation Phase (Programmers)**
   - Frontend: React components, Web3 integration
   - Backend: Rust API endpoints, database operations
   - Blockchain: Smart contract updates
   - Output: Working code in appropriate directories

5. **AI Safety Review (AI Safety Engineer)**
   - Review AI components for alignment
   - Check ethical guardrails
   - Verify bias detection
   - Output: `safety_report.md`

6. **Testing Phase (Testers)**
   - Property-based tests
   - Unit tests
   - Integration tests
   - E2E tests
   - Output: Test suites with >90% coverage

7. **Code Review (Reviewers)**
   - Security review
   - Performance review
   - Best practices check
   - WCAG compliance
   - Output: `review_report.md` with recommendations

8. **Documentation (Technical Writers)**
   - API documentation
   - User guides
   - Architecture docs
   - Output: Comprehensive documentation

**Complete Example:**

```bash
# Full feature development workflow
python ChatDev/run.py \
  --task "Implement Mwalimu AI 3.0 with consciousness-aware design and value alignment" \
  --name "mwalimu-ai-3.0" \
  --org "SyncSenta" \
  --config .chatdev/agents.json \
  --workflow feature_development \
  --output ./features/mwalimu-ai-3.0

# ChatDev will orchestrate all agents through the complete lifecycle
# Output will be in ./features/mwalimu-ai-3.0/ with:
# - requirements.md
# - design.md
# - src/ (code)
# - tests/ (test suites)
# - docs/ (documentation)
# - safety_report.md
# - review_report.md
```

### Workflow 2: AI Feature Development with Safety-First Approach

**Goal:** Develop AI features with comprehensive safety checks and ethical review.

**Steps:**

1. **Safety-First Requirements**
   ```bash
   python ChatDev/run.py \
     --task "Add AI-powered learning path generation with value alignment" \
     --workflow ai_feature \
     --safety-mode strict
   ```

2. **AI Safety Engineer Reviews Requirements**
   - Identifies potential alignment issues
   - Defines safety constraints
   - Specifies monitoring requirements
   - Output: `ai_requirements.md` with safety criteria

3. **Safety Design Phase**
   - Circuit breaker design
   - Interpretability mechanisms
   - Bias detection systems
   - Value drift monitoring
   - Output: `safety_design.md`

4. **Implementation with Safety Checks**
   - Programmers implement with safety constraints
   - AI Safety Engineer reviews each component
   - Continuous safety validation
   - Output: Code with embedded safety mechanisms

5. **Safety Testing**
   - Adversarial testing
   - Bias testing
   - Alignment testing
   - Edge case testing
   - Output: Comprehensive safety test suite

6. **Ethics Review**
   - UNESCO AI Ethics compliance
   - AU Continental AI Strategy alignment
   - Human rights impact assessment
   - Output: `ethics_report.md`

**Example:**

```bash
# AI feature with safety-first approach
python ChatDev/run.py \
  --task "Implement predictive at-risk student detection with fairness guarantees" \
  --workflow ai_feature \
  --safety-mode strict \
  --ethics-framework "UNESCO,AU-Continental" \
  --output ./features/at-risk-detection

# Agents will ensure:
# - No discriminatory bias
# - Transparent decision-making
# - Human oversight mechanisms
# - Privacy preservation
# - Contestability
```

### Workflow 3: Blockchain Smart Contract Development

**Goal:** Develop and deploy smart contracts for SyncSenta credentials and tokens.

**Steps:**

1. **Smart Contract Requirements**
   ```bash
   python ChatDev/run.py \
     --task "Create ERC-721 credential contract with revocation and verification" \
     --agents blockchain \
     --network polygon-mumbai
   ```

2. **Contract Design**
   - Blockchain Developer designs contract architecture
   - Security patterns (ReentrancyGuard, AccessControl)
   - Gas optimization strategies
   - Output: Contract specifications

3. **Implementation**
   - Solidity contract code
   - Deployment scripts
   - Verification scripts
   - Output: Deployable contracts

4. **Security Audit**
   - Reviewer performs security audit
   - Checks for common vulnerabilities
   - Gas optimization review
   - Output: Security audit report

5. **Testing**
   - Unit tests with Hardhat
   - Integration tests
   - Mainnet fork testing
   - Output: Comprehensive test suite

6. **Deployment**
   - Deploy to testnet
   - Verify on Polygonscan
   - Deploy to mainnet
   - Output: Deployed contract addresses

**Example:**

```bash
# Smart contract development
python ChatDev/run.py \
  --task "Implement SyncToken ERC-20 with learn-to-earn mechanics" \
  --agents blockchain,tester,reviewer \
  --network polygon-mumbai \
  --output ./contracts/sync-token

# Outputs:
# - contracts/SyncToken.sol
# - scripts/deploy.js
# - test/SyncToken.test.js
# - docs/SyncToken.md
```

### Workflow 4: Bug Diagnosis and Fix

**Goal:** Diagnose and fix bugs with multi-agent collaboration.

**Steps:**

1. **Bug Report Analysis**
   ```bash
   python ChatDev/run.py \
     --task "Fix: Mwalimu AI not responding to voice input" \
     --workflow bugfix \
     --bug-report ./bugs/issue-123.md
   ```

2. **Diagnosis Phase**
   - Tester reproduces the bug
   - Programmers analyze root cause
   - Output: `bug_analysis.md` with root cause

3. **Fix Implementation**
   - Appropriate programmer implements fix
   - Follows minimal change principle
   - Output: Fixed code

4. **Verification**
   - Tester verifies fix
   - Regression testing
   - Output: Test results

5. **Review**
   - Reviewer checks fix quality
   - Ensures no side effects
   - Output: Review approval

**Example:**

```bash
# Bug fix workflow
python ChatDev/run.py \
  --task "Fix: Token minting fails when learner achieves 90% mastery" \
  --workflow bugfix \
  --bug-report ./bugs/token-minting-issue.md \
  --output ./fixes/token-minting-fix

# Agents collaborate to:
# - Reproduce the bug
# - Identify root cause
# - Implement minimal fix
# - Verify fix works
# - Ensure no regressions
```

### Workflow 5: Documentation Generation

**Goal:** Generate comprehensive documentation for SyncSenta components.

**Steps:**

1. **Documentation Request**
   ```bash
   python ChatDev/run.py \
     --task "Generate API documentation for Mwalimu AI endpoints" \
     --agents technical_writer \
     --source ./backend/src/mwalimu_ai
   ```

2. **Code Analysis**
   - Technical Writer analyzes code
   - Extracts API contracts
   - Identifies usage patterns
   - Output: Documentation outline

3. **Documentation Writing**
   - API reference
   - Usage examples
   - Error handling
   - Best practices
   - Output: Complete documentation

4. **Review**
   - Programmer reviews for accuracy
   - Tester verifies examples work
   - Output: Approved documentation

**Example:**

```bash
# Documentation generation
python ChatDev/run.py \
  --task "Generate complete API documentation for blockchain service" \
  --agents technical_writer,programmer_blockchain \
  --source ./backend/src/blockchain \
  --output ./docs/api/blockchain

# Outputs:
# - API reference
# - Usage examples
# - Error codes
# - Best practices
# - Integration guide
```

## Advanced Features

### Multi-Agent Communication Patterns

ChatDev agents communicate through structured protocols:

**1. Chain of Thought Communication**
```python
# CEO → CTO → Programmer → Tester → Reviewer
# Each agent builds on previous agent's output
```

**2. Parallel Collaboration**
```python
# Frontend + Backend + Blockchain programmers work simultaneously
# Coordinated by CTO agent
```

**3. Iterative Refinement**
```python
# Programmer → Reviewer → Programmer (iterate until approved)
```

### Custom Agent Creation

Create specialized agents for SyncSenta:

```json
{
  "agents": {
    "web4_specialist": {
      "role": "Web4 Architecture Specialist",
      "expertise": ["decentralization", "IPFS", "blockchain", "DID", "Web3"],
      "focus": ["censorship resistance", "user sovereignty", "data ownership"]
    },
    "education_specialist": {
      "role": "Educational Technology Specialist",
      "expertise": ["pedagogy", "CBC curriculum", "learning science", "SEL"],
      "focus": ["learner-centered design", "mastery-based progression"]
    },
    "ethics_specialist": {
      "role": "AI Ethics Specialist",
      "expertise": ["AI safety", "value alignment", "fairness", "transparency"],
      "frameworks": ["UNESCO", "AU Continental AI Strategy", "Beneficial AI"]
    }
  }
}
```

### Integration with Kiro Specs

ChatDev can work directly with Kiro specs:

```bash
# Generate implementation from spec
python ChatDev/run.py \
  --spec .kiro/specs/syncsenta-education-os/requirements.md \
  --design .kiro/specs/syncsenta-education-os/design.md \
  --tasks .kiro/specs/syncsenta-education-os/tasks.md \
  --output ./implementation

# ChatDev reads specs and generates:
# - Complete implementation
# - Tests
# - Documentation
```

## Troubleshooting

### Issue: ChatDev Agents Not Collaborating

**Symptoms:**
- Agents produce disconnected outputs
- No communication between agents
- Workflow stalls

**Cause:** Misconfigured agent communication protocol

**Solution:**
1. Check `.chatdev/agents.json` for proper agent definitions
2. Verify workflow configuration in `.chatdev/workflows.json`
3. Ensure agents have compatible expertise areas
4. Review ChatDev logs: `tail -f ChatDev/logs/chatdev.log`

### Issue: Generated Code Doesn't Match SyncSenta Architecture

**Symptoms:**
- Code uses wrong tech stack
- Doesn't follow Web4 patterns
- Missing decentralization features

**Cause:** Agents not properly configured with SyncSenta context

**Solution:**
1. Update agent configurations with SyncSenta-specific context
2. Add tech stack constraints to CTO and programmer agents
3. Include architecture guidelines in agent prompts
4. Use `--context` flag to provide additional context:
   ```bash
   python ChatDev/run.py \
     --task "..." \
     --context "SyncSenta Web4 Education OS: React, Rust, Polygon, IPFS, DID" \
     --architecture-doc .kiro/specs/syncsenta-education-os/design.md
   ```

### Issue: AI Safety Checks Failing

**Symptoms:**
- Safety engineer rejects implementations
- Ethical concerns raised
- Alignment issues detected

**Cause:** Implementation doesn't meet safety requirements

**Solution:**
1. Review safety requirements in `ai_requirements.md`
2. Implement suggested safety mechanisms
3. Add interpretability features
4. Include bias detection
5. Implement circuit breakers
6. Re-run with `--safety-mode strict`

### Issue: Property-Based Tests Not Generated

**Symptoms:**
- Only unit tests created
- No proptest or fast-check tests
- Missing correctness properties

**Cause:** Tester agent not configured for property-based testing

**Solution:**
1. Update tester agent configuration:
   ```json
   {
     "tester": {
       "testing_strategy": "property-based-first",
       "tools": ["proptest", "fast-check"],
       "focus": ["correctness properties", "invariants", "edge cases"]
     }
   }
   ```
2. Provide property examples in task description
3. Reference spec correctness properties

### Issue: Smart Contracts Have Security Vulnerabilities

**Symptoms:**
- Security audit fails
- Common vulnerabilities detected
- Gas inefficiencies

**Cause:** Blockchain developer agent needs security patterns

**Solution:**
1. Update blockchain agent with security expertise:
   ```json
   {
     "programmer_blockchain": {
       "security_patterns": [
         "ReentrancyGuard",
         "AccessControl",
         "Pausable",
         "SafeMath"
       ],
       "audit_checklist": "OpenZeppelin security guidelines"
     }
   }
   ```
2. Run security-focused review:
   ```bash
   python ChatDev/run.py \
     --task "Security audit of SyncToken contract" \
     --agents reviewer \
     --focus security \
     --checklist ./security/smart-contract-checklist.md
   ```

### Issue: Documentation Incomplete or Inaccurate

**Symptoms:**
- Missing API endpoints
- Incorrect examples
- Outdated information

**Cause:** Technical writer agent working from stale code

**Solution:**
1. Ensure technical writer has access to latest code
2. Run documentation generation after code is finalized
3. Include programmer in documentation review
4. Use `--source` flag to point to correct code:
   ```bash
   python ChatDev/run.py \
     --task "Update API documentation" \
     --agents technical_writer,programmer_backend \
     --source ./backend/src \
     --verify-examples
   ```

## Best Practices

### 1. Start with Clear Requirements

**Good:**
```bash
python ChatDev/run.py \
  --task "Implement blockchain credential minting: When learner achieves 90%+ mastery, mint ERC-721 NFT with IPFS metadata within 60 seconds" \
  --acceptance-criteria .kiro/specs/syncsenta-education-os/requirements.md#requirement-26
```

**Bad:**
```bash
python ChatDev/run.py --task "Add credentials"
```

### 2. Use Appropriate Workflows

- **New features** → `feature_development` workflow
- **Bug fixes** → `bugfix` workflow
- **AI features** → `ai_feature` workflow (with safety checks)
- **Smart contracts** → `blockchain` workflow (with security audit)

### 3. Leverage Agent Expertise

- **Frontend** → `programmer_frontend`
- **Backend** → `programmer_backend`
- **Blockchain** → `programmer_blockchain`
- **AI Safety** → `ai_safety_engineer`
- **Testing** → `tester`
- **Review** → `reviewer`

### 4. Iterate with Feedback

```bash
# Initial implementation
python ChatDev/run.py --task "..." --output ./v1

# Review and iterate
python ChatDev/run.py \
  --task "Refine based on review feedback" \
  --input ./v1/review_report.md \
  --output ./v2
```

### 5. Integrate with Kiro Specs

```bash
# Use specs as source of truth
python ChatDev/run.py \
  --spec .kiro/specs/syncsenta-education-os/requirements.md \
  --design .kiro/specs/syncsenta-education-os/design.md \
  --tasks .kiro/specs/syncsenta-education-os/tasks.md
```

### 6. Safety-First for AI Features

```bash
# Always use ai_feature workflow for AI components
python ChatDev/run.py \
  --task "..." \
  --workflow ai_feature \
  --safety-mode strict \
  --ethics-framework "UNESCO,AU-Continental"
```

### 7. Test Before Merge

```bash
# Generate tests first
python ChatDev/run.py \
  --task "Generate property-based tests for credential minting" \
  --agents tester \
  --output ./tests

# Then implement
python ChatDev/run.py \
  --task "Implement credential minting" \
  --tests ./tests \
  --output ./implementation
```

### 8. Document as You Build

```bash
# Include documentation in workflow
python ChatDev/run.py \
  --task "..." \
  --workflow feature_development \
  --include-docs
```

### 9. Security Review for Blockchain

```bash
# Always include security review for smart contracts
python ChatDev/run.py \
  --task "..." \
  --agents blockchain,reviewer \
  --security-audit \
  --audit-checklist ./security/checklist.md
```

### 10. Version Control Integration

```bash
# Create feature branch
git checkout -b feature/chatdev-generated

# Run ChatDev
python ChatDev/run.py --task "..." --output ./feature

# Review and commit
git add ./feature
git commit -m "feat: ChatDev generated implementation"
git push origin feature/chatdev-generated
```

## Configuration

### Environment Variables

Create `.env` in ChatDev directory:

```bash
# LLM Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# Or use alternative LLM
ANTHROPIC_API_KEY=your-anthropic-key
ANTHROPIC_MODEL=claude-3-opus-20240229

# SyncSenta Configuration
SYNCSENTA_WORKSPACE=/path/to/syncsenta
SYNCSENTA_SPEC_DIR=.kiro/specs/syncsenta-education-os

# Blockchain Configuration
POLYGON_RPC_URL=https://polygon-mumbai.g.alchemy.com/v2/your-key
POLYGON_PRIVATE_KEY=your-private-key

# IPFS Configuration
IPFS_GATEWAY=https://ipfs.io
PINATA_API_KEY=your-pinata-key
PINATA_SECRET_KEY=your-pinata-secret

# Testing Configuration
RUN_PROPERTY_TESTS=true
TEST_COVERAGE_THRESHOLD=90

# Safety Configuration
AI_SAFETY_MODE=strict
ETHICS_FRAMEWORKS=UNESCO,AU-Continental
```

### Agent Customization

Edit `.chatdev/agents.json` to customize agent behavior:

```json
{
  "agents": {
    "programmer_frontend": {
      "llm_model": "gpt-4-turbo-preview",
      "temperature": 0.2,
      "max_tokens": 4000,
      "code_style": "airbnb",
      "frameworks": ["React", "TypeScript", "Tailwind"],
      "best_practices": [
        "WCAG 2.1 AA compliance",
        "Semantic HTML",
        "Accessibility-first",
        "Mobile-first responsive design"
      ]
    }
  }
}
```

## Integration with SyncSenta Workflow

### Step 1: Spec-Driven Development

```bash
# Start with Kiro spec
kiro spec create syncsenta-feature

# Use ChatDev to implement from spec
python ChatDev/run.py \
  --spec .kiro/specs/syncsenta-feature/requirements.md \
  --design .kiro/specs/syncsenta-feature/design.md \
  --output ./implementation
```

### Step 2: Task Execution

```bash
# Execute specific tasks from tasks.md
python ChatDev/run.py \
  --tasks .kiro/specs/syncsenta-education-os/tasks.md \
  --task-id "2.1" \
  --output ./task-2.1-implementation
```

### Step 3: Testing Integration

```bash
# Generate tests matching spec properties
python ChatDev/run.py \
  --task "Generate property-based tests" \
  --spec .kiro/specs/syncsenta-education-os/requirements.md \
  --properties-section "Correctness Properties" \
  --output ./tests
```

### Step 4: Continuous Integration

```bash
# Add to CI/CD pipeline
# .github/workflows/chatdev.yml
name: ChatDev CI
on: [push, pull_request]
jobs:
  chatdev-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run ChatDev Code Review
        run: |
          python ChatDev/run.py \
            --task "Review changes in this PR" \
            --agents reviewer \
            --diff ${{ github.event.pull_request.diff_url }}
```

## Additional Resources

- **ChatDev GitHub**: https://github.com/OpenBMB/ChatDev
- **ChatDev Documentation**: https://chatdev.ai/docs
- **SyncSenta Specs**: `.kiro/specs/syncsenta-education-os/`
- **Multi-Agent Systems**: https://arxiv.org/abs/2308.10848
- **AI Safety Resources**: https://www.safe.ai/

---

**Framework:** ChatDev by OpenBMB
**Integration:** SyncSenta Web4 Education OS
**License:** Apache 2.0
