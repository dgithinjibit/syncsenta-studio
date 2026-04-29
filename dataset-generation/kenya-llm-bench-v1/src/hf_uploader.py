#!/usr/bin/env python3
"""
Hugging Face Dataset Uploader for Kenya-LLM-Bench-v1

This module handles uploading the generated dataset to Hugging Face Hub
with proper formatting for supervised fine-tuning (SFT).
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, login
import yaml

class KenyaLLMBenchUploader:
    """Handles uploading Kenya-LLM-Bench-v1 to Hugging Face Hub"""
    
    def __init__(self, hf_token: str):
        """Initialize with Hugging Face token"""
        self.hf_token = hf_token
        self.api = HfApi()
        
        # Login to Hugging Face
        login(token=hf_token)
        print("✅ Logged in to Hugging Face Hub")
    
    def convert_to_sft_format(self, dialogues: List[Dict]) -> List[Dict]:
        """Convert dialogues to SFT (Supervised Fine-Tuning) format"""
        sft_data = []
        
        for dialogue in dialogues:
            # Create conversation format
            conversation = []
            
            for turn in dialogue['dialogue']:
                if turn['role'] == 'student':
                    conversation.append({
                        "from": "human",
                        "value": turn['content']
                    })
                elif turn['role'] == 'tutor':
                    conversation.append({
                        "from": "gpt", 
                        "value": turn['content']
                    })
            
            # Create SFT entry
            sft_entry = {
                "id": dialogue['dialogue_id'],
                "conversations": conversation,
                "metadata": {
                    "grade_level": dialogue['grade_level'],
                    "subject": dialogue['subject'],
                    "curriculum_strand": dialogue['curriculum_strand'],
                    "sub_strand": dialogue['sub_strand'],
                    "learning_objective": dialogue['learning_objective'],
                    "cultural_context": dialogue['cultural_context'],
                    "language_mix": dialogue['language_mix'],
                    "difficulty_level": dialogue['difficulty_level'],
                    "learning_outcome": dialogue['learning_outcome']
                }
            }
            
            sft_data.append(sft_entry)
        
        return sft_data
    
    def create_train_val_test_splits(self, data: List[Dict], 
                                   train_ratio: float = 0.8,
                                   val_ratio: float = 0.1,
                                   test_ratio: float = 0.1) -> Dict[str, List[Dict]]:
        """Create train/validation/test splits"""
        import random
        
        # Shuffle data
        shuffled_data = data.copy()
        random.shuffle(shuffled_data)
        
        total_size = len(shuffled_data)
        train_size = int(total_size * train_ratio)
        val_size = int(total_size * val_ratio)
        
        splits = {
            "train": shuffled_data[:train_size],
            "validation": shuffled_data[train_size:train_size + val_size],
            "test": shuffled_data[train_size + val_size:]
        }
        
        print(f"📊 Dataset splits created:")
        print(f"   Train: {len(splits['train'])} samples ({train_ratio*100:.1f}%)")
        print(f"   Validation: {len(splits['validation'])} samples ({val_ratio*100:.1f}%)")
        print(f"   Test: {len(splits['test'])} samples ({test_ratio*100:.1f}%)")
        
        return splits
    
    def create_dataset_card(self, stats: Dict) -> str:
        """Create comprehensive dataset card for Hugging Face"""
        card_content = f"""---
license: cc-by-4.0
task_categories:
- conversational
- text-generation
language:
- en
- sw
tags:
- education
- kenya
- cbc-curriculum
- swahili
- cultural-ai
- africa
- tutoring
- socratic-method
size_categories:
- 1K<n<10K
---

# Kenya-LLM-Bench-v1: CBC-Aligned Educational Dialogue Dataset

## Dataset Description

**Kenya-LLM-Bench-v1** is the first comprehensive educational dialogue dataset specifically designed for training culturally authentic AI tutors for Kenya's Competency-Based Curriculum (CBC). This dataset contains {stats['total_dialogues']} high-quality dialogues between AI tutors (Mwalimu) and Kenyan students, covering all major CBC curriculum strands with authentic cultural context.

