#!/usr/bin/env python3
"""
Quick Start Script for Kenya-LLM-Bench Dataset Creation
Run this to begin building your CBC curriculum dataset immediately.
"""

import os
import json
import requests
from pathlib import Path

def setup_environment():
    """Set up the working environment"""
    print("🚀 Setting up Kenya-LLM-Bench environment...")
    
    # Create directories
    directories = ["kicd_pdfs", "extracted_data", "synthetic_dialogues", "datasets"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    print("\n📦 Install required packages with:")
    print("pip install PyPDF2 pandas transformers datasets chromadb sentence-transformers scikit-learn requests beautifulsoup4")
    
    return True

def create_sample_curriculum_data():
    """Create sample curriculum data to get started"""
    print("\n📚 Creating sample CBC curriculum data...")
    
    sample_data = {
        "mathematics_grade_4": {
            "subject": "Mathematics",
            "grade": "Grade 4",
            "strands": [
                "Number Operations",
                "Measurement", 
                "Geometry",
                "Data Handling"
            ],
            "learning_outcomes": [
                "Identify and represent fractions using concrete materials and visual models",
                "Add and subtract fractions with like denominators",
                "Compare and order fractions using visual models",
                "Solve word problems involving fractions in real-life contexts",
                "Measure length using standard units (meters, centimeters)",
                "Calculate perimeter of regular and irregular shapes",
                "Identify and classify 2D and 3D shapes in the environment",
                "Collect, organize and present data using tables and charts"
            ]
        },
        "science_grade_5": {
            "subject": "Science",
            "grade": "Grade 5", 
            "strands": [
                "Living Things and Their Environment",
                "Materials and Their Properties",
                "Energy and Changes"
            ],
            "learning_outcomes": [
                "Classify plants based on their characteristics and habitat",
                "Explain the process of photosynthesis in simple terms",
                "Identify different types of soil and their properties",
                "Describe the water cycle and its importance",
                "Investigate properties of materials (hardness, flexibility, transparency)",
                "Explain how sound is produced and travels",
                "Demonstrate understanding of simple machines and their uses"
            ]
        }
    }
    
    # Save sample data
    with open("extracted_data/sample_cbc_curriculum.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    
    print("✅ Sample curriculum data created in extracted_data/sample_cbc_curriculum.json")
    return sample_data

def create_sample_dialogue():
    """Create a sample Socratic dialogue to demonstrate the format"""
    print("\n💬 Creating sample Socratic dialogue...")
    
    sample_dialogue = {
        "input": "Teach fractions to a Grade 4 student using Kenyan context",
        "context": "CBC Mathematics Grade 4 - Number Operations Strand",
        "output": """Teacher: Habari Amina! Today we're learning about sehemu (fractions). If mama gives you one chapati and asks you to share it equally with your brother, how would you do it?

Student: I would cut it into two pieces, teacher.

Teacher: Vizuri sana! Each piece would be what part of the whole chapati?

Student: Mmm... half?

Teacher: Exactly! In mathematics, we write half as 1/2. The bottom number (2) shows how many equal parts we divided the chapati into. What do you think the top number (1) shows?

Student: The number of pieces I have?

Teacher: Perfect! You're understanding well. Now, if you had 3 pieces out of 4 equal pieces of ugali, how would you write that fraction?

Student: Would it be 3/4?

Teacher: Excellent! You see how fractions help us describe parts of things we use every day - chapati, ugali, even pieces of sukuma wiki. Can you think of another example from home?

Student: When we share mandazi among 5 people, each person gets 1/5?

Teacher: Wonderful! You're becoming a fraction expert. Now let's practice with some more examples...""",
        "metadata": {
            "subject": "Mathematics",
            "grade": "Grade 4",
            "strand": "Number Operations", 
            "sub_strand": "Fractions",
            "learning_outcome": "Identify and represent fractions using concrete materials and visual models",
            "cultural_context": ["chapati", "ugali", "sukuma wiki", "mandazi"],
            "pedagogical_approach": "Socratic method",
            "language_mix": "English-Swahili",
            "kenyan_elements": ["Swahili greetings", "local foods", "cultural sharing practices"]
        }
    }
    
    # Save sample dialogue
    with open("synthetic_dialogues/sample_dialogue.json", "w") as f:
        json.dump(sample_dialogue, f, indent=2)
    
    print("✅ Sample dialogue created in synthetic_dialogues/sample_dialogue.json")
    return sample_dialogue

def create_huggingface_dataset_template():
    """Create template for Hugging Face dataset upload"""
    print("\n🤗 Creating Hugging Face dataset template...")
    
    dataset_template = {
        "dataset_name": "Kenya-LLM-Bench-v1",
        "description": "Curriculum-Aligned Synthetic Dataset for Kenyan CBC education",
        "license": "cc-by-4.0",
        "language": ["en", "sw"],
        "tags": ["education", "kenya", "cbc", "curriculum", "socratic-tutoring"],
        "task_categories": ["conversational", "text-generation"],
        "size_categories": "1K<n<10K",
        "format": "SFT (Supervised Fine-Tuning)",
        "features": {
            "input": "string - The learning objective or question",
            "context": "string - CBC curriculum context", 
            "output": "string - Socratic tutoring dialogue",
            "metadata": "dict - Subject, grade, strand, cultural context"
        },
        "sample_count": {
            "target": 10000,
            "current": 1,
            "per_subject": {
                "Mathematics": 2500,
                "Science": 2500, 
                "English": 2000,
                "Kiswahili": 2000,
                "Social Studies": 1000
            }
        }
    }
    
    with open("datasets/huggingface_template.json", "w") as f:
        json.dump(dataset_template, f, indent=2)
    
    print("✅ Hugging Face template created in datasets/huggingface_template.json")
    return dataset_template

def show_next_steps():
    """Show the user what to do next"""
    print("\n🎯 Next Steps:")
    print("1. Install the required packages:")
    print("   pip install PyPDF2 pandas transformers datasets chromadb sentence-transformers")
    print("\n2. Download KICD curriculum PDFs:")
    print("   - Visit https://kicd.ac.ke")
    print("   - Download CBC curriculum documents")
    print("   - Place PDFs in the kicd_pdfs/ directory")
    print("\n3. Run the curriculum extractor:")
    print("   python curriculum_extractor.py")
    print("\n4. Generate synthetic dialogues:")
    print("   python dialogue_generator.py")
    print("\n5. Upload to Hugging Face:")
    print("   - Create account at https://huggingface.co")
    print("   - Use datasets library to upload your Kenya-LLM-Bench")
    
    print("\n🏆 Goal: Create the first CBC-aligned dataset on Hugging Face!")
    print("📈 Impact: Own the African EdTech data infrastructure!")

def main():
    """Main function to set up everything"""
    print("🇰🇪 Kenya-LLM-Bench Dataset Creator")
    print("=" * 50)
    
    # Set up environment
    setup_environment()
    
    # Create sample data
    curriculum_data = create_sample_curriculum_data()
    sample_dialogue = create_sample_dialogue()
    dataset_template = create_huggingface_dataset_template()
    
    # Show next steps
    show_next_steps()
    
    print("\n✨ Setup complete! You're ready to build the Kenya-LLM-Bench dataset.")
    print("💡 Remember: You're not just building a dataset, you're building the foundation of African EdTech!")

if __name__ == "__main__":
    main()