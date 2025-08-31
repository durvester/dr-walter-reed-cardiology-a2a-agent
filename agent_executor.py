"""
Dr. Walter Reed's Interventional Cardiology Agent Executor

A proper A2A SDK-compliant agent executor for interventional cardiology practice.
This implementation follows the official A2A patterns and best practices without shortcuts.

Key Features:
- Proper A2A SDK AgentExecutor implementation
- Professional medical communication for interventional cardiology
- Input validation and security measures
- Claude API integration for medical expertise
- Full compliance with A2A protocol patterns

Medical Specializations:
- Interventional procedures (angiography, angioplasty)
- Heart failure management and optimization  
- Ischemic heart disease treatment
- Stroke prevention and acute management
- Advanced diagnostics (stress tests, ECG, 2D echo)
"""

import logging
import uuid
from typing import List

import anthropic
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import Message, TextPart, Task, TaskStatus, TaskState

from config import config

# Configure logging
logger = logging.getLogger(__name__)

class InterventionalCardiologyExecutor(AgentExecutor):
    """
    A2A-compliant agent executor for Dr. Walter Reed's Interventional Cardiology Practice.
    
    This executor implements the official A2A SDK patterns for:
    - Processing incoming messages via RequestContext
    - Sending responses via EventQueue  
    - Professional medical communication
    - Security validation and input protection
    - Integration with Claude API for medical expertise
    """
    
    def __init__(self):
        """Initialize the interventional cardiology executor with proper A2A patterns."""
        logger.info("Initializing Dr. Walter Reed's Interventional Cardiology Executor")
        
        # Initialize Claude client
        self.anthropic_client = anthropic.Anthropic(
            api_key=config.claude.api_key
        )
        
        # Get the properly formatted system prompt from configuration
        self.system_prompt = config.get_formatted_system_prompt()
        
        logger.info(f"Executor initialized for {config.agent.practice_name}")
        logger.info(f"Services: {len(config.agent.primary_services)} primary, {len(config.agent.diagnostic_services)} diagnostic")
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Execute a task following proper A2A SDK patterns.
        
        This method:
        1. Accesses the incoming message via context.message
        2. Extracts conversation history from context.current_task if needed
        3. Processes the medical request with appropriate validation
        4. Generates professional medical responses via Claude API
        5. Sends responses back via event_queue.enqueue_event()
        
        Args:
            context: A2A RequestContext containing the incoming message and task info
            event_queue: A2A EventQueue for sending response messages
        """
        try:
            # Get the incoming message from the A2A context
            incoming_message = context.message
            current_task = context.current_task
            
            logger.info(f"Processing message for task {context.task_id}")
            logger.info(f"Message role: {incoming_message.role}")
            
            # Extract text content from the incoming message parts
            user_text = self._extract_text_from_message(incoming_message)
            if not user_text.strip():
                await self._send_task_response(event_queue, 
                    "Hello! How can I assist you with our interventional cardiology services today?",
                    context
                )
                return
            
            logger.info(f"User query: {user_text[:100]}...")
            
            # Validate input for security (following A2A best practices)
            if not self._validate_input_security(user_text):
                await self._send_task_response(event_queue,
                    "I'm here to assist with medical information and coordination. "
                    "Please ask about our interventional cardiology services.",
                    context
                )
                return
            
            # Build conversation context for Claude
            conversation_messages = self._build_conversation_context(current_task, user_text)
            
            # Generate medical response using Claude API
            response_text = await self._generate_medical_response(conversation_messages)
            
            # Send the response via A2A event queue
            await self._send_task_response(event_queue, response_text, context)
            
            logger.info(f"Successfully processed task {context.task_id}")
            
        except Exception as e:
            logger.error(f"Error processing task {context.task_id}: {str(e)}")
            
            # Send error response following A2A patterns
            await self._send_task_response(event_queue,
                "I apologize, but I'm experiencing technical difficulties. "
                "Please try again later. For urgent medical matters, please contact "
                "our office directly.",
                context
            )
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Handle task cancellation following A2A SDK patterns.
        
        Since our interventional cardiology consultations complete quickly,
        cancellation is straightforward.
        """
        logger.info(f"Canceling task {context.task_id}")
        # The A2A framework handles cancellation responses automatically
    
    def _extract_text_from_message(self, message: Message) -> str:
        """Extract text content from A2A message parts."""
        text_parts = []
        
        for part in message.parts:
            # Simple direct access to text parts
            if hasattr(part, 'text') and part.text:
                text_parts.append(part.text.strip())
        
        return " ".join(text_parts)
    
    def _validate_input_security(self, text: str) -> bool:
        """
        Validate input for security following A2A best practices.
        
        As noted in A2A documentation: "treat any agent operating outside of 
        your direct control as a potentially untrusted entity"
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
    
    def _build_conversation_context(self, current_task, user_text: str) -> List[dict]:
        """Build conversation context for Claude API from A2A task history."""
        messages = []
        
        # If we have task history, include it for context
        if current_task and current_task.history:
            for msg in current_task.history:
                content = self._extract_text_from_message(msg)
                if content:
                    if msg.role == "user":
                        messages.append({"role": "user", "content": content})
                    elif msg.role == "agent":
                        messages.append({"role": "assistant", "content": content})
        
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
    
    async def _send_task_response(self, event_queue: EventQueue, text: str, context: RequestContext) -> None:
        """
        Send a Task response via A2A EventQueue.
        
        Creates a simple Task object with the agent response and sends it.
        """
        try:
            # Create agent response message
            agent_message = Message(
                message_id=str(uuid.uuid4()),
                role="agent",
                parts=[TextPart(text=text)],
                metadata={
                    "timestamp": self._get_current_timestamp()
                }
            )
            
            # Build history with user message + agent response
            history = [context.message, agent_message] if context.message else [agent_message]
            
            # Create simple Task object
            task_id = context.task_id or str(uuid.uuid4())
            
            task = Task(
                id=task_id,
                context_id=task_id,
                status=TaskStatus(state=TaskState.completed),
                history=history,
                artifacts=[]
            )
            
            # Send Task via event queue
            await event_queue.enqueue_event(task)
            
            logger.debug(f"Sent task response: {text[:50]}...")
            
        except Exception as e:
            logger.error(f"Failed to send task: {str(e)}")
            raise
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()