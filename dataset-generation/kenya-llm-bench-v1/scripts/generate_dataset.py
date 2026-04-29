#!/usr/bin/env python3
"""
Main script to generate the Kenya-LLM-Bench-v1 dataset

Usage:
    python scripts/generate_dataset.py --target-size 1000 --output data/generated_dialogues/
"""

import argparse
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from dialogue_generator import KenyaDialogueGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate Kenya-LLM-Bench-v1 dataset")
    parser.add_argument("--target-size", type=int, default=1000, 
                       help="Number of dialogues to generate")
    parser.add_argument("--output", type=str, default="data/generated_dialogues/",
                       help="Output directory for generated dialogues")
    parser.add_argument("--curriculum", type=str, default="data/cbc_curriculum.json",
                       help="Path to CBC curriculum file")
    parser.add_argument("--cultural", type=str, default="data/cultural_elements.json",
                       help="Path to cultural elements file")
    parser.add_argument("--batch-size", type=int, default=100,
                       help="Number of dialogues to generate per batch")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🇰🇪 Kenya-LLM-Bench-v1 Dataset Generation Starting...")
    print(f"Target size: {args.target_size} dialogues")
    print(f"Output directory: {output_dir}")
    
    # Initialize generator
    try:
        generator = KenyaDialogueGenerator(
            curriculum_path=args.curriculum,
            cultural_path=args.cultural
        )
        print("✅ Generator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return 1
    
    # Generate dialogues in batches
    all_dialogues = []
    batches = (args.target_size + args.batch_size - 1) // args.batch_size
    
    for batch_num in range(batches):
        batch_start = batch_num * args.batch_size
        batch_end = min((batch_num + 1) * args.batch_size, args.target_size)
        batch_size = batch_end - batch_start
        
        print(f"\n📝 Generating batch {batch_num + 1}/{batches} ({batch_size} dialogues)...")
        
        try:
            batch_dialogues = generator.generate_dataset(batch_size)
            all_dialogues.extend(batch_dialogues)
            
            # Save batch file
            batch_file = output_dir / f"batch_{batch_num + 1:03d}.json"
            generator.save_dialogues(batch_dialogues, str(batch_file))
            
            print(f"✅ Batch {batch_num + 1} completed: {len(batch_dialogues)} dialogues")
            
        except Exception as e:
            print(f"❌ Error in batch {batch_num + 1}: {e}")
            continue
    
    # Save complete dataset
    complete_file = output_dir / "kenya_llm_bench_v1_complete.json"
    generator.save_dialogues(all_dialogues, str(complete_file))
    
    # Generate statistics
    stats = generate_statistics(all_dialogues)
    stats_file = output_dir / "dataset_statistics.json"
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Dataset generation completed!")
    print(f"📊 Total dialogues: {len(all_dialogues)}")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📈 Statistics saved to: {stats_file}")
    
    # Print summary statistics
    print("\n📊 Dataset Summary:")
    print(f"   Grade levels: {len(stats['grade_distribution'])}")
    print(f"   Subjects: {len(stats['subject_distribution'])}")
    print(f"   Cultural contexts: {len(stats['cultural_context_distribution'])}")
    print(f"   Average dialogue length: {stats['average_dialogue_length']:.1f} turns")
    
    return 0

def generate_statistics(dialogues):
    """Generate comprehensive statistics about the dataset"""
    stats = {
        "total_dialogues": len(dialogues),
        "generation_timestamp": dialogues[0].metadata["generated_at"] if dialogues else None,
        "grade_distribution": {},
        "subject_distribution": {},
        "cultural_context_distribution": {},
        "difficulty_distribution": {},
        "dialogue_lengths": [],
        "average_dialogue_length": 0,
        "cultural_elements_frequency": {},
        "pedagogical_techniques_frequency": {}
    }
    
    for dialogue in dialogues:
        # Grade distribution
        grade = dialogue.grade_level
        stats["grade_distribution"][grade] = stats["grade_distribution"].get(grade, 0) + 1
        
        # Subject distribution
        subject = dialogue.subject
        stats["subject_distribution"][subject] = stats["subject_distribution"].get(subject, 0) + 1
        
        # Cultural context distribution
        context = dialogue.cultural_context
        stats["cultural_context_distribution"][context] = stats["cultural_context_distribution"].get(context, 0) + 1
        
        # Difficulty distribution
        difficulty = dialogue.difficulty_level
        stats["difficulty_distribution"][difficulty] = stats["difficulty_distribution"].get(difficulty, 0) + 1
        
        # Dialogue length
        length = len(dialogue.dialogue)
        stats["dialogue_lengths"].append(length)
        
        # Cultural elements frequency
        for turn in dialogue.dialogue:
            if turn.cultural_elements:
                for element in turn.cultural_elements:
                    stats["cultural_elements_frequency"][element] = stats["cultural_elements_frequency"].get(element, 0) + 1
        
        # Pedagogical techniques frequency
        for turn in dialogue.dialogue:
            if turn.pedagogical_technique:
                technique = turn.pedagogical_technique
                stats["pedagogical_techniques_frequency"][technique] = stats["pedagogical_techniques_frequency"].get(technique, 0) + 1
    
    # Calculate average dialogue length
    if stats["dialogue_lengths"]:
        stats["average_dialogue_length"] = sum(stats["dialogue_lengths"]) / len(stats["dialogue_lengths"])
    
    return stats

if __name__ == "__main__":
    exit(main())