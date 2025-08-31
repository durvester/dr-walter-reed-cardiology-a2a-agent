"""
Dr. Walter Reed's Interventional Cardiology Agent Executor

A2A integration layer for interventional cardiology practice.
Implements proper A2A SDK patterns with TaskUpdater for state management.

This executor delegates medical business logic to InterventionalCardiologyAgent
and focuses purely on A2A protocol integration and task lifecycle management.
"""

import logging
from typing import List

from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TextPart, TaskState
from a2a.types import Artifact

from agent import InterventionalCardiologyAgent
from config import config

# Configure logging
logger = logging.getLogger(__name__)

class InterventionalCardiologyExecutor(AgentExecutor):
    """
    A2A-compliant agent executor for Dr. Walter Reed's Interventional Cardiology Practice.
    
    This executor implements the standard A2A SDK patterns with TaskUpdater for:
    - Proper task lifecycle management (submitted → working → completed)
    - Task state transitions and artifact generation
    - Delegation to InterventionalCardiologyAgent for medical logic
    - A2A protocol integration and compliance
    """
    
    def __init__(self):
        """Initialize the interventional cardiology executor."""
        logger.info("Initializing Dr. Walter Reed's Interventional Cardiology Executor")
        
        # Initialize the core medical agent
        self.agent = InterventionalCardiologyAgent()
        
        logger.info(f"Executor initialized for {config.agent.practice_name}")
        logger.info(f"Services: {len(config.agent.primary_services)} primary, {len(config.agent.diagnostic_services)} diagnostic")
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Execute a task using proper A2A SDK patterns with TaskUpdater.
        
        This method follows the standard A2A lifecycle:
        1. Initialize TaskUpdater for proper state management
        2. Submit task (if new) and start work
        3. Delegate medical consultation to agent
        4. Generate artifacts for substantial outputs
        5. Complete task with proper state transitions
        
        Args:
            context: A2A RequestContext containing the incoming message and task info
            event_queue: A2A EventQueue for sending task updates
        """
        # Initialize TaskUpdater for proper A2A state management
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        
        try:
            logger.info(f"Processing message for task {context.task_id}")
            
            # Submit task if new, then start working
            if not context.current_task:
                await updater.submit()
            await updater.start_work()
            
            # Extract user input from message
            user_text = self._extract_text_from_message(context.message)
            if not user_text.strip():
                user_text = "Hello"  # Default greeting
            
            logger.info(f"User query: {user_text[:100]}...")
            
            # Build conversation history for agent context
            conversation_history = self._build_conversation_history(context.current_task)
            
            # Delegate to medical agent for business logic
            response_text = await self.agent.process_medical_consultation(
                user_text, 
                conversation_history
            )
            
            # For now, let's just always send as status message to avoid artifact complexity
            # We can add artifacts later once this works
            await updater.update_status(
                TaskState.working,  # Set state to working while processing response
                message=updater.new_agent_message([Part(root=TextPart(text=response_text))])
            )
            
            # Complete the task
            await updater.complete()
            
            logger.info(f"Successfully completed task {context.task_id}")
            
        except Exception as e:
            logger.error(f"Error processing task {context.task_id}: {str(e)}")
            
            # Handle error by updating task status
            try:
                error_response = (
                    "I apologize, but I'm experiencing technical difficulties. "
                    "Please try again later. For urgent medical matters, please contact "
                    "our office directly."
                )
                await updater.update_status(
                    TaskState.failed,
                    message=updater.new_agent_message([Part(root=TextPart(text=error_response))])
                )
            except Exception as cleanup_error:
                logger.error(f"Error during cleanup: {str(cleanup_error)}")
                raise e
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Handle task cancellation following A2A SDK patterns.
        """
        logger.info(f"Canceling task {context.task_id}")
        # Use TaskUpdater for proper cancellation
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        # The A2A framework handles cancellation responses automatically
    
    def _extract_text_from_message(self, message: Message) -> str:
        """Extract text content from A2A message parts."""
        text_parts = []
        
        for part in message.parts:
            # Simple direct access to text parts
            if hasattr(part, 'text') and part.text:
                text_parts.append(part.text.strip())
        
        return " ".join(text_parts)
    
    def _build_conversation_history(self, current_task) -> List[dict]:
        """Build conversation history for agent context from A2A task history."""
        history = []
        
        # Extract conversation history from task if available
        if current_task and current_task.history:
            for msg in current_task.history:
                content = self._extract_text_from_message(msg)
                if content:
                    if msg.role == "user":
                        history.append({"role": "user", "content": content})
                    elif msg.role == "agent":
                        history.append({"role": "assistant", "content": content})
        
        return history