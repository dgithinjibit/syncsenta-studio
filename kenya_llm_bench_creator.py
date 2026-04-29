#!/usr/bin/env python3
"""
Kenya-LLM-Bench Dataset Creator
Generates CBC-aligned Socratic tutoring dialogues for Kenyan education
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import os

class KenyaLLMBenchCreator:
    def __init__(self):
        self.dataset_name = "Kenya-LLM-Bench-v1"
        self.output_dir = Path("kenya_llm_bench_dataset")
        self.output_dir.mkdir(exist_ok=True)
        
        # CBC Curriculum Structure
        self.cbc_structure = self.load_cbc_structure()
        
        # Kenyan cultural elements
        self.kenyan_names = [
            "Amina", "John", "Wanjiku", "Omar", "Grace", "Peter", "Fatuma", 
            "David", "Aisha", "Michael", "Njeri", "Hassan", "Mary", "Joseph",
            "Zainab", "Daniel", "Wanjiru", "Ali", "Ruth", "Samuel"
        ]
        
        self.kenyan_foods = [
            "ugali", "sukuma wiki", "chapati", "mandazi", "nyama choma",
            "githeri", "mukimo", "samosa", "pilau", "matoke"
        ]
        
        self.kenyan_places = [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika",
            "Machakos", "Nyeri", "Meru", "Kakamega"
        ]
        
        self.swahili_greetings = [
            "Habari", "Hujambo", "Mambo", "Salamu", "Shikamoo"
        ]
        
        self.swahili_responses = [
            "Vizuri sana", "Poa", "Sawa", "Nzuri", "Asante"
        ]

    def load_cbc_structure(self) -> Dict[str, Any]:
        """Load CBC curriculum structure"""
        return {
            "Mathematics": {
                "Grade 1": {
                    "strands": ["Numbers", "Measurement", "Geometry"],
                    "learning_outcomes": [
                        "Count objects up to 99",
                        "Identify and write numbers 1-99", 
                        "Add numbers up to 20",
                        "Subtract numbers up to 20",
                        "Identify coins and notes",
                        "Measure length using non-standard units",
                        "Identify 2D shapes in the environment"
                    ]
                },
                "Grade 2": {
                    "strands": ["Numbers", "Measurement", "Geometry", "Data Handling"],
                    "learning_outcomes": [
                        "Count and write numbers up to 999",
                        "Add and subtract 2-digit numbers",
                        "Identify patterns in numbers",
                        "Tell time to the hour and half hour",
                        "Measure mass using balance",
                        "Identify 3D shapes",
                        "Collect and organize simple data"
                    ]
                },
                "Grade 3": {
                    "strands": ["Numbers", "Measurement", "Geometry", "Data Handling"],
                    "learning_outcomes": [
                        "Multiply numbers up to 12x12",
                        "Divide numbers with remainders",
                        "Work with fractions (halves, quarters)",
                        "Calculate with money (KES)",
                        "Measure capacity using standard units",
                        "Calculate perimeter of shapes",
                        "Read and interpret pictographs"
                    ]
                },
                "Grade 4": {
                    "strands": ["Number Operations", "Measurement", "Geometry", "Data Handling"],
                    "learning_outcomes": [
                        "Identify and represent fractions using visual models",
                        "Add and subtract fractions with like denominators", 
                        "Compare and order fractions",
                        "Solve word problems involving fractions",
                        "Measure length using meters and centimeters",
                        "Calculate area of rectangles",
                        "Create and interpret bar graphs"
                    ]
                },
                "Grade 5": {
                    "strands": ["Number Operations", "Measurement", "Geometry", "Data Handling"],
                    "learning_outcomes": [
                        "Multiply and divide fractions",
                        "Convert between fractions and decimals",
                        "Calculate percentage of quantities",
                        "Solve multi-step word problems",
                        "Calculate volume of rectangular prisms",
                        "Identify angles and their measures",
                        "Analyze data using mean and mode"
                    ]
                },
                "Grade 6": {
                    "strands": ["Number Operations", "Algebra", "Measurement", "Geometry", "Data Handling"],
                    "learning_outcomes": [
                        "Work with ratios and proportions",
                        "Solve simple algebraic equations",
                        "Calculate compound interest",
                        "Apply Pythagoras theorem",
                        "Calculate surface area of 3D shapes",
                        "Use coordinate geometry",
                        "Interpret statistical graphs"
                    ]
                }
            },
            "Science": {
                "Grade 1": {
                    "strands": ["Living Things", "Materials", "Energy"],
                    "learning_outcomes": [
                        "Identify parts of the human body",
                        "Classify animals by their characteristics",
                        "Identify different types of plants",
                        "Distinguish between living and non-living things",
                        "Identify sources of light and sound",
                        "Recognize different materials and their uses"
                    ]
                },
                "Grade 4": {
                    "strands": ["Living Things and Environment", "Materials and Properties", "Energy and Changes"],
                    "learning_outcomes": [
                        "Classify plants based on their characteristics",
                        "Explain the process of photosynthesis",
                        "Identify different types of soil",
                        "Describe the water cycle",
                        "Investigate properties of materials",
                        "Explain how sound travels",
                        "Demonstrate simple machines"
                    ]
                },
                "Grade 6": {
                    "strands": ["Living Things and Environment", "Materials and Properties", "Energy and Changes"],
                    "learning_outcomes": [
                        "Explain human reproduction system",
                        "Describe food chains and webs",
                        "Investigate chemical reactions",
                        "Understand states of matter",
                        "Explain electricity and circuits",
                        "Study renewable energy sources",
                        "Investigate forces and motion"
                    ]
                }
            },
            "English": {
                "Grade 3": {
                    "strands": ["Listening and Speaking", "Reading", "Writing", "Language Use"],
                    "learning_outcomes": [
                        "Listen and respond to simple instructions",
                        "Read simple texts with comprehension",
                        "Write simple sentences using correct grammar",
                        "Use appropriate vocabulary in context",
                        "Identify main ideas in texts",
                        "Write creative stories"
                    ]
                },
                "Grade 5": {
                    "strands": ["Listening and Speaking", "Reading", "Writing", "Language Use"],
                    "learning_outcomes": [
                        "Participate in group discussions",
                        "Read and analyze different text types",
                        "Write formal and informal letters",
                        "Use complex sentence structures",
                        "Identify literary devices",
                        "Write persuasive essays"
                    ]
                }
            },
            "Kiswahili": {
                "Grade 2": {
                    "strands": ["Kusikiliza na Kuzungumza", "Kusoma", "Kuandika", "Matumizi ya Lugha"],
                    "learning_outcomes": [
                        "Kusikiliza na kuelewa maagizo rahisi",
                        "Kusoma maneno na sentensi rahisi",
                        "Kuandika herufi na maneno",
                        "Kutumia msamiati sahihi",
                        "Kueleza picha kwa maneno"
                    ]
                },
                "Grade 4": {
                    "strands": ["Kusikiliza na Kuzungumza", "Kusoma", "Kuandika", "Matumizi ya Lugha"],
                    "learning_outcomes": [
                        "Kushiriki katika mazungumzo",
                        "Kusoma na kuelewa hadithi",
                        "Kuandika barua za kirafiki",
                        "Kutumia sarufi sahihi",
                        "Kutambua aina za maneno"
                    ]
                }
            }
        }

    def generate_socratic_dialogue(self, subject: str, grade: str, learning_outcome: str) -> Dict[str, Any]:
        """Generate a Socratic tutoring dialogue for a specific learning outcome"""
        
        student_name = random.choice(self.kenyan_names)
        greeting = random.choice(self.swahili_greetings)
        
        # Create context-specific dialogue based on subject and outcome
        if subject == "Mathematics":
            dialogue = self.generate_math_dialogue(grade, learning_outcome, student_name, greeting)
        elif subject == "Science":
            dialogue = self.generate_science_dialogue(grade, learning_outcome, student_name, greeting)
        elif subject == "English":
            dialogue = self.generate_english_dialogue(grade, learning_outcome, student_name, greeting)
        elif subject == "Kiswahili":
            dialogue = self.generate_kiswahili_dialogue(grade, learning_outcome, student_name, greeting)
        else:
            dialogue = self.generate_generic_dialogue(grade, learning_outcome, student_name, greeting)
        
        return {
            "input": f"Teach '{learning_outcome}' to a {grade} student using Socratic method",
            "context": f"CBC {subject} {grade} curriculum - Kenyan educational context",
            "output": dialogue,
            "metadata": {
                "subject": subject,
                "grade": grade,
                "learning_outcome": learning_outcome,
                "student_name": student_name,
                "pedagogical_approach": "Socratic method",
                "cultural_context": "Kenyan",
                "language_mix": "English-Swahili",
                "generated_at": datetime.now().isoformat()
            }
        }

    def generate_math_dialogue(self, grade: str, outcome: str, student_name: str, greeting: str) -> str:
        """Generate mathematics-specific Socratic dialogue"""
        
        if "fraction" in outcome.lower():
            food = random.choice(self.kenyan_foods)
            return f"""Teacher: {greeting} {student_name}! Today we're learning about sehemu (fractions). If mama gives you one {food} and asks you to share it equally with your sister, how would you do it?

