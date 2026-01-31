import json
import redis
from typing import List, Dict, Any, Optional

class RedisTasks:
    """ Redis-based task storage with per-user isolation"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0") -> None:
        """ Initialize Redis connection.

        Args:
            redis_url: Redis connection URL
        """

        self.redis_url = redis_url
        self._redis_client: Optional[redis.Redis] = None

    def _get_redis(self) -> redis.Redis:
        """ Get redis connection """

        if self._redis_client is None:
            self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis_client
    
    def _get_user_key(self, user_id: str) -> str:
        """ Generate redis key for user's tasks.
        
        Args:
            user_id: User identifier

        Returns:
            Redis key for user's tasks
        """
        return f"tasks:{user_id}"
    
    def _get_next_id_key(self, user_id: str) -> str:  
        """Generate Redis key for user's next task ID.  
          
        Args:  
            user_id: User identifier  
              
        Returns:  
            Redis key for next task ID  
        """  
        return f"tasks:{user_id}:next_id"  
      
    def add_task(self, user_id: str, title: str, description: str, completed: bool) -> int:  
        """Add a new task for the user.  
          
        Args:  
            user_id: User identifier  
            title: Task title  
            description: Task description  
            completed: Whether the task is completed  
              
        Returns:  
            New task ID  
        """  
        client = self._get_redis()  
        user_key = self._get_user_key(user_id)  
        next_id_key = self._get_next_id_key(user_id)  
          
        # Get next task ID (auto-incremental)  
        task_id = client.incr(next_id_key)  
          
        # Create task object  
        task = {  
            "id": task_id,  
            "title": title,  
            "description": description,  
            "completed": completed  
        }  
          
        # Get existing tasks  
        tasks_json = client.get(user_key)  
        tasks = json.loads(tasks_json) if tasks_json else []  
          
        # Add new task  
        tasks.append(task)  
          
        # Save back to Redis  
        client.set(user_key, json.dumps(tasks))  
          
        return task_id  
      
    def get_tasks(self, user_id: str) -> List[Dict[str, Any]]:  
        """Get all tasks for the user.  
          
        Args:  
            user_id: User identifier  
              
        Returns:  
            List of tasks  
        """  
        try:
            client = self._get_redis()  
            user_key = self._get_user_key(user_id)  
              
            tasks_json = client.get(user_key)
            if not tasks_json:
                return []
            return json.loads(tasks_json)
        except Exception:
            return []  
      
    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None,  
                    description: Optional[str] = None, completed: Optional[bool] = None) -> bool:  
        """Update an existing task.  
          
        Args:  
            user_id: User identifier  
            task_id: Task ID to update  
            title: New title (optional)  
            description: New description (optional)  
            completed: New completion status (optional)  
              
        Returns:  
            True if task was updated, False if not found  
        """  
        client = self._get_redis()  
        user_key = self._get_user_key(user_id)  
          
        # Get existing tasks  
        tasks_json = client.get(user_key)  
        if not tasks_json:  
            return False  
          
        tasks = json.loads(tasks_json)  
          
        # Find and update the task  
        for task in tasks:  
            if task["id"] == task_id:  
                if title is not None:  
                    task["title"] = title  
                if description is not None:  
                    task["description"] = description  
                if completed is not None:  
                    task["completed"] = completed  
                  
                # Save updated tasks  
                client.set(user_key, json.dumps(tasks))  
                return True  
          
        return False  
      
    def delete_task(self, user_id: str, task_id: int) -> bool:  
        """Delete a task by ID.  
          
        Args:  
            user_id: User identifier  
            task_id: Task ID to delete  
              
        Returns:  
            True if task was deleted, False if not found  
        """  
        client = self._get_redis()  
        user_key = self._get_user_key(user_id)  
          
        # Get existing tasks  
        tasks_json = client.get(user_key)  
        if not tasks_json:  
            return False  
          
        tasks = json.loads(tasks_json)  
          
        # Remove the task  
        original_length = len(tasks)  
        tasks = [task for task in tasks if task["id"] != task_id]  
          
        if len(tasks) == original_length:  
            return False  # Task not found  
          
        # Save updated tasks  
        client.set(user_key, json.dumps(tasks))  
        return True  
      
    def close(self) -> None:  
        """Close Redis connection."""  
        if self._redis_client:  
            self._redis_client.close()
    
