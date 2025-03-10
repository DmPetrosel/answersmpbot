import asyncio
# class TaskManager:
#     _instance = None
#     _lock = asyncio.Lock()
    
#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = cls()
#         return cls._instance
    
#     def __init__(self):
#         self._task_group = None
        
#     async def initialize(self):
#         if self._task_group is None:
#             self._task_group = asyncio.TaskGroup()
        
#     def add_task(self, coro):
#         if self._task_group is None:
#             raise RuntimeError("TaskGroup не инициализирован")
#         return self._task_group.create_task(coro)
        
#     async def shutdown(self):
#         if self._task_group:
#             try:
#             # Ожидаем завершения всех задач
#                 await asyncio.gather(
#                     *[task for task in self._task_group._tasks],
#                     return_exceptions=True
#                 )
#             finally:
#                 self._task_group = None

class TaskManager:
    def __init__(self):
        self.task_group = asyncio.TaskGroup()

    def add_task(self, coro):
        return self.task_group.create_task(coro)

    async def run_tasks(self):
        await self.task_group.complete()