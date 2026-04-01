from typing import Dict, List
import json

class NCDKnowledgeBase:
    """Knowledge base for Non-Communicable Diseases"""
    
    def __init__(self):
        self.ncd_data = {
            "diabetes": {
                "description": "Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces.",
                "symptoms": [
                    "Increased thirst",
                    "Frequent urination", 
                    "Extreme hunger",
                    "Unexplained weight loss",
                    "Fatigue",
                    "Irritability",
                    "Blurred vision"
                ],
                "prevention": [
                    "Maintain healthy body weight",
                    "Regular physical activity (at least 30 minutes daily)",
                    "Eat a healthy diet",
                    "Avoid tobacco use",
                    "Limit sugar and saturated fats intake"
                ],
                "management": [
                    "Regular blood sugar monitoring",
                    "Medication as prescribed",
                    "Regular exercise",
                    "Balanced diet",
                    "Regular medical check-ups"
                ]
            },
            "cardiovascular": {
                "description": "Cardiovascular diseases are disorders of the heart and blood vessels, including coronary heart disease, cerebrovascular disease, and peripheral arterial disease.",
                "symptoms": [
                    "Chest pain or discomfort",
                    "Shortness of breath",
                    "Pain in neck, jaw, or back",
                    "Pain or weakness in arms or legs",
                    "Fatigue",
                    "Dizziness or lightheadedness"
                ],
                "prevention": [
                    "Quit smoking",
                    "Reduce salt intake",
                    "Eat fruits and vegetables",
                    "Regular physical activity",
                    "Maintain healthy weight",
                    "Limit alcohol consumption"
                ],
                "management": [
                    "Take medications as prescribed",
                    "Low-sodium diet",
                    "Regular exercise",
                    "Stress management",
                    "Regular monitoring of blood pressure and cholesterol"
                ]
            },
            "cancer": {
                "description": "Cancer is a disease characterized by uncontrolled growth and spread of abnormal cells.",
                "symptoms": [
                    "Unexplained weight loss",
                    "Fatigue",
                    "Persistent pain",
                    "Changes in skin",
                    "Changes in bowel or bladder habits",
                    "Persistent cough or hoarseness"
                ],
                "prevention": [
                    "Avoid tobacco use",
                    "Maintain healthy diet",
                    "Regular physical activity",
                    "Limit alcohol consumption",
                    "Protect from sun exposure",
                    "Regular health screenings"
                ],
                "management": [
                    "Early detection through screening",
                    "Medical treatment (surgery, chemotherapy, radiation)",
                    "Palliative care",
                    "Lifestyle modifications",
                    "Regular follow-up care"
                ]
            },
            "respiratory": {
                "description": "Chronic respiratory diseases are diseases of the airways and other structures of the lungs, including asthma and COPD.",
                "symptoms": [
                    "Shortness of breath",
                    "Wheezing",
                    "Chest tightness",
                    "Chronic cough",
                    "Excess mucus production"
                ],
                "prevention": [
                    "Avoid tobacco smoke",
                    "Reduce exposure to air pollutants",
                    "Regular exercise",
                    "Maintain healthy weight",
                    "Get vaccinated"
                ],
                "management": [
                    "Medication (inhalers, oral medications)",
                    "Pulmonary rehabilitation",
                    "Oxygen therapy if needed",
                    "Avoid triggers",
                    "Regular medical monitoring"
                ]
            }
        }
    
    def get_disease_info(self, disease: str) -> Dict:
        """Get information about a specific NCD"""
        disease_lower = disease.lower()
        return self.ncd_data.get(disease_lower, {})
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all available diseases"""
        return list(self.ncd_data.keys())
    
    def search_symptoms(self, symptoms: List[str]) -> List[str]:
        """Search for diseases based on symptoms"""
        matching_diseases = []
        for disease, info in self.ncd_data.items():
            disease_symptoms = [s.lower() for s in info.get("symptoms", [])]
            for symptom in symptoms:
                if symptom.lower() in disease_symptoms:
                    matching_diseases.append(disease)
                    break
        return matching_diseases
    
    def get_prevention_tips(self, disease: str) -> List[str]:
        """Get prevention tips for a specific disease"""
        disease_info = self.get_disease_info(disease)
        return disease_info.get("prevention", [])
    
    def get_management_tips(self, disease: str) -> List[str]:
        """Get management tips for a specific disease"""
        disease_info = self.get_disease_info(disease)
        return disease_info.get("management", [])

# Global knowledge base instance
knowledge_base = NCDKnowledgeBase()
