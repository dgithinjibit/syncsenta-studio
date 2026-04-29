#!/usr/bin/env python3
"""
SyncSenta CBC Model Training on AMD MI300X
Fine-tune Llama 3.1 8B for Kenyan education context
"""

import os
import json
import torch
from pathlib import Path
from datetime import datetime
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset, load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import wandb

class CBCDatasetProcessor:
    """Process CBC curriculum data for training"""
    
    def __init__(self, tokenizer, max_length=2048):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.system_prompt = """You are Mwalimu, an AI assistant specialized in Kenya's Competency-Based Curriculum (CBC). 
You help students, teachers, and parents with CBC-aligned educational content in English, Kiswahili, and local languages.
Always provide accurate, culturally relevant responses that align with KICD standards."""
    
    def load_cbc_data(self):
        """Load and process CBC curriculum data"""
        print("📚 Loading CBC curriculum data...")
        
        # Load from scheme-scribe-ai curriculum data
        curriculum_path = Path("../repos/scheme-scribe-ai/src/data/curriculum")
        
        training_examples = []
        
        # Process curriculum files
        for grade_dir in curriculum_path.glob("grade_*"):
            if grade_dir.is_dir():
                print(f"Processing {grade_dir.name}...")
                
                for subject_file in grade_dir.glob("*.json"):
                    try:
                        with open(subject_file, 'r', encoding='utf-8') as f:
                            subject_data = json.load(f)
                        
                        # Convert curriculum data to training examples
                        examples = self.create_training_examples(subject_data, grade_dir.name)
                        training_examples.extend(examples)
                        
                    except Exception as e:
                        print(f"Error processing {subject_file}: {e}")
        
        print(f"✅ Created {len(training_examples)} training examples")
        return Dataset.from_list(training_examples)
    
    def create_training_examples(self, subject_data, grade):
        """Convert curriculum data to training examples"""
        examples = []
        
        # Extract subject info
        subject_name = subject_data.get('subject', 'Unknown')
        
        # Process learning areas/strands
        for strand in subject_data.get('strands', []):
            strand_name = strand.get('name', '')
            
            # Process sub-strands
            for sub_strand in strand.get('sub_strands', []):
                sub_strand_name = sub_strand.get('name', '')
                
                # Process specific learning outcomes
                for outcome in sub_strand.get('learning_outcomes', []):
                    # Create Q&A pairs for each learning outcome
                    examples.extend(self.create_qa_pairs(
                        grade, subject_name, strand_name, 
                        sub_strand_name, outcome
                    ))
        
        return examples
    
    def create_qa_pairs(self, grade, subject, strand, sub_strand, outcome):
        """Create question-answer pairs from learning outcomes"""
        examples = []
        
        # Basic explanation
        question = f"Explain the {subject} concept: {outcome.get('description', '')}"
        answer = f"In {grade} {subject}, under {strand} - {sub_strand}: {outcome.get('explanation', outcome.get('description', ''))}"
        
        examples.append({
            'input': question,
            'output': answer,
            'grade': grade,
            'subject': subject,
            'strand': strand
        })
        
        # Assessment question
        if 'assessment_criteria' in outcome:
            question = f"How would you assess a {grade} student's understanding of {outcome.get('description', '')}?"
            answer = f"Assessment criteria: {outcome['assessment_criteria']}"
            
            examples.append({
                'input': question,
                'output': answer,
                'grade': grade,
                'subject': subject,
                'strand': strand
            })
        
        # Teaching suggestion
        question = f"How should I teach {outcome.get('description', '')} to {grade} students?"
        answer = f"Teaching approach for {grade} {subject}: Focus on {outcome.get('teaching_notes', 'hands-on activities and real-world examples relevant to Kenyan context')}"
        
        examples.append({
            'input': question,
            'output': answer,
            'grade': grade,
            'subject': subject,
            'strand': strand
        })
        
        return examples
    
    def format_example(self, example):
        """Format example for training"""
        conversation = f"""<|system|>
{self.system_prompt}

<|user|>
{example['input']}

<|assistant|>
{example['output']}"""
        
        return conversation
    
    def tokenize_function(self, examples):
        """Tokenize examples for training"""
        # Format conversations
        texts = [self.format_example(ex) for ex in examples]
        
        # Tokenize
        tokenized = self.tokenizer(
            texts,
            truncation=True,
            padding=False,
            max_length=self.max_length,
            return_overflowing_tokens=False,
        )
        
        # Set labels for language modeling
        tokenized["labels"] = tokenized["input_ids"].copy()
        
        return tokenized

def setup_model_and_tokenizer(model_name):
    """Setup model and tokenizer with LoRA"""
    print(f"🤖 Loading model: {model_name}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with quantization for memory efficiency
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_8bit=True,  # Use 8-bit quantization
        trust_remote_code=True
    )
    
    # Setup LoRA configuration
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def main():
    """Main training function"""
    print("🚀 Starting SyncSenta CBC Model Training")
    print("=" * 50)
    
    # Load training configuration
    config_path = Path("ai-training/config/cbc_training_config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Initialize Weights & Biases
    wandb.init(
        project="syncsenta-cbc-training",
        name=f"mwalimu-cbc-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        config=config
    )
    
    # Setup model and tokenizer
    model, tokenizer = setup_model_and_tokenizer(config["model_name"])
    
    # Process dataset
    processor = CBCDatasetProcessor(tokenizer)
    dataset = processor.load_cbc_data()
    
    # Split dataset
    train_test = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = train_test['train']
    eval_dataset = train_test['test']
    
    # Tokenize datasets
    print("🔤 Tokenizing datasets...")
    train_dataset = train_dataset.map(
        processor.tokenize_function,
        batched=True,
        remove_columns=train_dataset.column_names
    )
    eval_dataset = eval_dataset.map(
        processor.tokenize_function,
        batched=True,
        remove_columns=eval_dataset.column_names
    )
    
    # Setup training arguments
    training_args = TrainingArguments(
        output_dir=config["output_dir"],
        per_device_train_batch_size=config["training_args"]["per_device_train_batch_size"],
        per_device_eval_batch_size=config["training_args"]["per_device_eval_batch_size"],
        gradient_accumulation_steps=config["training_args"]["gradient_accumulation_steps"],
        num_train_epochs=config["training_args"]["num_train_epochs"],
        learning_rate=config["training_args"]["learning_rate"],
        warmup_steps=config["training_args"]["warmup_steps"],
        logging_steps=config["training_args"]["logging_steps"],
        save_steps=config["training_args"]["save_steps"],
        eval_steps=config["training_args"]["eval_steps"],
        fp16=config["training_args"]["fp16"],
        dataloader_num_workers=config["training_args"]["dataloader_num_workers"],
        remove_unused_columns=False,
        report_to="wandb",
        run_name=f"mwalimu-cbc-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        evaluation_strategy="steps",
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # Start training
    print("🎯 Starting training...")
    trainer.train()
    
    # Save final model
    print("💾 Saving final model...")
    trainer.save_model()
    tokenizer.save_pretrained(config["output_dir"])
    
    # Upload to Hugging Face Hub
    if os.getenv("HF_TOKEN"):
        print("📤 Uploading to Hugging Face Hub...")
        model.push_to_hub(
            "syncsenta/mwalimu-cbc-8b",
            token=os.getenv("HF_TOKEN"),
            private=False
        )
        tokenizer.push_to_hub(
            "syncsenta/mwalimu-cbc-8b",
            token=os.getenv("HF_TOKEN"),
            private=False
        )
    
    print("🎉 Training complete!")
    wandb.finish()

if __name__ == "__main__":
    main()