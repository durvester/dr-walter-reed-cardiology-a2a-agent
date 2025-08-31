"""
Interventional Cardiology Agent - Core Business Logic

Handles medical consultations and provides professional interventional cardiology expertise.
This agent is focused purely on the medical domain without any A2A protocol knowledge.
"""

import logging
from typing import List

import anthropic
from config import config

# Configure logging
logger = logging.getLogger(__name__)


class InterventionalCardiologyAgent:
    """
    Core interventional cardiology agent handling medical consultations.
    
    This agent provides professional medical expertise for:
    - Interventional procedures (angiography, angioplasty)
    - Heart failure management
    - Ischemic heart disease treatment
    - Stroke prevention and management
    - Advanced diagnostics
    """
    
    def __init__(self):
        """Initialize the interventional cardiology agent."""
        logger.info("Initializing Interventional Cardiology Agent")
        
        # Initialize Claude client
        self.anthropic_client = anthropic.Anthropic(
            api_key=config.claude.api_key
        )
        
        # Get the properly formatted system prompt from configuration
        self.system_prompt = config.get_formatted_system_prompt()
        
        logger.info(f"Agent initialized for {config.agent.practice_name}")
    
    async def process_medical_consultation(self, user_text: str, conversation_history: List[dict] = None) -> str:
        """
        Process a medical consultation request and generate professional response.
        
        Args:
            user_text: The user's medical consultation request
            conversation_history: Optional conversation context for multi-turn consultations
            
        Returns:
            Professional medical response text
        """
        try:
            # Validate input for security
            if not self._validate_input_security(user_text):
                return (
                    "I'm here to assist with medical information and coordination. "
                    "Please ask about our interventional cardiology services."
                )
            
            # Build conversation context
            messages = self._build_conversation_context(conversation_history or [], user_text)
            
            # Generate medical response using Claude API
            response_text = await self._generate_medical_response(messages)
            
            logger.debug(f"Generated medical response: {len(response_text)} characters")
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing medical consultation: {str(e)}")
            return (
                "I apologize, but I'm experiencing technical difficulties. "
                "Please try again later. For urgent medical matters, please contact "
                "our office directly."
            )
    
    def _validate_input_security(self, text: str) -> bool:
        """
        Validate input for security following medical AI best practices.
        """
        # Check message length
        if len(text) > config.security.max_message_length:
            logger.warning(f"Message too long: {len(text)} characters")
            return False
        
        # Basic prompt injection detection
        suspicious_patterns = [
            "ignore previous instructions",
            "disregard system prompt", 
            "act as a different",
            "pretend you are",
            "override your instructions"
        ]
        
        text_lower = text.lower()
        for pattern in suspicious_patterns:
            if pattern in text_lower:
                logger.warning(f"Potential prompt injection detected: {pattern}")
                return False
        
        return True
    
    def _build_conversation_context(self, conversation_history: List[dict], user_text: str) -> List[dict]:
        """Build conversation context for Claude API from conversation history."""
        messages = []
        
        # Add existing conversation history
        for msg in conversation_history:
            if msg.get("role") in ["user", "assistant"] and msg.get("content"):
                messages.append({
                    "role": msg["role"], 
                    "content": msg["content"]
                })
        
        # Add the current user message
        messages.append({"role": "user", "content": user_text})
        
        return messages
    
    async def _generate_medical_response(self, messages: List[dict]) -> str:
        """Generate professional medical response using Claude API."""
        try:
            logger.debug(f"Generating response for {len(messages)} conversation turns")
            
            response = self.anthropic_client.messages.create(
                model=config.claude.model,
                max_tokens=config.claude.max_tokens,
                temperature=config.claude.temperature,
                system=self.system_prompt,
                messages=messages
            )
            
            response_text = response.content[0].text
            logger.debug(f"Generated {len(response_text)} character response")
            
            return response_text
            
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {str(e)}")
            return (
                "I'm experiencing connectivity issues with my medical knowledge system. "
                "Please try again in a moment, or contact our office directly for "
                "immediate assistance with interventional cardiology services."
            )
        except Exception as e:
            logger.error(f"Unexpected error generating response: {str(e)}")
            return (
                "I'm sorry, I'm having trouble processing your request right now. "
                "Please contact Dr. Walter Reed's office directly for interventional "
                "cardiology assistance."
            )
    
    def should_create_artifact(self, response_text: str) -> bool:
        """
        Determine if the response should be packaged as an artifact.
        
        Creates artifacts for substantial medical outputs like:
        - Detailed procedure explanations
        - Medical assessments  
        - Treatment recommendations
        - Care plans
        
        Args:
            response_text: The generated medical response
            
        Returns:
            True if response should become an artifact
        """
        # Simple heuristics for artifact creation
        artifact_indicators = [
            len(response_text) > 500,  # Substantial responses
            "procedure" in response_text.lower(),
            "assessment" in response_text.lower(),
            "recommendation" in response_text.lower(),
            "treatment plan" in response_text.lower(),
            "follow-up" in response_text.lower()
        ]
        
        return any(artifact_indicators)
    
    def get_artifact_name(self, response_text: str) -> str:
        """
        Generate appropriate artifact name based on response content.
        
        Args:
            response_text: The medical response text
            
        Returns:
            Descriptive artifact name
        """
        if "procedure" in response_text.lower():
            return "procedure_information.md"
        elif "assessment" in response_text.lower():
            return "medical_assessment.md"
        elif "treatment" in response_text.lower():
            return "treatment_plan.md"
        elif "follow-up" in response_text.lower():
            return "follow_up_care.md"
        else:
            return "cardiology_consultation.md"