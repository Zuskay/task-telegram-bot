from pathlib import Path  
from typing import Optional  
  
from cel.assistants.macaw.macaw_assistant import MacawAssistant    
from cel.prompt.prompt_template import PromptTemplate 
from cel.assistants.common import Param
from cel.assistants.function_context import FunctionContext     
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
  
        # Initialize MacawAssistant without explicit LLM (let cel handle it internally)
        self.assistant = MacawAssistant(  
            prompt=prompt_template
        )  
        
        # Initialize task tools
        self.task_tools = TaskTools()
  
        # Register task management tools  
        self._register_tools()  
                  
    def _register_tools(self) -> None:  
        """Register all task management tools with the assistant."""  
        
        # Register add_task function  
        self.assistant.function(  
            "add_task",  
            "Add a new task with title, description, and completion status",  
            [  
                Param("title", "string", "Task title", required=True),  
                Param("description", "string", "Task description", required=True),  
                Param("completed", "boolean", "Task completion status", required=True)  
            ]  
        )(self._create_add_task_handler())
        
        # Register list_tasks function  
        self.assistant.function(  
            "list_tasks",  
            "List all tasks for the current user",  
            []  
        )(self._create_list_tasks_handler())
        
        # Register update_task function  
        self.assistant.function(  
            "update_task",  
            "Update an existing task",  
            [  
                Param("task_id", "integer", "Task ID to update", required=True),  
                Param("title", "string", "New task title", required=False),  
                Param("description", "string", "New task description", required=False),  
                Param("completed", "boolean", "New completion status", required=False)  
            ]  
        )(self._create_update_task_handler())
        
        # Register delete_task function  
        self.assistant.function(  
            "delete_task",  
            "Delete a task by ID",  
            [  
                Param("task_id", "integer", "Task ID to delete", required=True)  
            ]  
        )(self._create_delete_task_handler())
    
    def _create_add_task_handler(self):
        """Create the add_task handler function"""
        async def handle_add_task(session, params, ctx: FunctionContext):
            try:
                user_id = str(ctx.lead.conversation_from.id)
                title = params.get('title')
                description = params.get('description')
                completed = params.get('completed')
                
                task_id = self.task_tools.add_task(user_id, title, description, completed)
                return ctx.response_text(f"Tarea agregada exitosamente con ID: {task_id}")
            except Exception as e:
                return ctx.response_text(f"Error al agregar tarea: {str(e)}")
        return handle_add_task
    
    def _create_list_tasks_handler(self):
        """Create the list_tasks handler function"""
        async def handle_list_tasks(session, params, ctx: FunctionContext):
            try:
                user_id = str(ctx.lead.conversation_from.id)
                tasks = self.task_tools.get_tasks_for_user(user_id)
                
                if not tasks:
                    return ctx.response_text("No tienes tareas registradas")
                
                result = "**Tus Tareas:**\n\n"
                for task in tasks:
                    status = "✅" if task["completed"] else "⏳"
                    short_desc = task["description"][:30] + "..." if len(task["description"]) > 30 else task["description"]
                    result += f"{status} **ID {task['id']}** | {task['title']} | {short_desc}\n"
                
                return ctx.response_text(result)
            except Exception as e:
                return ctx.response_text(f"Error al listar tareas: {str(e)}")
        return handle_list_tasks
    
    def _create_update_task_handler(self):
        """Create the update_task handler function"""
        async def handle_update_task(session, params, ctx: FunctionContext):
            try:
                user_id = str(ctx.lead.conversation_from.id)
                task_id = params.get('task_id')
                title = params.get('title')
                description = params.get('description')
                completed = params.get('completed')
                
                success = self.task_tools.update_task_for_user(user_id, task_id, title, description, completed)
                if success:
                    return ctx.response_text(f"Tarea {task_id} actualizada exitosamente.")
                else:
                    return ctx.response_text(f"No se encontró la tarea con ID: {task_id}")
            except Exception as e:
                return ctx.response_text(f"Error al actualizar tarea: {str(e)}")
        return handle_update_task
    
    def _create_delete_task_handler(self):
        """Create the delete_task handler function"""
        async def handle_delete_task(session, params, ctx: FunctionContext):
            try:
                user_id = str(ctx.lead.conversation_from.id)
                task_id = params.get('task_id')
                
                success = self.task_tools.delete_task_for_user(user_id, task_id)
                if success:
                    return ctx.response_text(f"Tarea {task_id} eliminada exitosamente.")
                else:
                    return ctx.response_text(f"No se encontró la tarea con ID: {task_id}")
            except Exception as e:
                return ctx.response_text(f"Error al eliminar tarea: {str(e)}")
        return handle_delete_task