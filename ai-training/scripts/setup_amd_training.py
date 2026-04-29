#!/usr/bin/env python3
"""
SyncSenta CBC Model Training Setup for AMD MI300X
Fine-tune Llama 3.1 8B on Kenyan CBC curriculum data
"""

import os
import sys
from pathlib import Path
import subprocess
import json

def check_environment():
    """Verify all required environment variables and dependencies"""
    required_vars = [
        'AMD_API_KEY',
        'AMD_PROJECT_ID', 
        'HF_TOKEN',
        'AISA_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("Please add them to your .env file")
        return False
    
    print("✅ All environment variables configured")
    return True

def setup_amd_instance():
    """Launch AMD MI300X instance for training"""
    print("🚀 Setting up AMD MI300X instance...")
    
    # AMD instance configuration
    config = {
        "instance_type": "mi300x",
        "region": os.getenv("AMD_REGION", "us-east-1"),
        "image": "rocm-pytorch-7.0",
        "storage": "100GB",
        "project_id": os.getenv("AMD_PROJECT_ID")
    }
    
    print(f"Instance config: {json.dumps(config, indent=2)}")
    
    # TODO: Implement AMD API calls to launch instance
    # For now, print instructions
    print("""
    Manual steps to launch AMD instance:
    1. Go to AMD Developer Cloud portal
    2. Create new instance with:
       - Type: MI300X
       - OS: Ubuntu 22.04 + ROCm 7
       - Storage: 100GB SSD
       - Project: SyncSenta-AI-Training
    3. Note the instance IP and SSH key
    4. Update .env with AMD_INSTANCE_IP and AMD_SSH_KEY_PATH
    """)

def prepare_cbc_dataset():
    """Prepare CBC curriculum dataset for training"""
    print("📚 Preparing CBC curriculum dataset...")
    
    # Check if scheme-scribe-ai data exists
    scheme_data_path = Path("../repos/scheme-scribe-ai/src/data/curriculum")
    if not scheme_data_path.exists():
        print(f"❌ CBC curriculum data not found at {scheme_data_path}")
        print("Please ensure scheme-scribe-ai repo is available")
        return False
    
    print(f"✅ Found CBC curriculum data at {scheme_data_path}")
    
    # Create training dataset structure
    dataset_dir = Path("ai-training/datasets/cbc-curriculum")
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created dataset directory: {dataset_dir}")
    return True

def install_dependencies():
    """Install required Python packages for training"""
    print("📦 Installing training dependencies...")
    
    requirements = [
        "torch>=2.0.0",
        "transformers>=4.35.0", 
        "datasets>=2.14.0",
        "accelerate>=0.24.0",
        "peft>=0.6.0",  # For LoRA fine-tuning
        "bitsandbytes>=0.41.0",  # For quantization
        "huggingface_hub>=0.17.0",
        "wandb>=0.15.0",  # For experiment tracking
        "amd-smi>=0.1.0"  # AMD GPU monitoring
    ]
    
    for package in requirements:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_training_config():
    """Create training configuration for CBC fine-tuning"""
    config = {
        "model_name": "meta-llama/Llama-3.1-8B",
        "dataset_name": "cbc-curriculum-v1",
        "output_dir": "./models/mwalimu-cbc-8b",
        "training_args": {
            "per_device_train_batch_size": 4,
            "per_device_eval_batch_size": 4,
            "gradient_accumulation_steps": 4,
            "num_train_epochs": 3,
            "learning_rate": 2e-5,
            "warmup_steps": 100,
            "logging_steps": 10,
            "save_steps": 500,
            "eval_steps": 500,
            "max_seq_length": 2048,
            "fp16": True,
            "dataloader_num_workers": 4
        },
        "lora_config": {
            "r": 16,
            "lora_alpha": 32,
            "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
            "lora_dropout": 0.1,
            "bias": "none",
            "task_type": "CAUSAL_LM"
        },
        "system_prompt": """You are Mwalimu, an AI assistant specialized in Kenya's Competency-Based Curriculum (CBC). 
You help students, teachers, and parents with CBC-aligned educational content in English, Kiswahili, and local languages.
Always provide accurate, culturally relevant responses that align with KICD standards."""
    }
    
    config_path = Path("ai-training/config/cbc_training_config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Training config saved to {config_path}")
    return config_path

def main():
    """Main setup function"""
    print("🌱 SyncSenta CBC Model Training Setup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Prepare dataset
    if not prepare_cbc_dataset():
        print("❌ Failed to prepare CBC dataset")
        sys.exit(1)
    
    # Create training config
    config_path = create_training_config()
    
    # Setup AMD instance
    setup_amd_instance()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Launch AMD MI300X instance manually")
    print("2. Update .env with instance details")
    print("3. Run: python ai-training/scripts/train_cbc_model.py")
    print(f"4. Training config: {config_path}")

if __name__ == "__main__":
    main()