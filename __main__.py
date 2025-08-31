"""
Dr. Walter Reed's Interventional Cardiology A2A Agent
Main Application Entry Point

This is the main entry point for Dr. Walter Reed's Interventional Cardiology
A2A Agent. It sets up the A2A server using the official SDK, configures the
agent with specialized interventional cardiology skills, and starts the server.

Features:
- Official A2A SDK integration with full protocol compliance
- Specialized interventional cardiology skills and capabilities
- Comprehensive configuration management (no hardcoded values)
- Professional medical communication standards
- Security validation and input protection
- Server-Sent Events (SSE) streaming support

Usage:
    python __main__.py

Environment Variables:
    ANTHROPIC_API_KEY: Claude API key (required)
    PORT: Server port (default: 9999)
    HOST: Server host (default: 0.0.0.0)
    DEBUG: Enable debug mode (default: false)
    
    See config.py for complete configuration options.
"""

import os
import sys
import logging
import asyncio
from typing import List

# Configure logging before other imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Import A2A SDK components
    from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
    from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
    from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
    from a2a.types import (
        AgentCapabilities,
        AgentCard,
        AgentSkill,
    )
    
    # Import our custom components
    from agent_executor import InterventionalCardiologyExecutor
    from config import config
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure you have activated the virtual environment and installed all dependencies")
    sys.exit(1)

def create_interventional_cardiology_skills() -> List[AgentSkill]:
    """
    Create specialized skills for Dr. Walter Reed's Interventional Cardiology practice.
    
    These skills are configured based on the practice's specialization in:
    - Advanced interventional procedures
    - Heart failure management
    - Comprehensive cardiac diagnostics
    - Professional healthcare coordination
    """
    
    skills = []
    
    # Interventional Procedures Skill
    interventional_skill = AgentSkill(
        id='interventional_procedures',
        name='Interventional Cardiology Procedures',
        description=(
            'Coordinate and provide information about advanced interventional '
            'cardiology procedures including angiography, angioplasty, stenting, '
            'and complex coronary interventions'
        ),
        tags=['interventional', 'angiography', 'angioplasty', 'stenting', 'procedures'],
        examples=[
            'I need information about angiography procedures',
            'Can you coordinate an angioplasty consultation?',
            'What does the stent placement procedure involve?',
            'Schedule interventional cardiology evaluation'
        ]
    )
    skills.append(interventional_skill)
    
    # Heart Failure Management Skill  
    heart_failure_skill = AgentSkill(
        id='heart_failure_management',
        name='Heart Failure Management',
        description=(
            'Provide coordination and information for comprehensive heart failure '
            'management, including optimization therapy, monitoring protocols, '
            'and advanced treatment options'
        ),
        tags=['heart failure', 'management', 'optimization', 'monitoring'],
        examples=[
            'Heart failure management consultation needed',
            'What are the latest heart failure treatment protocols?', 
            'Coordinate heart failure monitoring program',
            'Advanced heart failure therapy options'
        ]
    )
    skills.append(heart_failure_skill)
    
    # Ischemic Heart Disease Skill
    ihd_skill = AgentSkill(
        id='ischemic_heart_disease',
        name='Ischemic Heart Disease Treatment',
        description=(
            'Coordinate treatment and management of ischemic heart disease, '
            'including acute coronary syndromes, chronic CAD, and secondary '
            'prevention protocols'
        ),
        tags=['ischemic', 'CAD', 'coronary', 'acute coronary syndrome'],
        examples=[
            'Ischemic heart disease evaluation needed',
            'Acute coronary syndrome management',
            'Chronic CAD treatment coordination',
            'Secondary prevention protocol information'
        ]
    )
    skills.append(ihd_skill)
    
    # Stroke Prevention and Management Skill
    stroke_skill = AgentSkill(
        id='stroke_prevention_management',
        name='Stroke Prevention and Management',
        description=(
            'Coordinate stroke prevention strategies and acute stroke management '
            'in the context of cardiovascular disease, including anticoagulation '
            'and risk factor modification'
        ),
        tags=['stroke', 'prevention', 'management', 'anticoagulation'],
        examples=[
            'Stroke prevention consultation needed',
            'Anticoagulation management for stroke prevention',
            'Cardiovascular stroke risk assessment',
            'Acute stroke management protocols'
        ]
    )
    skills.append(stroke_skill)
    
    # Diagnostic Services Skill
    diagnostic_skill = AgentSkill(
        id='cardiac_diagnostics',
        name='Comprehensive Cardiac Diagnostics',
        description=(
            'Coordinate comprehensive cardiac diagnostic services including '
            'stress testing, electrocardiography, echocardiography, and '
            'cardiac catheterization procedures'
        ),
        tags=['diagnostics', 'stress test', 'ECG', 'echo', 'catheterization'],
        examples=[
            'Schedule cardiac stress test',
            'ECG interpretation consultation needed',
            '2D echocardiography with Doppler',
            'Cardiac catheterization procedure coordination'
        ]
    )
    skills.append(diagnostic_skill)
    
    logger.info(f"Created {len(skills)} specialized interventional cardiology skills")
    return skills

