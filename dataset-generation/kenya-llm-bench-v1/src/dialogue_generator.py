#!/usr/bin/env python3
"""
Kenya-LLM-Bench-v1 Dialogue Generator

This module generates culturally authentic educational dialogues between
Mwalimu AI tutors and Kenyan students following CBC curriculum standards.
"""

import json
import random
import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import yaml

@dataclass
class DialogueTurn:
    """Represents a single turn in the dialogue"""
    role: str  # "student" or "tutor"
    content: str
    timestamp: str
    pedagogical_technique: Optional[str] = None
    cultural_elements: Optional[List[str]] = None

@dataclass
class Dialogue:
    """Represents a complete educational dialogue"""
    dialogue_id: str
    grade_level: str
    subject: str
    curriculum_strand: str
    sub_strand: str
    learning_objective: str
    cultural_context: str
    language_mix: str
    dialogue: List[DialogueTurn]
    learning_outcome: str
    difficulty_level: int
    metadata: Dict

class KenyaDialogueGenerator:
    """Generates CBC-aligned educational dialogues with Kenyan cultural context"""
    
    def __init__(self, curriculum_path: str, cultural_path: str):
        """Initialize with curriculum and cultural data"""
        with open(curriculum_path, 'r', encoding='utf-8') as f:
            self.curriculum = json.load(f)
        
        with open(cultural_path, 'r', encoding='utf-8') as f:
            self.cultural_elements = json.load(f)
        
        self.dialogue_templates = self._load_dialogue_templates()
        
    def _load_dialogue_templates(self) -> Dict:
        """Load dialogue templates for different pedagogical approaches"""
        return {
            "socratic_discovery": {
                "description": "Guide student to discover answer through questions",
                "tutor_starters": [
                    "Karibu! Let's explore this together. What do you notice about...",
                    "Habari! I see you're working on... What do you think about...",
                    "Good question! Before I answer, what do you already know about...",
                    "Pole, let me help you. Can you tell me what you see when..."
                ],
                "follow_up_questions": [
                    "What pattern do you notice?",
                    "How is this similar to something you know?",
                    "What would happen if we changed...?",
                    "Can you explain your thinking?",
                    "What makes you think that?"
                ]
            },
            "scaffolded_support": {
                "description": "Provide decreasing levels of support",
                "support_levels": [
                    "Let me show you step by step...",
                    "Now try this similar problem with my help...",
                    "Good! Can you try this one on your own?",
                    "Excellent! You've mastered this concept!"
                ]
            },
            "cultural_connection": {
                "description": "Connect learning to Kenyan cultural context",
                "connection_phrases": [
                    "Just like when we count {cultural_item} at the market...",
                    "Remember how we use {cultural_concept} in our daily life...",
                    "This is similar to when {cultural_scenario}...",
                    "In Kenya, we often see this when..."
                ]
            }
        }
    
    def generate_dialogue(self, 
                         grade_level: str, 
                         subject: str, 
                         target_length: int = 8) -> Dialogue:
        """Generate a single educational dialogue"""
        
        # Select curriculum content
        curriculum_content = self._select_curriculum_content(grade_level, subject)
        if not curriculum_content:
            raise ValueError(f"No curriculum content found for {grade_level} {subject}")
        
        # Select cultural context
        cultural_context = self._select_cultural_context()
        
        # Generate dialogue turns
        dialogue_turns = self._generate_dialogue_turns(
            curriculum_content, cultural_context, target_length
        )
        
        # Create dialogue object
        dialogue = Dialogue(
            dialogue_id=f"cbc_{subject.lower()}_{grade_level.lower()}_{uuid.uuid4().hex[:8]}",
            grade_level=grade_level,
            subject=subject,
            curriculum_strand=curriculum_content['strand'],
            sub_strand=curriculum_content['sub_strand'],
            learning_objective=curriculum_content['objective'],
            cultural_context=cultural_context['type'],
            language_mix="english_swahili",
            dialogue=dialogue_turns,
            learning_outcome="achieved",  # Will be validated later
            difficulty_level=self._calculate_difficulty_level(grade_level),
            metadata={
                "generated_by": "kiro_moe",
                "generated_at": datetime.now().isoformat(),
                "reviewed": False,
                "cultural_authenticity_score": 0.0,  # Will be calculated
                "pedagogical_effectiveness_score": 0.0  # Will be calculated
            }
        )
        
        return dialogue
    
    def _select_curriculum_content(self, grade_level: str, subject: str) -> Optional[Dict]:
        """Select specific curriculum content for the dialogue"""
        try:
            grade_data = self.curriculum['grade_levels'][grade_level]
            subject_data = grade_data['subjects'][subject]
            
            # Randomly select strand and sub-strand
            strand_name = random.choice(list(subject_data['strands'].keys()))
            strand_data = subject_data['strands'][strand_name]
            
            sub_strand = random.choice(strand_data['sub_strands'])
            objective = random.choice(strand_data['learning_objectives'])
            
            return {
                'strand': strand_name,
                'sub_strand': sub_strand,
                'objective': objective,
                'grade_level': grade_level,
                'subject': subject
            }
        except KeyError:
            return None
    
    def _select_cultural_context(self) -> Dict:
        """Select cultural context for the dialogue"""
        contexts = ['foods', 'animals', 'places', 'common_scenarios']
        context_type = random.choice(contexts)
        
        if context_type == 'foods':
            category = random.choice(['staples', 'snacks', 'fruits'])
            items = self.cultural_elements['kenyan_cultural_elements']['foods'][category]
            selected_item = random.choice(items)
            return {
                'type': 'kenyan_foods',
                'category': category,
                'item': selected_item
            }
        elif context_type == 'animals':
            category = random.choice(['wild', 'domestic'])
            animals = self.cultural_elements['kenyan_cultural_elements']['animals'][category]
            selected_animal = random.choice(animals)
            return {
                'type': 'kenyan_animals',
                'category': category,
                'animal': selected_animal
            }
        elif context_type == 'places':
            category = random.choice(['cities', 'landmarks'])
            places = self.cultural_elements['kenyan_cultural_elements']['places'][category]
            selected_place = random.choice(places)
            return {
                'type': 'kenyan_places',
                'category': category,
                'place': selected_place
            }
        else:  # common_scenarios
            scenarios = self.cultural_elements['kenyan_cultural_elements']['common_scenarios']
            scenario_name = random.choice(list(scenarios.keys()))
            return {
                'type': 'kenyan_scenarios',
                'scenario': scenarios[scenario_name]
            }
    
    def _generate_dialogue_turns(self, 
                                curriculum_content: Dict, 
                                cultural_context: Dict, 
                                target_length: int) -> List[DialogueTurn]:
        """Generate the actual dialogue turns"""
        turns = []
        base_time = datetime.now()
        
        # Student's initial question/confusion
        student_question = self._generate_student_question(curriculum_content, cultural_context)
        turns.append(DialogueTurn(
            role="student",
            content=student_question,
            timestamp=(base_time).isoformat()
        ))
        
        # Tutor's welcoming response with Socratic approach
        tutor_response = self._generate_tutor_response(
            curriculum_content, cultural_context, "socratic_discovery"
        )
        turns.append(DialogueTurn(
            role="tutor",
            content=tutor_response,
            timestamp=(base_time).isoformat(),
            pedagogical_technique="socratic_method",
            cultural_elements=self._extract_cultural_elements(tutor_response)
        ))
        
        # Continue dialogue with scaffolded support
        for i in range(2, target_length):
            if i % 2 == 0:  # Student turn
                student_response = self._generate_student_response(curriculum_content, i // 2)
                turns.append(DialogueTurn(
                    role="student",
                    content=student_response,
                    timestamp=(base_time).isoformat()
                ))
            else:  # Tutor turn
                technique = "scaffolded_support" if i < target_length - 2 else "reinforcement"
                tutor_response = self._generate_tutor_response(
                    curriculum_content, cultural_context, technique
                )
                turns.append(DialogueTurn(
                    role="tutor",
                    content=tutor_response,
                    timestamp=(base_time).isoformat(),
                    pedagogical_technique=technique,
                    cultural_elements=self._extract_cultural_elements(tutor_response)
                ))
        
        return turns
    
    def _generate_student_question(self, curriculum_content: Dict, cultural_context: Dict) -> str:
        """Generate authentic student question"""
        questions = [
            f"Mwalimu, I don't understand {curriculum_content['sub_strand'].lower()}",
            f"How do I solve this {curriculum_content['strand'].lower()} problem?",
            f"Can you help me with {curriculum_content['objective'].lower()}?",
            f"I'm confused about {curriculum_content['sub_strand'].lower()}. Can you explain?",
            f"Mwalimu, what does {curriculum_content['sub_strand'].lower()} mean?"
        ]
        
        # Add cultural context if relevant
        if cultural_context['type'] == 'kenyan_foods':
            item_name = cultural_context['item']['name']
            questions.extend([
                f"Mwalimu, how many {item_name} are there?",
                f"Can we use {item_name} to learn about {curriculum_content['strand'].lower()}?"
            ])
        
        return random.choice(questions)
    
    def _generate_tutor_response(self, 
                                curriculum_content: Dict, 
                                cultural_context: Dict, 
                                technique: str) -> str:
        """Generate culturally authentic tutor response"""
        
        # Start with Kenyan greeting
        greetings = ["Karibu!", "Habari!", "Pole, let me help you.", "Good question!"]
        greeting = random.choice(greetings)
        
        if technique == "socratic_discovery":
            questions = [
                "What do you already know about this topic?",
                "Can you think of where we see this in our daily life?",
                "What happens when we count things at the market?",
                "How is this similar to something you know?"
            ]
            
            # Add cultural connection
            if cultural_context['type'] == 'kenyan_foods':
                item = cultural_context['item']
                cultural_connection = f"Let's use {item['name']} to understand this. "
            elif cultural_context['type'] == 'kenyan_animals':
                animal = cultural_context['animal']
                cultural_connection = f"Think about {animal['name']} ({animal['english']}). "
            else:
                cultural_connection = "Let's think about this step by step. "
            
            question = random.choice(questions)
            return f"{greeting} {cultural_connection}{question}"
        
        elif technique == "scaffolded_support":
            supports = [
                "Let me show you one step at a time.",
                "We'll work through this together.",
                "First, let's start with something simple.",
                "Good effort! Now let's try the next step."
            ]
            return f"{greeting} {random.choice(supports)}"
        
        elif technique == "reinforcement":
            reinforcements = [
                "Excellent work! You understand this concept well.",
                "Vizuri sana! (Very good!) You've got it!",
                "Perfect! Now you can help other students too.",
                "Asante for working so hard. You've mastered this!"
            ]
            return random.choice(reinforcements)
        
        return f"{greeting} Let me help you understand this better."
    
    def _generate_student_response(self, curriculum_content: Dict, progress_level: int) -> str:
        """Generate student response showing learning progression"""
        if progress_level == 1:
            responses = [
                "I think I see what you mean...",
                "Oh, so it's like when we...",
                "Let me try... is it...?",
                "I'm starting to understand."
            ]
        elif progress_level == 2:
            responses = [
                "Yes! I can see the pattern now.",
                "That makes sense! So if I...",
                "I think I can do this one myself.",
                "Asante, Mwalimu! I understand better now."
            ]
        else:
            responses = [
                "I've got it! The answer is...",
                "Thank you for helping me understand!",
                "Now I can solve similar problems.",
                "This is actually easier than I thought!"
            ]
        
        return random.choice(responses)
    
    def _extract_cultural_elements(self, text: str) -> List[str]:
        """Extract cultural elements mentioned in the text"""
        elements = []
        
        # Check for Swahili words
        swahili_words = ["karibu", "habari", "asante", "pole", "vizuri", "sana", "mwalimu"]
        for word in swahili_words:
            if word.lower() in text.lower():
                elements.append(f"swahili_{word}")
        
        # Check for cultural items
        cultural_items = ["ugali", "sukuma wiki", "chapati", "mandazi", "matatu", "shamba"]
        for item in cultural_items:
            if item.lower() in text.lower():
                elements.append(f"kenyan_{item}")
        
        return elements
    
    def _calculate_difficulty_level(self, grade_level: str) -> int:
        """Calculate difficulty level based on grade"""
        difficulty_map = {
            'PP1': 1, 'PP2': 1,
            'Grade1': 2, 'Grade2': 2, 'Grade3': 3,
            'Grade4': 4, 'Grade5': 4, 'Grade6': 5,
            'Grade7': 6, 'Grade8': 7, 'Grade9': 8
        }
        return difficulty_map.get(grade_level, 5)
    
    def generate_dataset(self, target_size: int = 1000) -> List[Dialogue]:
        """Generate complete dataset of dialogues"""
        dialogues = []
        
        # Define distribution across grades and subjects
        grade_levels = ['PP1', 'PP2', 'Grade1', 'Grade2', 'Grade3', 'Grade4', 'Grade5', 'Grade6', 'Grade7', 'Grade8', 'Grade9']
        subjects = ['Mathematics', 'English', 'Kiswahili', 'Environmental Activities']
        
        # Calculate dialogues per combination
        dialogues_per_combo = target_size // (len(grade_levels) * len(subjects))
        
        for grade in grade_levels:
            for subject in subjects:
                # Skip subjects not available for certain grades
                if not self._is_subject_available(grade, subject):
                    continue
                
                for _ in range(dialogues_per_combo):
                    try:
                        dialogue = self.generate_dialogue(grade, subject)
                        dialogues.append(dialogue)
                        
                        if len(dialogues) % 50 == 0:
                            print(f"Generated {len(dialogues)} dialogues...")
                            
                    except Exception as e:
                        print(f"Error generating dialogue for {grade} {subject}: {e}")
                        continue
        
        # Fill remaining slots with random combinations
        while len(dialogues) < target_size:
            grade = random.choice(grade_levels)
            subject = random.choice(subjects)
            
            if self._is_subject_available(grade, subject):
                try:
                    dialogue = self.generate_dialogue(grade, subject)
                    dialogues.append(dialogue)
                except Exception:
                    continue
        
        print(f"Generated {len(dialogues)} total dialogues")
        return dialogues[:target_size]
    
    def _is_subject_available(self, grade_level: str, subject: str) -> bool:
        """Check if subject is available for the grade level"""
        try:
            return subject in self.curriculum['grade_levels'][grade_level]['subjects']
        except KeyError:
            return False
    
    def save_dialogues(self, dialogues: List[Dialogue], output_path: str):
        """Save dialogues to JSON file"""
        dialogue_dicts = [asdict(dialogue) for dialogue in dialogues]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dialogue_dicts, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(dialogues)} dialogues to {output_path}")

if __name__ == "__main__":
    # Example usage
    generator = KenyaDialogueGenerator(
        curriculum_path="data/cbc_curriculum.json",
        cultural_path="data/cultural_elements.json"
    )
    
    # Generate sample dialogue
    sample_dialogue = generator.generate_dialogue("Grade1", "Mathematics")
    print("Sample Dialogue:")
    print(json.dumps(asdict(sample_dialogue), indent=2, ensure_ascii=False))