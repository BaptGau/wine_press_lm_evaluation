from asyncio import TaskGroup
from typing import List, Dict, Any


async def run_parallel_execution(coro, n_evaluations: int) -> List[Dict[str, Any]]:
    async with TaskGroup() as group:
        tasks = [
            group.create_task(
                coro()
            )
            for _ in range(n_evaluations)
        ]

    return [task.result() for task in tasks]
