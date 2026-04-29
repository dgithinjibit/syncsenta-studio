# 🚀 SyncSenta AI Training Infrastructure

**Production-level training pipeline for Kenya-LLM-Bench-v1 dataset**

Fine-tune Llama 3.1 with authentic Kenyan cultural context and CBC curriculum alignment to create a world-class educational AI tutor that rivals Synthesis Tutor and Magic School AI.

---

## 🎯 **VISION**

Create the **first production-grade open source educational AI** with:
- 🇰🇪 **Authentic Kenyan cultural context** (Swahili/English code-switching)
- 📚 **CBC curriculum alignment** (Kenya's Competency-Based Curriculum)
- 💰 **Cost efficiency** ($0.001/request vs $0.03+ for competitors)
- 🔒 **Data sovereignty** (self-hosted, no external API dependencies)
- 🛠️ **Full customization** (open source advantage)

---

## 🏗️ **ARCHITECTURE**

### **Training Pipeline**
```
Kenya-LLM-Bench-v1 → Fine-tuning → RLHF → Production Model
   (1,000 dialogues)    (Llama 3.1)   (Teacher feedback)   (Candle inference)
```

### **Technology Stack**
- **Foundation Model**: Meta Llama 3.1 8B/70B
- **Training Framework**: Candle (Rust ML framework)
- **Hardware**: AMD ROCm (cost-efficient GPU training)
- **Dataset**: Kenya-LLM-Bench-v1 (authentic Kenyan educational dialogues)
- **Inference**: Self-hosted Candle inference engine

---

## 🚀 **QUICK START**

### **Prerequisites**
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install AMD ROCm (for AMD GPUs)
# Follow: https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html

# Clone repository
git clone <repo-url>
cd ai-training
```

### **Setup Training Environment**
```bash
# Build training infrastructure
cargo build --release --features rocm

# Validate setup (dry run)
./target/release/train-kenya-llama --dry-run

# Check dataset availability
ls -la ../dataset-generation/kenya-llm-bench-v1/data/generated_dialogues/
```

### **Start Training**
```bash
# Fine-tune Llama 3.1 8B on Kenya-LLM-Bench-v1
./target/release/train-kenya-llama \
  --model meta-llama/Llama-3.1-8B \
  --epochs 3 \
  --batch-size 32 \
  --learning-rate 2e-5 \
  --rocm
```

### **Monitor Training**
```bash
# Training logs show progress
tail -f training.log

# Model checkpoints saved to models/
ls -la models/kenya-llama-v1/
```

---

## 📊 **TRAINING CONFIGURATION**

### **Optimized for AMD ROCm**
```toml
[training]
device = "rocm"              # AMD GPU acceleration
batch_size = 32              # Optimized for AMD memory
learning_rate = 2e-5         # Conservative for fine-tuning
num_epochs = 3               # Prevent overfitting
gradient_accumulation = 4    # Memory efficiency
```

### **Cultural Authenticity Weighting**
```toml
[cultural]
swahili_weight = 2.0         # Prioritize Swahili elements
kenyan_context_weight = 1.8  # Boost Kenyan cultural references
cbc_alignment_weight = 1.5   # Enhance curriculum alignment
```

### **Dataset Configuration**
```toml
[dataset]
train_path = "../dataset-generation/kenya-llm-bench-v1/data/generated_dialogues/kenya_llm_bench_v1_complete.json"
max_length = 2048            # Token limit per example
cultural_weight = 1.5        # Boost culturally authentic examples
curriculum_weight = 1.3      # Boost CBC-aligned examples
```

---

## 🎓 **TRAINING PROCESS**

### **Phase 1: Supervised Fine-tuning (Week 1-2)**
1. **Load Llama 3.1 8B** base model
2. **Convert Kenya-LLM-Bench-v1** to training format
3. **Apply cultural weighting** to prioritize authentic examples
4. **Fine-tune** with CBC curriculum alignment
5. **Validate** on held-out test set

### **Phase 2: Reinforcement Learning (Week 3-4)**
1. **Collect teacher feedback** on cultural authenticity
2. **Train reward model** on teacher preferences
3. **Apply RLHF** using PPO (Proximal Policy Optimization)
4. **Optimize** for cultural authenticity and pedagogical effectiveness

### **Phase 3: Production Deployment (Week 5-6)**
1. **Optimize inference** with Candle framework
2. **Deploy self-hosted** inference server
3. **Integrate** with SyncSenta platform
4. **Monitor** performance and cultural authenticity

---

## 📈 **PERFORMANCE TARGETS**

### **Quality Metrics**
- **Cultural Authenticity**: >95% (unique competitive advantage)
- **Pedagogical Effectiveness**: >90% (match Synthesis Tutor)
- **CBC Curriculum Alignment**: >95% (Kenya-specific advantage)
- **Response Relevance**: >92% (match Magic School AI)

### **Performance Metrics**
- **Inference Latency**: <500ms (competitive with cloud APIs)
- **Throughput**: >100 requests/second (production scale)
- **Memory Usage**: <8GB VRAM (efficient deployment)
- **Training Cost**: <$1000 total (AMD cost advantage)

### **Cost Comparison**
| Provider | Cost per Request | Monthly (10K requests) |
|----------|------------------|------------------------|
| **SyncSenta (Self-hosted)** | **$0.001** | **$10** |
| OpenAI GPT-4 | $0.030 | $300 |
| Anthropic Claude | $0.015 | $150 |
| **Savings** | **97% less** | **$290 saved** |

---

## 🛠️ **DEVELOPMENT COMMANDS**

### **Training Commands**
```bash
# Full training pipeline
cargo run --bin train-kenya-llama --release

# Custom configuration
cargo run --bin train-kenya-llama -- --config custom-config.toml

# Different model sizes
cargo run --bin train-kenya-llama -- --model meta-llama/Llama-3.1-70B

# CPU training (slower)
cargo run --bin train-kenya-llama -- --device cpu
```

### **Dataset Commands**
```bash
# Convert dataset format
cargo run --bin dataset-converter

# Validate dataset quality
cargo run --bin validate-dataset

# Generate dataset statistics
cargo run --bin dataset-stats
```

### **Inference Commands**
```bash
# Start inference server
cargo run --bin inference-server --release

# Test inference
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Mwalimu, help me understand fractions", "max_tokens": 200}'
```

---

## 🔧 **CONFIGURATION FILES**

### **Training Configuration (`config/training.toml`)**
```toml
[model]
base_model = "meta-llama/Llama-3.1-8B"
context_length = 8192
vocab_size = 128256
cultural_tokens = ["habari", "karibu", "pole", "asante", "ugali", "matatu"]

[training]
device = "rocm"
batch_size = 32
learning_rate = 2e-5
num_epochs = 3
gradient_accumulation = 4
warmup_steps = 500

[dataset]
train_path = "../dataset-generation/kenya-llm-bench-v1/data/generated_dialogues/kenya_llm_bench_v1_complete.json"
eval_path = "../dataset-generation/kenya-llm-bench-v1/data/samples/sample_dialogues.json"
max_length = 2048
cultural_weight = 1.5

[cultural]
swahili_weight = 2.0
kenyan_context_weight = 1.8
cbc_alignment_weight = 1.5
```

---

## 📊 **MONITORING & EVALUATION**

### **Training Metrics**
- **Loss curves** (training and validation)
- **Cultural authenticity scores** (Swahili usage, Kenyan references)
- **Pedagogical effectiveness** (teaching technique application)
- **CBC alignment** (curriculum standard compliance)

### **Evaluation Benchmarks**
- **Cultural authenticity test set** (100 Kenyan teacher evaluations)
- **CBC curriculum coverage** (all subjects and grade levels)
- **Pedagogical technique assessment** (Socratic method, scaffolding, etc.)
- **Student engagement simulation** (response quality and relevance)

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **AMD ROCm Setup**
```bash
# Check ROCm installation
rocm-smi

# Verify GPU detection
rocminfo

# Install ROCm if missing
sudo apt install rocm-dev rocm-libs
```

#### **Memory Issues**
```bash
# Reduce batch size
--batch-size 16

# Increase gradient accumulation
--gradient-accumulation 8

# Use smaller model
--model meta-llama/Llama-3.1-8B  # instead of 70B
```

#### **Dataset Issues**
```bash
# Verify dataset exists
ls -la ../dataset-generation/kenya-llm-bench-v1/data/

# Check dataset format
head -n 10 ../dataset-generation/kenya-llm-bench-v1/data/generated_dialogues/kenya_llm_bench_v1_complete.json
```

---

## 🎯 **COMPETITIVE ADVANTAGES**

### **vs Synthesis Tutor**
- ✅ **Cultural authenticity** (Kenyan context vs generic)
- ✅ **Cost efficiency** (self-hosted vs cloud API)
- ✅ **Curriculum alignment** (CBC vs US standards)
- ✅ **Language support** (Swahili/English vs English only)

### **vs Magic School AI**
- ✅ **Educational focus** (tutor vs general assistant)
- ✅ **Cultural relevance** (Kenyan examples vs generic)
- ✅ **Data privacy** (self-hosted vs cloud)
- ✅ **Customization** (open source vs proprietary)

---

## 🚀 **NEXT STEPS**

1. **Complete training setup** (AMD ROCm + Llama 3.1)
2. **Fine-tune on Kenya-LLM-Bench-v1** (3-5 epochs)
3. **Collect teacher feedback** for RLHF
4. **Deploy inference server** (Candle + production)
5. **Integrate with SyncSenta** (MVP enhancement)

**Ready to build the future of African educational AI! 🇰🇪🚀**