Student: I would cut it into two pieces, teacher.

Teacher: Vizuri sana! Each piece would be what part of the whole {food}?

Student: Mmm... half?

Teacher: Exactly! In mathematics, we write half as 1/2. The bottom number (2) shows how many equal parts we divided the {food} into. What do you think the top number (1) shows?

Student: The number of pieces I have?

Teacher: Perfect! You're understanding well. Now, if you had 3 pieces out of 4 equal pieces of ugali, how would you write that fraction?

Student: Would it be 3/4?

Teacher: Excellent! You see how fractions help us describe parts of things we use every day. Can you think of another example from home?

Student: When we share mandazi among 5 people, each person gets 1/5?

Teacher: Wonderful! You're becoming a fraction expert. What happens if we want to add 1/4 + 1/4?

Student: We get 2/4?

Teacher: Yes! And can we make 2/4 simpler?

Student: It's the same as 1/2!

Teacher: Exactly! You've discovered that 2/4 = 1/2. This is called equivalent fractions."""
        
        elif "multiply" in outcome.lower() or "times" in outcome.lower():
            return f"""Teacher: {greeting} {student_name}! Let's explore multiplication using things from our daily life. If mama buys 3 packets of maize flour, and each packet costs 50 shillings, how much does she pay in total?

Student: Umm... I need to add 50 + 50 + 50?

Teacher: That's one way! Can you see a pattern there?

Student: I'm adding 50 three times?

Teacher: Exactly! When we add the same number multiple times, we can use multiplication. Instead of 50 + 50 + 50, we can write 3 × 50. What do you think 3 × 50 equals?

Student: 150 shillings?

Teacher: Vizuri sana! Now, if baba buys 4 crates of soda, and each crate has 24 bottles, how many bottles are there altogether?

Student: I need to find 4 × 24?

Teacher: Yes! Can you think of a way to solve this?

Student: Maybe I can break it down... 4 × 20 = 80, and 4 × 4 = 16, so 80 + 16 = 96?

Teacher: Excellent strategy! You used what we call the distributive property. You broke 24 into 20 + 4, then multiplied each part by 4."""
        
        else:
            return f"""Teacher: {greeting} {student_name}! Today we're exploring {outcome.lower()}. Can you tell me what you already know about this topic?

Student: I'm not sure, teacher. Can you help me understand?

Teacher: Of course! Let's start with something familiar. Think about when you go to the market with mama. How does this topic appear in real life?

Student: I think I see it when we count money or measure things?

Teacher: Good observation! Let's explore this step by step. What questions do you have?

Student: How do I know when to use this in solving problems?

Teacher: Excellent question! Let's work through some examples together and discover the patterns."""

    def generate_science_dialogue(self, grade: str, outcome: str, student_name: str, greeting: str) -> str:
        """Generate science-specific Socratic dialogue"""
        
        if "plant" in outcome.lower() or "photosynthesis" in outcome.lower():
            return f"""Teacher: {greeting} {student_name}! Let's take a walk around our school compound. What do you notice about the plants here?

Student: There are many different types - some have big leaves, others have small ones.

Teacher: Good observation! Now, look at this mti (tree). What does it need to grow big and strong?

Student: Water and sunlight?

Teacher: Vizuri! And what about soil - why do you think plants need soil?

Student: For nutrients?

Teacher: Exactly! Now, here's an interesting question - plants need food to grow, just like us. But have you ever seen a plant eating ugali or sukuma wiki?

Student: No, teacher! Plants don't eat like us.

Teacher: So how do you think plants get their food?

Student: Maybe they make their own food?

Teacher: Brilliant thinking! Plants do make their own food through a process called photosynthesis. What do you think they use to make this food?

Student: The sunlight and water you mentioned?

Teacher: Yes! And they also use something from the air. When you breathe out, what gas do you release?

Student: Carbon dioxide?

Teacher: Perfect! Plants take in carbon dioxide from the air, water from the soil, and use sunlight to make their food. What do you think they release back into the air that we need?

Student: Oxygen?

Teacher: Exactly! So plants help us by cleaning the air and giving us oxygen to breathe."""
        
        elif "water cycle" in outcome.lower():
            place = random.choice(self.kenyan_places)
            return f"""Teacher: {greeting} {student_name}! Yesterday it rained heavily in {place}. Where do you think all that rainwater goes?

Student: Some goes into the ground, and some flows into rivers?

Teacher: Good thinking! And what happens to the water in rivers and lakes when the sun shines on them?

Student: It gets hot?

Teacher: Yes, and something else happens. Have you noticed what happens to water when mama boils it for tea?

Student: It turns into steam and disappears?

Teacher: Exactly! The water doesn't really disappear - it changes into water vapor and goes into the air. This is called evaporation. What do you think happens to all that water vapor in the sky?

Student: It forms clouds?

Teacher: Vizuri sana! And when the clouds get heavy with water, what happens?

Student: It rains again?

Teacher: Perfect! So the water goes from the ground to the sky and back to the ground. This is called the water cycle. Can you trace the journey of a drop of water from Lake Victoria?"""
        
        else:
            return f"""Teacher: {greeting} {student_name}! Today we're investigating {outcome.lower()}. Let's start by observing our environment. What do you notice around us that relates to this topic?

Student: I can see many examples, but I'm not sure how they connect.

Teacher: That's a great start! Science is all about observing and asking questions. What questions come to your mind when you look at these examples?

Student: Why do things work the way they do?

Teacher: Excellent question! Let's investigate together and discover the answers through observation and experimentation."""

    def generate_english_dialogue(self, grade: str, outcome: str, student_name: str, greeting: str) -> str:
        """Generate English-specific Socratic dialogue"""
        
        return f"""Teacher: Hello {student_name}! Today we're working on {outcome.lower()}. Let's start with something you know well - can you tell me about your favorite Kenyan story?

Student: I like the story of the hare and the hyena, teacher.

Teacher: That's a wonderful choice! What makes that story interesting to you?

Student: The hare is very clever and always tricks the hyena.

Teacher: Good! You've identified the main characters and their traits. Now, when you tell this story to your younger brother, how do you make it exciting?

Student: I use different voices for the hare and hyena, and I make gestures.

Teacher: Excellent! You're using expression and body language. In writing, we need to do something similar. How can we make our writing as exciting as your storytelling?

Student: Use interesting words?

Teacher: Yes! We call these descriptive words. Instead of saying 'the hare ran,' what could we say to make it more exciting?

Student: The clever hare dashed quickly through the forest?

Teacher: Wonderful! You've added adjectives and a more specific verb. Can you think of other ways to improve our writing?

Student: Maybe add details about how things look or sound?

Teacher: Perfect! You're discovering the tools that make writing come alive for readers."""

    def generate_kiswahili_dialogue(self, grade: str, outcome: str, student_name: str, greeting: str) -> str:
        """Generate Kiswahili-specific Socratic dialogue"""
        
        return f"""Mwalimu: {greeting} {student_name}! Leo tunajifunza {outcome.lower()}. Hebu tuanze kwa kitu unachokijua vizuri - unaweza kuniambia jina la chakula unachokipenda?

Mwanafunzi: Napenda ugali na sukuma wiki, mwalimu.

Mwalimu: Vizuri sana! Sasa, ukitaka kumwambia rafiki yako kutoka nchi nyingine kuhusu chakula hiki, utasemaje?

Mwanafunzi: Nitamwambia kuwa ugali ni chakula cha asili cha Kiafrika?

Mwalimu: Nzuri! Umetumia maneno mazuri. Je, unajua tofauti kati ya 'chakula' na 'vyakula'?

Mwanafunzi: 'Chakula' ni kimoja, na 'vyakula' ni vingi?

Mwalimu: Kabisa! Umegundua kanuni muhimu ya Kiswahili. Maneno yanabadilika kulingana na idadi. Unaweza kutoa mfano mwingine?

Mwanafunzi: 'Kitabu' kimoja, 'vitabu' vingi?

Mwalimu: Vizuri sana! Unaona jinsi lugha yetu inavyofuata kanuni za kimantiki? Hii ni sababu ya kuwa Kiswahili ni lugha nzuri ya kujifunza."""

    def generate_generic_dialogue(self, grade: str, outcome: str, student_name: str, greeting: str) -> str:
        """Generate generic Socratic dialogue for any subject"""
        
        return f"""Teacher: {greeting} {student_name}! Today we're exploring {outcome.lower()}. What comes to your mind when you hear about this topic?

Student: I think I've seen examples of this in daily life, but I'm not sure how to explain it.

Teacher: That's a perfect starting point! Learning often begins with recognizing patterns around us. Can you describe one example you've noticed?

Student: Well, I see it when [specific example related to Kenyan context].

Teacher: Excellent observation! You're already thinking like a scholar. Now, what questions does this example raise for you?

Student: I wonder why it works that way, and if there are rules that govern it.

Teacher: Wonderful curiosity! Let's investigate together and discover those patterns. What do you think we should examine first?

Student: Maybe we should look at more examples and see what they have in common?

Teacher: Vizuri sana! You're developing the skills of a true investigator. Let's explore and see what we discover."""

    def generate_dataset_batch(self, target_size: int = 1000) -> List[Dict[str, Any]]:
        """Generate a batch of dialogues for the dataset"""
        
        dialogues = []
        subjects = list(self.cbc_structure.keys())
        
        # Calculate dialogues per subject
        dialogues_per_subject = target_size // len(subjects)
        
        for subject in subjects:
            grades = list(self.cbc_structure[subject].keys())
            dialogues_per_grade = dialogues_per_subject // len(grades)
            
            for grade in grades:
                learning_outcomes = self.cbc_structure[subject][grade]["learning_outcomes"]
                
                # Generate multiple dialogues per learning outcome
                for outcome in learning_outcomes:
                    variations = min(3, dialogues_per_grade // len(learning_outcomes) + 1)
                    
                    for _ in range(variations):
                        dialogue_data = self.generate_socratic_dialogue(subject, grade, outcome)
                        dialogues.append(dialogue_data)
                        
                        if len(dialogues) >= target_size:
                            break
                    
                    if len(dialogues) >= target_size:
                        break
                
                if len(dialogues) >= target_size:
                    break
            
            if len(dialogues) >= target_size:
                break
        
        return dialogues[:target_size]

    def save_dataset(self, dialogues: List[Dict[str, Any]], filename: str = None):
        """Save the dataset to JSON file"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kenya_llm_bench_{len(dialogues)}_dialogues_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        dataset = {
            "dataset_info": {
                "name": self.dataset_name,
                "description": "Curriculum-Aligned Synthetic Dataset for Kenyan CBC education using Socratic tutoring method",
                "version": "1.0.0",
                "license": "cc-by-4.0",
                "language": ["en", "sw"],
                "size": len(dialogues),
                "created_at": datetime.now().isoformat(),
                "subjects_covered": list(self.cbc_structure.keys()),
                "pedagogical_approach": "Socratic method",
                "cultural_context": "Kenyan"
            },
            "data": dialogues
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dataset saved to {filepath}")
        print(f"📊 Total dialogues: {len(dialogues)}")
        
        # Print statistics
        self.print_dataset_statistics(dialogues)
        
        return filepath

    def print_dataset_statistics(self, dialogues: List[Dict[str, Any]]):
        """Print statistics about the generated dataset"""
        
        subjects = {}
        grades = {}
        
        for dialogue in dialogues:
            subject = dialogue["metadata"]["subject"]
            grade = dialogue["metadata"]["grade"]
            
            subjects[subject] = subjects.get(subject, 0) + 1
            grades[grade] = grades.get(grade, 0) + 1
        
        print("\n📈 Dataset Statistics:")
        print("=" * 40)
        print("By Subject:")
        for subject, count in subjects.items():
            print(f"  {subject}: {count} dialogues")
        
        print("\nBy Grade:")
        for grade, count in sorted(grades.items()):
            print(f"  {grade}: {count} dialogues")
        
        print(f"\nTotal: {len(dialogues)} dialogues")

def main():
    """Main function to create the Kenya-LLM-Bench dataset"""
    
    print("🇰🇪 Kenya-LLM-Bench Dataset Creator")
    print("=" * 50)
    
    creator = KenyaLLMBenchCreator()
    
    # Generate dataset
    print("🔄 Generating CBC-aligned Socratic dialogues...")
    dialogues = creator.generate_dataset_batch(target_size=500)  # Start with 500
    
    # Save dataset
    print("💾 Saving dataset...")
    filepath = creator.save_dataset(dialogues)
    
    print(f"\n✨ Kenya-LLM-Bench dataset created successfully!")
    print(f"📁 File: {filepath}")
    print(f"🎯 Ready for Hugging Face upload!")
    
    return filepath

if __name__ == "__main__":
    main()