### Key Features

🇰🇪 **Culturally Authentic**: Natural Swahili/English code-switching patterns
📚 **CBC-Aligned**: Covers official KICD curriculum standards  
🎓 **Pedagogically Sound**: Implements Socratic method and scaffolded learning
🌍 **Contextually Rich**: Uses familiar Kenyan foods, places, and scenarios
📊 **Comprehensive Coverage**: {len(stats['grade_distribution'])} grade levels, {len(stats['subject_distribution'])} subjects

## Dataset Statistics

- **Total Dialogues**: {stats['total_dialogues']:,}
- **Average Dialogue Length**: {stats['average_dialogue_length']:.1f} turns
- **Grade Levels**: {', '.join(stats['grade_distribution'].keys())}
- **Subjects**: {', '.join(stats['subject_distribution'].keys())}
- **Cultural Contexts**: {len(stats['cultural_context_distribution'])} different types

### Grade Distribution
{self._format_distribution(stats['grade_distribution'])}

### Subject Distribution  
{self._format_distribution(stats['subject_distribution'])}

### Cultural Context Distribution
{self._format_distribution(stats['cultural_context_distribution'])}

## Dataset Structure

Each dialogue follows this structure:

```json
{{
  "id": "cbc_math_grade1_001",
  "conversations": [
    {{
      "from": "human",
      "value": "Mwalimu, how do I count these mangoes?"
    }},
    {{
      "from": "gpt", 
      "value": "Karibu! Let's count together. Can you point to each mango as we count? Moja, mbili, tatu..."
    }}
  ],
  "metadata": {{
    "grade_level": "Grade1",
    "subject": "Mathematics", 
    "curriculum_strand": "Numbers",
    "sub_strand": "Counting",
    "learning_objective": "Count objects up to 20",
    "cultural_context": "kenyan_foods",
    "language_mix": "english_swahili",
    "difficulty_level": 2,
    "learning_outcome": "achieved"
  }}
}}
```

## Cultural Authenticity

This dataset incorporates authentic Kenyan cultural elements:

- **Language**: Natural English/Swahili code-switching patterns
- **Foods**: ugali, sukuma wiki, chapati, mandazi, githeri
- **Greetings**: Habari, Karibu, Asante, Pole, Mambo
- **Places**: Nairobi, Mombasa, Kisumu, Maasai Mara
- **Scenarios**: market, shamba, matatu, school contexts

## Pedagogical Approach

The dialogues implement research-backed educational techniques:

- **Socratic Method**: Guiding students to discover answers through questions
- **Scaffolded Learning**: Providing decreasing levels of support
- **Cultural Responsiveness**: Connecting learning to students' backgrounds
- **Mastery-Based Progression**: Ensuring understanding before advancing

## Usage

### Fine-tuning Language Models

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("syncsenta/kenya-llm-bench-v1")

# Access different splits
train_data = dataset["train"]
val_data = dataset["validation"] 
test_data = dataset["test"]

# Example conversation
print(train_data[0]["conversations"])
```

### Evaluation Benchmarking

This dataset can be used to evaluate:
- Cultural authenticity of AI responses
- Pedagogical effectiveness 
- CBC curriculum alignment
- Swahili/English code-switching quality

## Ethical Considerations

- **Cultural Representation**: Developed with deep understanding of Kenyan culture
- **Educational Equity**: Designed to support quality education for all Kenyan students
- **Language Preservation**: Promotes healthy multilingualism
- **Open Access**: CC-BY-4.0 license for maximum accessibility

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{{kenya_llm_bench_v1,
  title={{Kenya-LLM-Bench-v1: CBC-Aligned Educational Dialogue Dataset}},
  author={{SyncSenta Team}},
  year={{2024}},
  publisher={{Hugging Face}},
  url={{https://huggingface.co/datasets/syncsenta/kenya-llm-bench-v1}}
}}
```

