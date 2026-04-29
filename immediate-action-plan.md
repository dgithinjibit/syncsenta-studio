# Immediate Action Plan: Building Kenya-LLM-Bench Dataset

## Today's Tasks (Next 4 Hours)

### Task 1: Set Up the Data Pipeline Environment
```bash
# Create virtual environment
python -m venv kenya-llm-bench
source kenya-llm-bench/bin/activate  # On Windows: kenya-llm-bench\Scripts\activate

# Install required packages (all free)
pip install PyPDF2 pandas transformers datasets chromadb sentence-transformers scikit-learn requests beautifulsoup4
```

### Task 2: Download KICD Curriculum PDFs
```python
# Create curriculum_downloader.py
import requests
import os
from urllib.parse import urljoin, urlparse

class KICDCurriculumDownloader:
    def __init__(self):
        self.base_url = "https://kicd.ac.ke"
        self.download_dir = "kicd_pdfs"
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_cbc_documents(self):
        """Download all available CBC curriculum documents"""
        # Known KICD curriculum URLs (update these with actual URLs)
        curriculum_urls = [
            "https://kicd.ac.ke/wp-content/uploads/2019/07/MATHEMATICS-GRADE-1.pdf",
            "https://kicd.ac.ke/wp-content/uploads/2019/07/MATHEMATICS-GRADE-2.pdf", 
            "https://kicd.ac.ke/wp-content/uploads/2019/07/MATHEMATICS-GRADE-3.pdf",
            # Add more URLs as you find them
        ]
        
        for url in curriculum_urls:
            self.download_pdf(url)
    
    def download_pdf(self, url):
        """Download individual PDF file"""
        try:
            response = requests.get(url)
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Run the downloader
if __name__ == "__main__":
    downloader = KICDCurriculumDownloader()
    downloader.download_cbc_documents()
```

### Task 3: Create PDF Text Extractor
```python
# Create curriculum_extractor.py
import PyPDF2
import json
import re
from pathlib import Path

class CBCCurriculumExtractor:
    def __init__(self, pdf_directory="kicd_pdfs"):
        self.pdf_directory = Path(pdf_directory)
        self.curriculum_data = {}
    
    def extract_all_pdfs(self):
        """Extract text from all PDFs in directory"""
        for pdf_file in self.pdf_directory.glob("*.pdf"):
            print(f"Processing: {pdf_file.name}")
            text = self.extract_pdf_text(pdf_file)
            structured_data = self.structure_curriculum_data(text, pdf_file.name)
            self.curriculum_data[pdf_file.stem] = structured_data
        
        # Save extracted data
        with open("cbc_curriculum_data.json", "w") as f:
            json.dump(self.curriculum_data, f, indent=2)
        
        return self.curriculum_data
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting {pdf_path}: {e}")
        
        return text
    
    def structure_curriculum_data(self, text, filename):
        """Structure curriculum text into learning outcomes"""
        # Extract subject and grade from filename
        subject_grade = self.parse_filename(filename)
        
        # Extract learning outcomes using regex patterns
        learning_outcomes = self.extract_learning_outcomes(text)
        strands = self.extract_strands(text)
        
        return {
            "subject": subject_grade["subject"],
            "grade": subject_grade["grade"],
            "strands": strands,
            "learning_outcomes": learning_outcomes,
            "raw_text": text[:1000]  # First 1000 chars for reference
        }
    
    def parse_filename(self, filename):
        """Parse subject and grade from filename"""
        # Example: "MATHEMATICS-GRADE-1.pdf" -> {"subject": "Mathematics", "grade": "Grade 1"}
        parts = filename.upper().replace(".PDF", "").split("-")
        subject = parts[0].title() if parts else "Unknown"
        grade = f"Grade {parts[-1]}" if len(parts) > 1 else "Unknown"
        
        return {"subject": subject, "grade": grade}
    
    def extract_learning_outcomes(self, text):
        """Extract learning outcomes from curriculum text"""
        # Common patterns for learning outcomes in KICD documents
        patterns = [
            r"By the end of.*?the learner should be able to:?\s*(.*?)(?=\n\n|\n[A-Z])",
            r"Learning outcomes?:?\s*(.*?)(?=\n\n|\n[A-Z])",
            r"The learner should be able to:?\s*(.*?)(?=\n\n|\n[A-Z])"
        ]
        
        outcomes = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            outcomes.extend(matches)
        
        # Clean and split outcomes
        cleaned_outcomes = []
        for outcome in outcomes:
            # Split by bullet points or numbers
            items = re.split(r'[•\-\d+\.\)]\s*', outcome)
            cleaned_outcomes.extend([item.strip() for item in items if item.strip()])
        
        return cleaned_outcomes[:20]  # Limit to first 20 outcomes
    
    def extract_strands(self, text):
        """Extract curriculum strands from text"""
        # Look for strand patterns
        strand_patterns = [
            r"Strand\s*\d*:?\s*([A-Za-z\s]+)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*Strand",
        ]
        
        strands = []
        for pattern in strand_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            strands.extend(matches)
        
        return list(set(strands))  # Remove duplicates

# Run the extractor
if __name__ == "__main__":
    extractor = CBCCurriculumExtractor()
    curriculum_data = extractor.extract_all_pdfs()
    print(f"Extracted data from {len(curriculum_data)} documents")
```