def create_agent_card() -> AgentCard:
    """
    Create the A2A Agent Card for Dr. Walter Reed's Interventional Cardiology practice.
    
    The Agent Card serves as the "business card" for the agent, describing its
    identity, capabilities, skills, and how other agents can interact with it.
    """
    
    # Create specialized skills
    skills = create_interventional_cardiology_skills()
    
    # Get agent card data from configuration
    card_data = config.get_agent_card_data()
    
    # Create Agent Card with interventional cardiology specialization
    agent_card = AgentCard(
        name=card_data["name"],
        description=card_data["description"],
        url=card_data["url"],
        version=card_data["version"],
        defaultInputModes=card_data["defaultInputModes"],
        defaultOutputModes=card_data["defaultOutputModes"],
        capabilities=AgentCapabilities(
            streaming=card_data["capabilities"]["streaming"],
            pushNotifications=card_data["capabilities"]["pushNotifications"]
        ),
        skills=skills,
        # Additional metadata for medical specialization
        metadata={
            "specialization": "interventional_cardiology",
            "practice_name": config.agent.practice_name,
            "medical_focus": "advanced_cardiac_procedures",
            "target_users": ["healthcare_providers", "medical_coordinators", "specialist_referrals"]
        }
    )
    
    logger.info(f"Created agent card for {agent_card.name}")
    logger.info(f"Agent URL: {agent_card.url}")
    logger.info(f"Skills: {len(agent_card.skills)}")
    
    return agent_card

def create_a2a_application() -> A2AStarletteApplication:
    """
    Create the A2A Starlette application with proper configuration.
    
    This sets up the complete A2A server infrastructure including:
    - Agent card configuration
    - Request handling with our custom executor
    - Task storage management
    - Security and validation
    """
    
    logger.info("Creating A2A Starlette application...")
    
    # Create the agent card
    agent_card = create_agent_card()
    
    # Create the custom request handler with our interventional cardiology executor
    request_handler = DefaultRequestHandler(
        agent_executor=InterventionalCardiologyExecutor(),
        task_store=InMemoryTaskStore()  # In-memory storage for Phase 1
    )
    
    # Create the A2A Starlette application
    app_builder = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    
    logger.info("A2A application created successfully")
    return app_builder

def main():
    """
    Main entry point for Dr. Walter Reed's Interventional Cardiology A2A Agent.
    
    This function:
    1. Validates configuration and environment
    2. Creates the A2A application with specialized medical skills
    3. Starts the server with proper logging and error handling
    """
    
    logger.info("=" * 80)
    logger.info("Dr. Walter Reed's Interventional Cardiology A2A Agent")
    logger.info("=" * 80)
    
    # Validate configuration
    try:
        config.print_config_summary()
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        logger.error("Please check your environment variables and configuration")
        sys.exit(1)
    
    # Validate required environment variables
    if not config.claude.api_key:
        logger.error("ANTHROPIC_API_KEY environment variable is required")
        logger.error("Please set your Claude API key before starting the agent")
        sys.exit(1)
    
    try:
        # Create the A2A application
        app_builder = create_a2a_application()
        app = app_builder.build()
        
        # Start the server
        logger.info(f"Starting server on {config.server.host}:{config.server.port}")
        logger.info(f"Agent card will be available at: {config.server.base_url}/.well-known/agent-card.json")
        logger.info(f"A2A endpoint: {config.server.base_url}/")
        logger.info(f"Debug mode: {config.server.debug}")
        
        # Import and start uvicorn
        import uvicorn
        
        uvicorn.run(
            app,
            host=config.server.host,
            port=config.server.port,
            log_level=config.server.log_level,
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error starting server: {e}")
        logger.error("Check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()