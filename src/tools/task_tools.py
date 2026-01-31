from typing import List, Dict, Any, Optional
from langchain_core.tools import tool

from src.storage.redis_tasks import RedisTasks

class TaskTools:
    """ Collection of task management tools """

    def __init__(self) -> None:
        """ Initialize task tools with Redis storage """
        self.redis_tasks = RedisTasks()

    @tool
    def add_task(self, user_id: str, title: str, description: str, completed: bool) -> str:
        """ Add a new task to the user's task list
        
        Arg:
            user_id: Telegram user ID
            title: Task title
            description: Task description
            completed: Wheter the task is completed
        
        Returns:
            Success message with task ID
        """

        try:
            task_id = self.redis_tasks.add_task(user_id, title, description, completed)
            return f"Tarea agregada exitosamente con ID: {task_id}"
        except Exception as e:
            return f"Error al agregar tarea: {str(e)}"

    @tool
    def list_tasks(self, user_id: str) -> str:
        """ List all tasks for the user
        
        Args:
            user_id: Telegram user ID

        Returns:
            Formatted list of tasks
        """
        
        try:
            tasks = self.redis_tasks.get_tasks(user_id)
            if not tasks:
                return "No tienes tareas registradas"
            
            result = "**Tus Tareas:**\n\n"
            for task in tasks:
                status = "✅" if task["completed"] else "⏳"
                # truncate description for display
                short_desc = task["description"][:30] + "..." if len(task["description"]) > 30 else task["description"]
                result += f"{status} **ID {task['id?']}** | {task['title']} | {short_desc}\n"
            
            return result
        except Exception as e:
            return f"Error al listar tareas: {str(e)}"
        
    @tool
    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> str:
        """ Update an existing task.  
          
        Args:  
            user_id: Telegram user ID  
            task_id: ID of the task to update  
            title: New title (optional)  
            description: New description (optional)  
            completed: New completion status (optional)  
              
        Returns:  
            Success or error message  
        """
        try:  
            success = self.redis_tasks.update_task(user_id, task_id, title, description, completed)  
            if success:  
                return f"Tarea {task_id} actualizada exitosamente."  
            else:  
                return f"No se encontró la tarea con ID: {task_id}"  
        except Exception as e:  
            return f"Error al actualizar tarea: {str(e)}"  
      
    @tool  
    def delete_task(self, user_id: str, task_id: int) -> str:  
        """Delete a task by ID.  
          
        Args:  
            user_id: Telegram user ID  
            task_id: ID of the task to delete  
              
        Returns:  
            Success or error message  
        """  
        try:  
            success = self.redis_tasks.delete_task(user_id, task_id)  
            if success:  
                return f"Tarea {task_id} eliminada exitosamente."  
            else:  
                return f"No se encontró la tarea con ID: {task_id}"  
        except Exception as e:  
            return f"Error al eliminar tarea: {str(e)}"
        