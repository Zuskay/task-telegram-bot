from pathlib import Path
from typing import Optional

from cel.assistants.macaw.macaw_assistant import MacawAssistant  
from cel.prompt.prompt_template import PromptTemplate  
from cel.stores.state.state_redis_provider import RedisStateProvider  
from langchain_openai import ChatOpenAI  
  
from src.config import settings  
from src.tools.task_tools import TaskTools

class TaskAssistant:
    """ Task management assistant with CRUD operations """

    def __init__(self) -> None:
        """ Initialize the task assistant with LLM and tools """
        # Load system prompt from file
        prompt_path = Path(__file__).parent.parent.parent /"prompts" / "task_manager_prompt.txt"
        system_prompt = prompt_path.read_text(encoding="utf-8")

        # Create prompt template
        prompt_template = PromptTemplate(system_prompt)

        # Configure OpenAI LLM with specified model and fallback
        llm = self._create_llm()

        # Create redis state provider for persistence
        state_provider = RedisStateProvider(redis_url=settings.redis_url)

        # Initialize MacawAssistant
        self.assistant = MacawAssistant(
            prompt=prompt_template,
            llm=llm,
            state_store=state_provider
        )

        # Register task management tools
        self._register_tools()

    def _create_llm(self) -> ChatOpenAI:
            """ Create OpenAI LLM with specified model and fallback """
            # Try to use the specified model, fallback to gpt-4o-mini if not available
            model_name ="gpt-4.1-nano-2025-04-14"

            try:
                llm = ChatOpenAI(
                    model=model_name,
                    temperature=0.3,
                    streaming = True,
                    api_key=settings.openai_api_key
                )
                return llm
            except Exception:
                # Fallback to gpt-4o-mini if specified model is not available
                llm = ChatOpenAI(
                    model="gpt-4o-mini",  
                    temperature=0.3,  
                    streaming=True,  
                    api_key=settings.openai_api_key 
                )
                return llm
                
    def _register_tools(self) -> None:  
        """Register all task management tools with the assistant."""  
        task_tools = TaskTools()  
          
        # Register each tool as a function  
        self.assistant.function("add_task")(task_tools.add_task)  
        self.assistant.function("list_tasks")(task_tools.list_tasks)  
        self.assistant.function("update_task")(task_tools.update_task)  
        self.assistant.function("delete_task")(task_tools.delete_task)  
      
    def get_assistant(self) -> MacawAssistant:  
        """Get the configured MacawAssistant instance."""  
        return self.assistant   