### Task 4: Generate First Synthetic Dialogues
```python
# Create dialogue_generator.py
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import json
import random

class SocraticDialogueGenerator:
    def __init__(self):
        # Use free Hugging Face model
        self.generator = pipeline("text-generation", 
                                model="microsoft/DialoGPT-medium",
                                tokenizer="microsoft/DialoGPT-medium")
        
        # Load curriculum data
        with open("cbc_curriculum_data.json", "r") as f:
            self.curriculum_data = json.load(f)
    
    def generate_dialogue_for_outcome(self, subject, grade, learning_outcome):
        """Generate Socratic dialogue for specific learning outcome"""
        
        # Create culturally relevant prompt
        prompt = self.create_kenyan_prompt(subject, grade, learning_outcome)
        
        # Generate dialogue
        dialogue = self.generate_socratic_conversation(prompt)
        
        return {
            "input": f"Teach {learning_outcome} to a {grade} student",
            "context": f"CBC {subject} {grade} curriculum",
            "output": dialogue,
            "metadata": {
                "subject": subject,
                "grade": grade,
                "learning_outcome": learning_outcome,
                "pedagogical_approach": "Socratic method",
                "cultural_context": "Kenyan",
                "language_mix": "English-Swahili"
            }
        }
    
    def create_kenyan_prompt(self, subject, grade, learning_outcome):
        """Create culturally relevant prompt for dialogue generation"""
        
        # Kenyan names for diversity
        student_names = ["Amina", "John", "Wanjiku", "Omar", "Grace", "Peter", "Fatuma", "David"]
        student_name = random.choice(student_names)
        
        # Cultural contexts by subject
        cultural_contexts = {
            "Mathematics": ["sharing ugali", "counting matatu fare", "dividing sukuma wiki", "calculating maize harvest"],
            "Science": ["observing baobab trees", "studying Lake Victoria", "examining maize growth", "weather in Nairobi"],
            "English": ["reading Kenyan stories", "writing about safari", "discussing family traditions"],
            "Kiswahili": ["mazungumzo ya kila siku", "hadithi za kimila", "mazingira ya Kenya"]
        }
        
        context = random.choice(cultural_contexts.get(subject, ["everyday life in Kenya"]))
        
        prompt = f"""
        Generate a tutoring dialogue between a Kenyan teacher and {student_name}, a {grade} student.
        
        Learning Outcome: {learning_outcome}
        Cultural Context: {context}
        
        Requirements:
        - Use Socratic method (ask guiding questions, don't give direct answers)
        - Include appropriate Swahili greetings and phrases
        - Use examples from Kenyan daily life
        - Guide the student to discover the answer themselves
        - Show common misconceptions and how to address them
        
        Teacher: Habari {student_name}! Today we're going to explore {learning_outcome.lower()}. 
        """
        
        return prompt
    
    def generate_socratic_conversation(self, prompt):
        """Generate the actual conversation using the LLM"""
        try:
            # Generate response
            response = self.generator(prompt, 
                                   max_length=500, 
                                   num_return_sequences=1,
                                   temperature=0.8,
                                   do_sample=True)
            
            generated_text = response[0]['generated_text']
            
            # Clean up the generated text
            dialogue = self.clean_dialogue(generated_text)
            
            return dialogue
            
        except Exception as e:
            print(f"Error generating dialogue: {e}")
            return self.create_fallback_dialogue(prompt)
    
    def clean_dialogue(self, text):
        """Clean and format the generated dialogue"""
        # Remove the original prompt
        lines = text.split('\n')
        dialogue_lines = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('Teacher:') or line.startswith('Student:')):
                dialogue_lines.append(line)
        
        return '\n'.join(dialogue_lines)
    
    def create_fallback_dialogue(self, prompt):
        """Create a simple fallback dialogue if generation fails"""
        return """Teacher: Habari! Let's explore this concept together.
Student: Habari teacher! I'm ready to learn.
Teacher: Good! Can you tell me what you already know about this topic?
Student: I'm not sure, can you help me understand?
Teacher: Of course! Let's start with a simple example from our daily life..."""
    
    def generate_dataset_batch(self, batch_size=100):
        """Generate a batch of dialogues for the dataset"""
        dialogues = []
        
        for doc_name, doc_data in self.curriculum_data.items():
            subject = doc_data.get("subject", "Unknown")
            grade = doc_data.get("grade", "Unknown")
            learning_outcomes = doc_data.get("learning_outcomes", [])
            
            # Generate dialogues for each learning outcome
            for outcome in learning_outcomes[:5]:  # Limit to first 5 per document
                if outcome and len(outcome) > 10:  # Skip very short outcomes
                    dialogue_data = self.generate_dialogue_for_outcome(subject, grade, outcome)
                    dialogues.append(dialogue_data)
                    
                    if len(dialogues) >= batch_size:
                        break
            
            if len(dialogues) >= batch_size:
                break
        
        # Save the batch
        with open(f"synthetic_dialogues_batch_{len(dialogues)}.json", "w") as f:
            json.dump(dialogues, f, indent=2)
        
        print(f"Generated {len(dialogues)} synthetic dialogues")
        return dialogues

# Run the generator
if __name__ == "__main__":
    generator = SocraticDialogueGenerator()
    dialogues = generator.generate_dataset_batch(50)  # Start with 50 dialogues
```

## This Week's Deliverables

By the end of this week, you should have:

1. **✅ 50+ synthetic CBC-aligned dialogues** in SFT format
2. **✅ Structured curriculum data** from KICD PDFs  
3. **✅ Working data pipeline** for scaling up
4. **✅ First version** ready for Hugging Face upload

## Next Week: Scale to 1,000+ Dialogues

Once you have the pipeline working, you can:
- Generate 10 variations per learning outcome
- Cover all CBC subjects and grades
- Add quality control and human auditing
- Upload to Hugging Face as "Kenya-LLM-Bench-v1"

## The Strategic Impact

This approach will:
- **Position you as the CBC data authority**
- **Create licensing opportunities** for other EdTech companies
- **Attract research partnerships** with universities
- **Enable government contracts** for curriculum digitization
- **Build the foundation** for truly effective Kenyan AI tutoring

**Start with Task 1 today!** 🚀