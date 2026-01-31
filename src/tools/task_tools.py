from typing import List, Dict, Any, Optional
from src.storage.redis_tasks import RedisTasks

class TaskTools:
    """ Collection of task management tools """

    def __init__(self) -> None:
        """ Initialize task tools with Redis storage """
        self.redis_tasks = RedisTasks()

    def add_task(self, user_id: str, title: str, description: str, completed: bool) -> str:
        """ Add a new task to the user's task list
        
        Args:
            user_id: Telegram user ID
            title: Task title
            description: Task description
            completed: Whether the task is completed
        
        Returns:
            Task ID as string
        """
        try:
            task_id = self.redis_tasks.add_task(user_id, title, description, completed)
            return str(task_id)
        except Exception as e:
            raise Exception(f"Error al agregar tarea: {str(e)}")

    def get_tasks_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """ Get all tasks for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            List of tasks
        """
        try:
            tasks = self.redis_tasks.get_tasks(user_id)
            return tasks if tasks else []
        except Exception as e:
            raise Exception(f"Error al listar tareas: {str(e)}")
        
    def update_task_for_user(self, user_id: str, task_id: int, title: Optional[str] = None, 
                            description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """ Update an existing task.  
          
        Args:  
            user_id: Telegram user ID
            task_id: ID of the task to update  
            title: New title (optional)  
            description: New description (optional)  
            completed: New completion status (optional)  
              
        Returns:  
            True if successful, False otherwise
        """
        try:
            success = self.redis_tasks.update_task(user_id, task_id, title, description, completed)
            return success
        except Exception as e:
            raise Exception(f"Error al actualizar tarea: {str(e)}")
      
    def delete_task_for_user(self, user_id: str, task_id: int) -> bool:  
        """Delete a task by ID.  
          
        Args:  
            user_id: Telegram user ID
            task_id: ID of the task to delete  
              
        Returns:  
            True if successful, False otherwise
        """  
        try:
            success = self.redis_tasks.delete_task(user_id, task_id)
            return success
        except Exception as e:
            raise Exception(f"Error al eliminar tarea: {str(e)}")
        