## Contributing

We welcome contributions to improve this dataset:
- Report cultural inaccuracies
- Suggest additional curriculum coverage
- Propose quality improvements

## License

This dataset is released under CC-BY-4.0 license, allowing commercial and non-commercial use with attribution.

## Acknowledgments

- Kenya Institute of Curriculum Development (KICD) for CBC standards
- Kenyan educators who provided cultural validation
- Open source AI community for tools and frameworks

---

**Built with ❤️ for Kenya's educational future**
"""
        return card_content
    
    def _format_distribution(self, distribution: Dict[str, int]) -> str:
        """Format distribution dictionary for markdown display"""
        lines = []
        for key, value in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (value / sum(distribution.values())) * 100
            lines.append(f"- **{key}**: {value:,} ({percentage:.1f}%)")
        return "\n".join(lines)
    
    def upload_to_hub(self, 
                     dialogues_path: str,
                     stats_path: str,
                     repo_name: str = "kenya-llm-bench-v1",
                     organization: str = "syncsenta") -> str:
        """Upload dataset to Hugging Face Hub"""
        
        # Load dialogues and statistics
        with open(dialogues_path, 'r', encoding='utf-8') as f:
            dialogues = json.load(f)
        
        with open(stats_path, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        print(f"📤 Preparing to upload {len(dialogues)} dialogues...")
        
        # Convert to SFT format
        sft_data = self.convert_to_sft_format(dialogues)
        
        # Create splits
        splits = self.create_train_val_test_splits(sft_data)
        
        # Create Hugging Face datasets
        dataset_dict = DatasetDict()
        
        for split_name, split_data in splits.items():
            dataset_dict[split_name] = Dataset.from_list(split_data)
        
        # Create repository name
        full_repo_name = f"{organization}/{repo_name}"
        
        try:
            # Create repository
            self.api.create_repo(
                repo_id=full_repo_name,
                repo_type="dataset",
                exist_ok=True,
                private=False
            )
            print(f"✅ Repository created/updated: {full_repo_name}")
            
            # Upload dataset
            dataset_dict.push_to_hub(
                repo_id=full_repo_name,
                token=self.hf_token
            )
            print(f"✅ Dataset uploaded successfully")
            
            # Create and upload dataset card
            dataset_card = self.create_dataset_card(stats)
            
            # Save dataset card locally first
            card_path = Path("README.md")
            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(dataset_card)
            
            # Upload dataset card
            self.api.upload_file(
                path_or_fileobj=str(card_path),
                path_in_repo="README.md",
                repo_id=full_repo_name,
                repo_type="dataset",
                token=self.hf_token
            )
            print(f"✅ Dataset card uploaded")
            
            # Clean up local README
            card_path.unlink()
            
            repo_url = f"https://huggingface.co/datasets/{full_repo_name}"
            print(f"🎉 Dataset successfully published at: {repo_url}")
            
            return repo_url
            
        except Exception as e:
            print(f"❌ Error uploading to Hugging Face: {e}")
            raise e

def main():
    """Example usage of the uploader"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload Kenya-LLM-Bench-v1 to Hugging Face")
    parser.add_argument("--dialogues", required=True, help="Path to dialogues JSON file")
    parser.add_argument("--stats", required=True, help="Path to statistics JSON file") 
    parser.add_argument("--token", required=True, help="Hugging Face token")
    parser.add_argument("--repo", default="kenya-llm-bench-v1", help="Repository name")
    parser.add_argument("--org", default="syncsenta", help="Organization name")
    
    args = parser.parse_args()
    
    uploader = KenyaLLMBenchUploader(args.token)
    
    repo_url = uploader.upload_to_hub(
        dialogues_path=args.dialogues,
        stats_path=args.stats,
        repo_name=args.repo,
        organization=args.org
    )
    
    print(f"✅ Upload completed: {repo_url}")

if __name__ == "__main__":
    main()