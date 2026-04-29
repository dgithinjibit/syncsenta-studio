//! Dataset processing for Kenya-LLM-Bench-v1
//! 
//! Converts our educational dialogues into training format for Llama 3.1

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::{DatasetConfig, CulturalConfig};

/// Training example for Kenya-LLM fine-tuning
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KenyaTrainingExample {
    pub system_prompt: String,
    pub user_input: String,
    pub assistant_response: String,
    pub cultural_elements: Vec<String>,
    pub pedagogical_technique: String,
    pub curriculum_alignment: CBCAlignment,
    pub cultural_weight: f64,
}

/// CBC curriculum alignment information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CBCAlignment {
    pub subject: String,
    pub grade_level: String,
    pub strand: String,
    pub sub_strand: String,
    pub learning_objective: String,
}

/// Original Kenya-LLM-Bench-v1 dialogue format
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KenyaDialogue {
    pub dialogue_id: String,
    pub grade_level: String,
    pub subject: String,
    pub curriculum_strand: String,
    pub sub_strand: String,
    pub learning_objective: String,
    pub cultural_context: String,
    pub language_mix: String,
    pub dialogue: Vec<DialogueTurn>,
    pub learning_outcome: String,
    pub difficulty_level: u8,
    pub metadata: DialogueMetadata,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogueTurn {
    pub role: String, // "student" or "tutor"
    pub content: String,
    pub timestamp: String,
    pub pedagogical_technique: Option<String>,
    pub cultural_elements: Option<Vec<String>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogueMetadata {
    pub generated_by: String,
    pub generated_at: String,
    pub reviewed: bool,
    pub cultural_authenticity_score: f64,
    pub pedagogical_effectiveness_score: f64,
}

/// Load and convert Kenya-LLM-Bench-v1 dataset
pub async fn load_kenya_dataset(config: &DatasetConfig) -> Result<Vec<KenyaTrainingExample>> {
    tracing::info!("Loading Kenya-LLM dataset from: {}", config.train_path);
    
    // Read the JSON file
    let content = tokio::fs::read_to_string(&config.train_path).await?;
    let dialogues: Vec<KenyaDialogue> = serde_json::from_str(&content)?;
    
    tracing::info!("Loaded {} dialogues, converting to training format...", dialogues.len());
    
    let mut training_examples = Vec::new();
    
    for dialogue in dialogues {
        // Convert each dialogue into training examples
        let examples = convert_dialogue_to_training_examples(&dialogue, config)?;
        training_examples.extend(examples);
    }
    
    tracing::info!("Generated {} training examples", training_examples.len());
    
    // Apply cultural weighting
    apply_cultural_weighting(&mut training_examples, config);
    
    Ok(training_examples)
}

/// Convert a single dialogue into multiple training examples
fn convert_dialogue_to_training_examples(
    dialogue: &KenyaDialogue,
    config: &DatasetConfig,
) -> Result<Vec<KenyaTrainingExample>> {
    let mut examples = Vec::new();
    
    // Build system prompt with cultural context
    let system_prompt = build_cultural_system_prompt(dialogue);
    
    // Extract tutor responses for training
    let tutor_turns: Vec<&DialogueTurn> = dialogue.dialogue
        .iter()
        .filter(|turn| turn.role == "tutor")
        .collect();
    
    let student_turns: Vec<&DialogueTurn> = dialogue.dialogue
        .iter()
        .filter(|turn| turn.role == "student")
        .collect();
    
    // Create training examples from student-tutor pairs
    for (i, student_turn) in student_turns.iter().enumerate() {
        if let Some(tutor_turn) = tutor_turns.get(i) {
            let cultural_weight = calculate_cultural_weight(tutor_turn, dialogue, config);
            
            let example = KenyaTrainingExample {
                system_prompt: system_prompt.clone(),
                user_input: student_turn.content.clone(),
                assistant_response: tutor_turn.content.clone(),
                cultural_elements: tutor_turn.cultural_elements.clone().unwrap_or_default(),
                pedagogical_technique: tutor_turn.pedagogical_technique.clone().unwrap_or_default(),
                curriculum_alignment: CBCAlignment {
                    subject: dialogue.subject.clone(),
                    grade_level: dialogue.grade_level.clone(),
                    strand: dialogue.curriculum_strand.clone(),
                    sub_strand: dialogue.sub_strand.clone(),
                    learning_objective: dialogue.learning_objective.clone(),
                },
                cultural_weight,
            };
            
            examples.push(example);
        }
    }
    
    Ok(examples)
}

/// Build culturally-aware system prompt
fn build_cultural_system_prompt(dialogue: &KenyaDialogue) -> String {
    format!(
        "You are Mwalimu AI, an authentic Kenyan educational tutor specializing in CBC curriculum. \
        You naturally code-switch between English and Swahili, use Kenyan cultural references like ugali, matatu, and local places. \
        You are helping a {} student with {} ({}). \
        Use appropriate Swahili greetings (Habari, Karibu, Pole, Asante) and reference Kenyan foods, places, and scenarios naturally. \
        Apply {} pedagogical techniques and ensure CBC curriculum alignment. \
        Be culturally authentic while maintaining educational excellence.",
        dialogue.grade_level,
        dialogue.subject,
        dialogue.curriculum_strand,
        dialogue.cultural_context.replace("_", " ")
    )
}

/// Calculate cultural weight for training example
fn calculate_cultural_weight(
    tutor_turn: &DialogueTurn,
    dialogue: &KenyaDialogue,
    config: &DatasetConfig,
) -> f64 {
    let mut weight = 1.0;
    
    // Boost examples with cultural elements
    if let Some(cultural_elements) = &tutor_turn.cultural_elements {
        if !cultural_elements.is_empty() {
            weight *= config.cultural_weight;
        }
        
        // Extra boost for Swahili elements
        for element in cultural_elements {
            if element.starts_with("swahili_") {
                weight *= 1.2;
            }
            if element.starts_with("kenyan_") {
                weight *= 1.1;
            }
        }
    }
    
    // Boost CBC-aligned examples
    if !dialogue.curriculum_strand.is_empty() {
        weight *= config.curriculum_weight;
    }
    
    // Boost high-quality examples
    weight *= dialogue.metadata.cultural_authenticity_score;
    weight *= dialogue.metadata.pedagogical_effectiveness_score;
    
    weight
}

/// Apply cultural weighting to prioritize authentic examples
fn apply_cultural_weighting(examples: &mut Vec<KenyaTrainingExample>, config: &DatasetConfig) {
    // Sort by cultural weight (highest first)
    examples.sort_by(|a, b| b.cultural_weight.partial_cmp(&a.cultural_weight).unwrap());
    
    tracing::info!(
        "Applied cultural weighting. Top example weight: {:.2}, Bottom: {:.2}",
        examples.first().map(|e| e.cultural_weight).unwrap_or(0.0),
        examples.last().map(|e| e.cultural_weight).unwrap_or(0.0)
    );
}

/// Convert training examples to tokenized format
pub fn tokenize_examples(
    examples: &[KenyaTrainingExample],
    tokenizer: &tokenizers::Tokenizer,
    max_length: usize,
) -> Result<Vec<TokenizedExample>> {
    let mut tokenized = Vec::new();
    
    for example in examples {
        // Format as conversation
        let conversation = format!(
            "<|system|>\n{}\n<|user|>\n{}\n<|assistant|>\n{}",
            example.system_prompt,
            example.user_input,
            example.assistant_response
        );
        
        // Tokenize
        let encoding = tokenizer.encode(conversation, true)
            .map_err(|e| anyhow::anyhow!("Tokenization failed: {}", e))?;
        
        let tokens = encoding.get_ids().to_vec();
        
        // Truncate if too long
        let tokens = if tokens.len() > max_length {
            tokens[..max_length].to_vec()
        } else {
            tokens
        };
        
        tokenized.push(TokenizedExample {
            input_ids: tokens,
            cultural_weight: example.cultural_weight,
            cultural_elements: example.cultural_elements.clone(),
        });
    }
    
    Ok(tokenized)
}

/// Tokenized training example
#[derive(Debug, Clone)]
pub struct TokenizedExample {
    pub input_ids: Vec<u32>,
    pub cultural_weight: f64,
    pub cultural_elements: Vec<String>,
}

/// Dataset statistics for monitoring
#[derive(Debug, Serialize)]
pub struct DatasetStats {
    pub total_examples: usize,
    pub avg_cultural_weight: f64,
    pub subject_distribution: HashMap<String, usize>,
    pub grade_distribution: HashMap<String, usize>,
    pub cultural_element_count: HashMap<String, usize>,
    pub pedagogical_technique_count: HashMap<String, usize>,
}

/// Calculate dataset statistics
pub fn calculate_dataset_stats(examples: &[KenyaTrainingExample]) -> DatasetStats {
    let mut subject_dist = HashMap::new();
    let mut grade_dist = HashMap::new();
    let mut cultural_count = HashMap::new();
    let mut technique_count = HashMap::new();
    let mut total_weight = 0.0;
    
    for example in examples {
        // Subject distribution
        *subject_dist.entry(example.curriculum_alignment.subject.clone()).or_insert(0) += 1;
        
        // Grade distribution
        *grade_dist.entry(example.curriculum_alignment.grade_level.clone()).or_insert(0) += 1;
        
        // Cultural elements
        for element in &example.cultural_elements {
            *cultural_count.entry(element.clone()).or_insert(0) += 1;
        }
        
        // Pedagogical techniques
        if !example.pedagogical_technique.is_empty() {
            *technique_count.entry(example.pedagogical_technique.clone()).or_insert(0) += 1;
        }
        
        total_weight += example.cultural_weight;
    }
    
    DatasetStats {
        total_examples: examples.len(),
        avg_cultural_weight: total_weight / examples.len() as f64,
        subject_distribution: subject_dist,
        grade_distribution: grade_dist,
        cultural_element_count: cultural_count,
        pedagogical_technique_count: technique_count,
    }
}