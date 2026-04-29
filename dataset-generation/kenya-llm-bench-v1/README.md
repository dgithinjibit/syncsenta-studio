# Kenya-LLM-Bench-v1 Dataset Generation

## Overview

This directory contains the infrastructure for generating the **Kenya-LLM-Bench-v1** dataset - the first comprehensive CBC-aligned educational dialogue dataset for training culturally authentic AI tutors for Kenya and Africa.

## Dataset Specifications

### Target Metrics
- **1,000+ high-quality dialogues** covering all CBC curriculum strands
- **Culturally authentic** Kenyan context with Swahili/English code-switching
- **Grade coverage**: PP1 through Form 4 with appropriate difficulty progression
- **Pedagogical approach**: Socratic method dialogues that guide discovery learning
- **Question diversity**: Conceptual, procedural, application, and analysis questions

### Data Structure
```json
{
  "dialogue_id": "cbc_math_pp1_001",
  "grade_level": "PP1",
  "subject": "Mathematics",
  "curriculum_strand": "Numbers",
  "sub_strand": "Counting",
  "learning_objective": "Count objects up to 10",
  "cultural_context": "kenyan_foods",
  "language_mix": "english_swahili",
  "dialogue": [
    {
      "role": "student",
      "content": "Mwalimu, how many mangoes are there?",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "role": "tutor",
      "content": "Karibu! Let's count together. Can you point to each mango as we count? Moja...",
      "timestamp": "2024-01-01T10:00:05Z",
      "pedagogical_technique": "guided_discovery",
      "cultural_elements": ["swahili_greeting", "kenyan_fruit"]
    }
  ],
  "learning_outcome": "achieved",
  "difficulty_level": 1,
  "metadata": {
    "generated_by": "kiro_moe",
    "reviewed": true,
    "cultural_authenticity_score": 0.95,
    "pedagogical_effectiveness_score": 0.92
  }
}
```

## Generation Pipeline

1. **CBC Curriculum Mapping**: Load official KICD curriculum structure
2. **Cultural Context Library**: Kenyan foods, greetings, examples, scenarios
3. **Dialogue Generation**: AI-powered creation with quality controls
4. **Cultural Validation**: Authenticity scoring and review
5. **Pedagogical Validation**: Educational effectiveness assessment
6. **Format Conversion**: Transform to Hugging Face SFT format
7. **Upload & Publishing**: Deploy to Hugging Face Hub

## Files Structure

```
dataset-generation/kenya-llm-bench-v1/
├── README.md                          # This file
├── src/
│   ├── curriculum_loader.py           # CBC curriculum structure
│   ├── cultural_context.py            # Kenyan cultural elements
│   ├── dialogue_generator.py          # Core generation engine
│   ├── quality_validator.py           # Authenticity & pedagogy scoring
│   └── hf_uploader.py                 # Hugging Face integration
├── data/
│   ├── cbc_curriculum.json            # Official KICD structure
│   ├── cultural_elements.json         # Kenyan context library
│   └── generated_dialogues/           # Output directory
├── config/
│   ├── generation_config.yaml         # Generation parameters
│   └── hf_config.yaml                 # Hugging Face settings
└── scripts/
    ├── generate_dataset.py             # Main generation script
    ├── validate_quality.py             # Quality assurance
    └── upload_to_hf.py                 # Publishing script
```

## Usage

```bash
# 1. Generate the dataset
python scripts/generate_dataset.py --target-size 1000 --quality-threshold 0.9

# 2. Validate quality
python scripts/validate_quality.py --input data/generated_dialogues/

# 3. Upload to Hugging Face
python scripts/upload_to_hf.py --token $HF_TOKEN --repo kenya-llm-bench-v1
```

## Quality Standards

### Cultural Authenticity Criteria
- ✅ Appropriate Swahili/English code-switching patterns
- ✅ Kenyan food references (ugali, sukuma wiki, chapati, etc.)
- ✅ Local greetings and social conventions
- ✅ Familiar scenarios and contexts
- ✅ Respectful cultural representation

### Pedagogical Effectiveness Criteria
- ✅ Socratic method implementation
- ✅ Scaffolded learning progression
- ✅ Appropriate difficulty for grade level
- ✅ Clear learning objectives alignment
- ✅ Engaging and motivating content

## Impact Goals

1. **Establish Kenya as African AI leader** in educational technology
2. **Enable culturally authentic AI tutors** for 47+ million Kenyans
3. **Create replicable model** for other African countries
4. **Advance open-source AI** for educational equity
5. **Support CBC curriculum implementation** at scale

---

**Status**: 🔥 **HIGH PRIORITY** - Critical for SyncSenta's AI authenticity
**Timeline**: Target completion within 2 weeks
**Owner**: Kiro MoE with human oversight