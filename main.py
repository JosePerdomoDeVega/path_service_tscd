import asyncio
from services.logger.logger import get_logger
from application.return_jobs import return_result_to_gsq
from domain.cache.job_execution_decision import i_can_execute_this_job
from application.providers.cache_provider import get_cache_manager
from application.providers.queue_manager_provider import get_queue_manager
from application.providers.graph_operator_provider import get_graph_operator

logger = get_logger()


async def process_queued_messages(queue_manager, cache_manager, graph_operator):
    with logger.span("Processing queued messages..."):
        for job in queue_manager.get_queued_jobs():
            if await i_can_execute_this_job(job, cache_manager):
                graph_operation_result = graph_operator.execute_job(job)
                print(graph_operation_result)

                if not graph_operation_result.errors:
                    await cache_manager.set_job_status(key=job.job_id, status='done')
                    queue_manager.delete_message(job)
                    logger.info(f"Job {job.job_id} completed successfully")

                logger.info(f"Returning result: {graph_operation_result.result}", **graph_operation_result.to_dict())
                await return_result_to_gsq(graph_operation_result)

            else:
                continue


async def loop():
    with logger.span("Building necessary models graph operations..."):
        cache_manager = get_cache_manager()
        graph_operator = get_graph_operator()
        queue_manager = get_queue_manager()

    while True:
        await process_queued_messages(queue_manager, cache_manager, graph_operator)
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(loop())
