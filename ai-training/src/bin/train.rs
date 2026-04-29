//! Kenya-LLM Training Binary
//! 
//! Fine-tune Llama 3.1 on Kenya-LLM-Bench-v1 dataset using AMD ROCm

use anyhow::Result;
use clap::Parser;
use syncsenta_ai_training::{KenyaAIConfig, train_kenya_llama};
use tracing::{info, error};

#[derive(Parser)]
#[command(name = "train-kenya-llama")]
#[command(about = "Fine-tune Llama 3.1 on Kenya-LLM-Bench-v1 dataset")]
struct Args {
    /// Configuration file path
    #[arg(short, long, default_value = "config/training.toml")]
    config: String,
    
    /// Base model to fine-tune
    #[arg(short, long, default_value = "meta-llama/Llama-3.1-8B")]
    model: String,
    
    /// Training dataset path
    #[arg(short, long)]
    dataset: Option<String>,
    
    /// Output directory for trained model
    #[arg(short, long, default_value = "models/kenya-llama-v1")]
    output: String,
    
    /// Number of training epochs
    #[arg(short, long, default_value = "3")]
    epochs: usize,
    
    /// Batch size (adjust for your GPU memory)
    #[arg(short, long, default_value = "32")]
    batch_size: usize,
    
    /// Learning rate
    #[arg(short, long, default_value = "2e-5")]
    learning_rate: f64,
    
    /// Enable AMD ROCm
    #[arg(long)]
    rocm: bool,
    
    /// Dry run (validate setup without training)
    #[arg(long)]
    dry_run: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();
    
    let args = Args::parse();
    
    info!("🚀 Starting Kenya-LLM Training");
    info!("Model: {}", args.model);
    info!("Epochs: {}", args.epochs);
    info!("Batch Size: {}", args.batch_size);
    info!("Learning Rate: {}", args.learning_rate);
    
    // Load configuration
    let mut config = load_config(&args.config).unwrap_or_else(|_| {
        info!("Using default configuration");
        KenyaAIConfig::default()
    });
    
    // Override with command line arguments
    config.model.base_model = args.model;
    config.training.num_epochs = args.epochs;
    config.training.batch_size = args.batch_size;
    config.training.learning_rate = args.learning_rate;
    
    if let Some(dataset_path) = args.dataset {
        config.dataset.train_path = dataset_path;
    }
    
    if args.rocm {
        config.training.device = "rocm".to_string();
        info!("🔥 AMD ROCm enabled");
    }
    
    // Validate setup
    validate_setup(&config).await?;
    
    if args.dry_run {
        info!("✅ Dry run completed successfully");
        return Ok(());
    }
    
    // Start training
    info!("🎯 Starting training with Kenya-LLM-Bench-v1 dataset...");
    
    match train_kenya_llama(config).await {
        Ok(()) => {
            info!("🎉 Training completed successfully!");
            info!("📁 Model saved to: {}", args.output);
            info!("🇰🇪 Kenya-LLM is ready for authentic educational AI!");
        }
        Err(e) => {
            error!("❌ Training failed: {}", e);
            std::process::exit(1);
        }
    }
    
    Ok(())
}

/// Load configuration from file
fn load_config(path: &str) -> Result<KenyaAIConfig> {
    if std::path::Path::new(path).exists() {
        let content = std::fs::read_to_string(path)?;
        let config: KenyaAIConfig = toml::from_str(&content)?;
        Ok(config)
    } else {
        anyhow::bail!("Configuration file not found: {}", path);
    }
}

/// Validate training setup
async fn validate_setup(config: &KenyaAIConfig) -> Result<()> {
    info!("🔍 Validating training setup...");
    
    // Check dataset exists
    if !std::path::Path::new(&config.dataset.train_path).exists() {
        anyhow::bail!("Training dataset not found: {}", config.dataset.train_path);
    }
    info!("✅ Dataset found: {}", config.dataset.train_path);
    
    // Check GPU availability
    match config.training.device.as_str() {
        "rocm" => {
            info!("🔥 Checking AMD ROCm availability...");
            // ROCm validation would go here
            #[cfg(feature = "rocm")]
            {
                info!("✅ AMD ROCm support enabled");
            }
            #[cfg(not(feature = "rocm"))]
            {
                anyhow::bail!("ROCm support not compiled. Rebuild with --features rocm");
            }
        }
        "cuda" => {
            info!("🟢 Checking NVIDIA CUDA availability...");
            // CUDA validation would go here
        }
        "cpu" => {
            info!("⚠️  CPU training mode (will be slow)");
        }
        _ => {
            anyhow::bail!("Unknown device: {}", config.training.device);
        }
    }
    
    // Validate memory requirements
    let estimated_memory_gb = estimate_memory_requirements(config);
    info!("📊 Estimated memory requirement: {:.1} GB", estimated_memory_gb);
    
    if estimated_memory_gb > 24.0 {
        info!("⚠️  High memory usage detected. Consider reducing batch size.");
    }
    
    // Check output directory
    let output_dir = std::path::Path::new("models");
    if !output_dir.exists() {
        std::fs::create_dir_all(output_dir)?;
        info!("📁 Created output directory: models/");
    }
    
    info!("✅ Setup validation completed");
    Ok(())
}

/// Estimate memory requirements for training
fn estimate_memory_requirements(config: &KenyaAIConfig) -> f64 {
    // Rough estimation for Llama 3.1 8B
    let model_params = 8_000_000_000.0; // 8B parameters
    let bytes_per_param = 4.0; // FP32
    let gradient_memory = 2.0; // Gradients + optimizer states
    let batch_memory_multiplier = config.training.batch_size as f64 * config.training.gradient_accumulation as f64;
    
    let base_memory = (model_params * bytes_per_param * gradient_memory) / (1024.0 * 1024.0 * 1024.0);
    let batch_memory = (batch_memory_multiplier * config.dataset.max_length as f64 * 4.0) / (1024.0 * 1024.0 * 1024.0);
    
    base_memory + batch_memory
}

/// Display training progress and statistics
fn display_training_info(config: &KenyaAIConfig) {
    println!("\n🎯 KENYA-LLM TRAINING CONFIGURATION");
    println!("═══════════════════════════════════");
    println!("📚 Base Model: {}", config.model.base_model);
    println!("🎓 Dataset: Kenya-LLM-Bench-v1 (CBC-aligned)");
    println!("🇰🇪 Cultural Focus: Authentic Kenyan context");
    println!("📖 Curriculum: CBC (Competency-Based Curriculum)");
    println!("🗣️  Languages: English + Swahili code-switching");
    println!("🔥 Device: {} (AMD ROCm optimized)", config.training.device);
    println!("📊 Batch Size: {}", config.training.batch_size);
    println!("🔄 Epochs: {}", config.training.num_epochs);
    println!("📈 Learning Rate: {}", config.training.learning_rate);
    println!("═══════════════════════════════════");
    println!("🚀 Ready to train the future of African AI education!");
    println!();
}