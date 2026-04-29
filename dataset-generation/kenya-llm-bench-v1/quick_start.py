#!/usr/bin/env python3
"""
Quick Start Demo for Kenya-LLM-Bench-v1 Dataset Generation

This script demonstrates the dataset generation capabilities and creates
a small sample dataset for testing and validation.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from dialogue_generator import KenyaDialogueGenerator

def main():
    print("🇰🇪 Kenya-LLM-Bench-v1 Quick Start Demo")
    print("=" * 50)
    
    # Initialize generator
    try:
        generator = KenyaDialogueGenerator(
            curriculum_path="data/cbc_curriculum.json",
            cultural_path="data/cultural_elements.json"
        )
        print("✅ Generator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return 1
    
    # Generate sample dialogues for different grades and subjects
    sample_configs = [
        ("PP1", "Mathematics"),
        ("Grade1", "English"), 
        ("Grade3", "Mathematics"),
        ("Grade5", "Kiswahili"),
        ("Grade7", "Mathematics")
    ]
    
    print(f"\n📝 Generating {len(sample_configs)} sample dialogues...")
    
    sample_dialogues = []
    
    for i, (grade, subject) in enumerate(sample_configs, 1):
        try:
            print(f"   {i}. {grade} {subject}...")
            dialogue = generator.generate_dialogue(grade, subject)
            sample_dialogues.append(dialogue)
            print(f"      ✅ Generated dialogue: {dialogue.dialogue_id}")
        except Exception as e:
            print(f"      ❌ Error: {e}")
            continue
    
    # Display sample dialogue
    if sample_dialogues:
        print(f"\n🎯 Sample Dialogue Preview:")
        print("=" * 50)
        
        sample = sample_dialogues[0]
        print(f"Grade: {sample.grade_level}")
        print(f"Subject: {sample.subject}")
        print(f"Strand: {sample.curriculum_strand} > {sample.sub_strand}")
        print(f"Objective: {sample.learning_objective}")
        print(f"Cultural Context: {sample.cultural_context}")
        print(f"Difficulty: {sample.difficulty_level}/8")
        print()
        
        for i, turn in enumerate(sample.dialogue, 1):
            role_emoji = "👨‍🎓" if turn.role == "student" else "👩‍🏫"
            print(f"{i}. {role_emoji} {turn.role.title()}: {turn.content}")
            if turn.pedagogical_technique:
                print(f"   📚 Technique: {turn.pedagogical_technique}")
            if turn.cultural_elements:
                print(f"   🇰🇪 Cultural: {', '.join(turn.cultural_elements)}")
            print()
    
    # Save sample dataset
    output_dir = Path("data/samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sample_file = output_dir / "sample_dialogues.json"
    generator.save_dialogues(sample_dialogues, str(sample_file))
    
    print(f"💾 Sample dialogues saved to: {sample_file}")
    
    # Generate statistics
    from scripts.generate_dataset import generate_statistics
    stats = generate_statistics(sample_dialogues)
    
    stats_file = output_dir / "sample_statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Statistics saved to: {stats_file}")
    
    # Display key statistics
    print(f"\n📈 Quick Statistics:")
    print(f"   Total dialogues: {stats['total_dialogues']}")
    print(f"   Average length: {stats['average_dialogue_length']:.1f} turns")
    print(f"   Grade levels: {len(stats['grade_distribution'])}")
    print(f"   Subjects: {len(stats['subject_distribution'])}")
    print(f"   Cultural contexts: {len(stats['cultural_context_distribution'])}")
    
    print(f"\n🎉 Quick start demo completed successfully!")
    print(f"\n📋 Next Steps:")
    print(f"   1. Review sample dialogues in {sample_file}")
    print(f"   2. Generate full dataset: python scripts/generate_dataset.py --target-size 1000")
    print(f"   3. Upload to Hugging Face: python scripts/upload_to_hf.py --token $HF_TOKEN")
    
    return 0

if __name__ == "__main__":
    exit(main())