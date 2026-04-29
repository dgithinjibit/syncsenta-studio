#!/usr/bin/env python3
"""
Upload Kenya-LLM-Bench-v1 dataset to Hugging Face Hub

Usage:
    python scripts/upload_to_hf.py --token $HF_TOKEN --dialogues data/generated_dialogues/kenya_llm_bench_v1_complete.json
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from hf_uploader import KenyaLLMBenchUploader

def main():
    parser = argparse.ArgumentParser(description="Upload Kenya-LLM-Bench-v1 to Hugging Face Hub")
    parser.add_argument("--token", required=True, 
                       help="Hugging Face fine-grained token with write access")
    parser.add_argument("--dialogues", required=True,
                       help="Path to generated dialogues JSON file")
    parser.add_argument("--stats", 
                       help="Path to dataset statistics JSON file (auto-detected if not provided)")
    parser.add_argument("--repo", default="kenya-llm-bench-v1",
                       help="Repository name on Hugging Face")
    parser.add_argument("--org", default="syncsenta", 
                       help="Organization name on Hugging Face")
    parser.add_argument("--dry-run", action="store_true",
                       help="Prepare dataset but don't upload")
    
    args = parser.parse_args()
    
    # Validate inputs
    dialogues_path = Path(args.dialogues)
    if not dialogues_path.exists():
        print(f"❌ Dialogues file not found: {dialogues_path}")
        return 1
    
    # Auto-detect stats file if not provided
    if args.stats:
        stats_path = Path(args.stats)
    else:
        stats_path = dialogues_path.parent / "dataset_statistics.json"
    
    if not stats_path.exists():
        print(f"❌ Statistics file not found: {stats_path}")
        print("   Generate statistics first or provide --stats argument")
        return 1
    
    print("🇰🇪 Kenya-LLM-Bench-v1 Hugging Face Upload")
    print(f"📁 Dialogues: {dialogues_path}")
    print(f"📊 Statistics: {stats_path}")
    print(f"🏢 Repository: {args.org}/{args.repo}")
    
    if args.dry_run:
        print("🧪 DRY RUN MODE - No actual upload will occur")
    
    try:
        # Initialize uploader
        if args.dry_run:
            print("🧪 DRY RUN MODE - Simulating uploader initialization")
            print("✅ Would initialize uploader with provided token")
        else:
            uploader = KenyaLLMBenchUploader(args.token)
        
        if args.dry_run:
            print("✅ Uploader initialized successfully (dry run)")
            print("   Would upload to Hugging Face Hub in real run")
            
            # Show what would be uploaded
            import json
            with open(dialogues_path, 'r', encoding='utf-8') as f:
                dialogues = json.load(f)
            
            print(f"\n📊 Dataset Preview (would upload {len(dialogues)} dialogues):")
            print(f"   Sample dialogue ID: {dialogues[0]['dialogue_id']}")
            print(f"   Grade levels: {set(d['grade_level'] for d in dialogues[:10])}")
            print(f"   Subjects: {set(d['subject'] for d in dialogues[:10])}")
            print(f"   Cultural contexts: {set(d['cultural_context'] for d in dialogues[:10])}")
            
            return 0
        
        # Upload to Hugging Face
        repo_url = uploader.upload_to_hub(
            dialogues_path=str(dialogues_path),
            stats_path=str(stats_path),
            repo_name=args.repo,
            organization=args.org
        )
        
        print(f"\n🎉 SUCCESS! Dataset published at:")
        print(f"   {repo_url}")
        print(f"\n📋 Next steps:")
        print(f"   1. Review the dataset card and metadata")
        print(f"   2. Test loading with: datasets.load_dataset('{args.org}/{args.repo}')")
        print(f"   3. Share with the community!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())