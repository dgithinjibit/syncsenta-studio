# SyncSenta Data-First Strategy: Building the Kenya-LLM-Bench Dataset

## The Problem Statement
Generic LLMs fail Kenyan students because they lack:
- CBC curriculum alignment
- Local context and cultural nuance  
- KCPE/KCSE question patterns and "distractors"
- Competency-based learning progressions
- Swahili/English code-switching patterns

## The Solution: Curriculum-Aligned Synthetic Dataset (CASD)

### Phase 1: PDF-to-Dataset Pipeline ($0 Budget)

#### Step 1: KICD Curriculum Extraction
```python
# Use free tools to extract CBC curriculum data
import PyPDF2
import pandas as pd
from transformers import pipeline

# Extract text from KICD PDFs (freely available)
def extract_kicd_curriculum(pdf_path):
    """Extract structured curriculum data from KICD PDFs"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    # Structure the curriculum data
    curriculum_data = parse_curriculum_structure(text)
    return curriculum_data

def parse_curriculum_structure(text):
    """Parse CBC structure: Subject -> Grade -> Strand -> Sub-strand -> Learning Outcomes"""
    # Use regex patterns to extract structured data
    subjects = extract_subjects(text)
    grades = extract_grades(text)
    strands = extract_strands(text)
    learning_outcomes = extract_learning_outcomes(text)
    
    return {
        'subjects': subjects,
        'grades': grades, 
        'strands': strands,
        'learning_outcomes': learning_outcomes
    }
```

#### Step 2: Synthetic Data Generation Pipeline
```python
# Use free Hugging Face models for synthetic data generation
from transformers import AutoTokenizer, AutoModelForCausalLM

class CBCSyntheticDataGenerator:
    def __init__(self):
        # Use free models like microsoft/DialoGPT or google/flan-t5
        self.model_name = "microsoft/DialoGPT-large"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
    
    def generate_student_tutor_dialogue(self, learning_outcome, grade_level):
        """Generate Socratic tutoring dialogue for specific CBC learning outcome"""
        
        prompt = f"""
        Generate a tutoring dialogue between a Kenyan teacher and Grade {grade_level} student.
        Learning Outcome: {learning_outcome}
        
        Requirements:
        - Use Socratic method (guide, don't give answers)
        - Include Kenyan cultural context
        - Use appropriate Swahili/English mix for Grade {grade_level}
        - Include common student misconceptions
        - End with student understanding the concept
        
        Dialogue:
        """
        
        # Generate multiple variations
        dialogues = []
        for i in range(10):  # Generate 10 variations per learning outcome
            dialogue = self.generate_dialogue(prompt)
            dialogues.append({
                'input': learning_outcome,
                'context': f"Grade {grade_level} CBC curriculum",
                'output': dialogue,
                'metadata': {
                    'subject': self.extract_subject(learning_outcome),
                    'grade': grade_level,
                    'strand': self.extract_strand(learning_outcome),
                    'language_mix': self.detect_language_mix(dialogue)
                }
            })
        
        return dialogues
```

#### Step 3: Free Vector Database Alternative
```python
# Use ChromaDB (free, local) instead of Pinecone
import chromadb
from sentence_transformers import SentenceTransformer

class FreeVectorStore:
    def __init__(self):
        # Use free sentence transformer model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("cbc_curriculum")
    
    def add_curriculum_data(self, curriculum_items):
        """Add CBC curriculum data to vector store"""
        for item in curriculum_items:
            embedding = self.embedder.encode(item['text'])
            self.collection.add(
                embeddings=[embedding.tolist()],
                documents=[item['text']],
                metadatas=[item['metadata']],
                ids=[item['id']]
            )
    
    def search_similar_content(self, query, n_results=5):
        """Find similar curriculum content"""
        query_embedding = self.embedder.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        return results
```

### Phase 2: Dataset Structure for Hugging Face

#### SFT Format for Kenya-LLM-Bench
```json
{
  "conversations": [
    {
      "input": "Explain fractions to a Grade 4 student",
      "context": "CBC Mathematics Grade 4 - Number Operations Strand",
      "output": "Teacher: Habari John! Today we're learning about sehemu (fractions). If mama gives you one chapati and asks you to share it equally with your sister, how would you do it?\n\nStudent: I would cut it into two pieces?\n\nTeacher: Vizuri sana! Each piece would be what part of the whole chapati?\n\nStudent: Half?\n\nTeacher: Exactly! In mathematics, we write half as 1/2. The bottom number (2) shows how many equal parts we divided the chapati into. What does the top number (1) show?\n\nStudent: The number of pieces I have?\n\nTeacher: Perfect! Now, if you had 3 pieces out of 4 equal pieces of ugali, how would you write that fraction?",
      "metadata": {
        "subject": "Mathematics",
        "grade": "Grade 4", 
        "strand": "Number Operations",
        "sub_strand": "Fractions",
        "learning_outcome": "Learner should be able to identify and represent fractions",
        "cultural_context": ["chapati", "ugali", "Swahili greetings"],
        "pedagogical_approach": "Socratic method",
        "language_mix": "English-Swahili"
      }
    }
  ]
}
```

### Phase 3: Knowledge Tracing Without Expensive Tools

#### Free Student Progress Tracking
```python
# Use SQLite + simple ML models instead of expensive solutions
import sqlite3
import numpy as np
from sklearn.linear_model import LogisticRegression

class FreeKnowledgeTracer:
    def __init__(self):
        self.db = sqlite3.connect('student_progress.db')
        self.setup_database()
        self.model = LogisticRegression()
    
    def setup_database(self):
        """Create tables for tracking student progress"""
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_interactions (
                id INTEGER PRIMARY KEY,
                student_id TEXT,
                learning_outcome TEXT,
                question_type TEXT,
                response TEXT,
                correct BOOLEAN,
                error_type TEXT,
                timestamp DATETIME,
                difficulty_level INTEGER
            )
        ''')
        self.db.commit()
    
    def track_student_response(self, student_id, learning_outcome, response, correct, error_type=None):
        """Track individual student responses for knowledge tracing"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO student_interactions 
            (student_id, learning_outcome, response, correct, error_type, timestamp)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', (student_id, learning_outcome, response, correct, error_type))
        self.db.commit()
    
    def predict_mastery_probability(self, student_id, learning_outcome):
        """Predict probability of student mastering a concept"""
        # Get student's history for this learning outcome
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT correct, error_type, difficulty_level 
            FROM student_interactions 
            WHERE student_id = ? AND learning_outcome = ?
            ORDER BY timestamp DESC LIMIT 10
        ''', (student_id, learning_outcome))
        
        history = cursor.fetchall()
        if not history:
            return 0.5  # No data, assume 50% probability
        
        # Simple features for prediction
        features = self.extract_features(history)
        probability = self.model.predict_proba([features])[0][1]
        return probability
    
    def extract_features(self, history):
        """Extract features from student interaction history"""
        if not history:
            return [0, 0, 0, 0]
        
        recent_accuracy = sum(1 for h in history[:5] if h[0]) / min(5, len(history))
        overall_accuracy = sum(1 for h in history if h[0]) / len(history)
        error_diversity = len(set(h[1] for h in history if h[1])) / len(history)
        avg_difficulty = sum(h[2] for h in history if h[2]) / len(history)
        
        return [recent_accuracy, overall_accuracy, error_diversity, avg_difficulty]
```

### Phase 4: Implementation Roadmap

#### Week 1-2: Data Collection
- [ ] Download all KICD curriculum PDFs (free from KICD website)
- [ ] Extract and structure curriculum data using PyPDF2
- [ ] Create CBC curriculum taxonomy (subjects → grades → strands → learning outcomes)

#### Week 3-4: Synthetic Data Generation  
- [ ] Set up free Hugging Face models (DialoGPT, Flan-T5)
- [ ] Generate 1,000 student-tutor dialogues per grade level
- [ ] Human audit 5% for quality assurance
- [ ] Format data for Hugging Face dataset upload

#### Week 5-6: Vector Database Setup
- [ ] Install ChromaDB locally (free alternative to Pinecone)
- [ ] Embed all curriculum content using free sentence transformers
- [ ] Build semantic search for curriculum alignment

#### Week 7-8: Knowledge Tracing System
- [ ] Implement SQLite-based student progress tracking
- [ ] Build simple ML models for mastery prediction
- [ ] Create adaptive difficulty adjustment algorithms

### Phase 5: The Data Moat Strategy

#### Upload to Hugging Face
```python
# Create the Kenya-LLM-Bench dataset
from datasets import Dataset, DatasetDict

def create_kenya_llm_bench():
    """Create and upload the Kenya-LLM-Bench dataset"""
    
    # Load your synthetic data
    train_data = load_synthetic_dialogues('train')
    test_data = load_synthetic_dialogues('test')
    
    # Create dataset
    dataset = DatasetDict({
        'train': Dataset.from_pandas(train_data),
        'test': Dataset.from_pandas(test_data)
    })
    
    # Upload to Hugging Face (free)
    dataset.push_to_hub("dgithinjibit/Kenya-LLM-Bench-v1")
    
    return dataset
```

#### Competitive Advantage
Once you upload this dataset, you will have:
1. **The first CBC-aligned dataset on Hugging Face**
2. **Licensing opportunities** for other African EdTech companies
3. **Research partnerships** with universities
4. **Government contracts** for curriculum digitization
5. **International recognition** as the Kenya EdTech data pioneer

### Budget Breakdown: $0
- KICD PDFs: Free (government website)
- PyPDF2: Free Python library
- Hugging Face models: Free tier
- ChromaDB: Free, local vector database
- SQLite: Free database
- Hugging Face dataset hosting: Free
- Your time as SME: Priceless but free

This approach transforms you from "another LLM wrapper" to "the owner of African EdTech infrastructure." 🎯