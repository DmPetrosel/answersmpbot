import logging
import asyncio
import traceback
import time
def logger_params():
    logdir = 'data'
    logging.basicConfig(
                        filemode='a',
                        filename=f'{logdir}/log.log',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d, %a, %H:%M:%S',
                        force=True)

attempts = 2
logger = logger_params()
async def handle_errors(coroutine, minutes=1, company='unnamed_company'):
    i = 0
    logging.info(f'Company: {company}. Run function {coroutine.func.__module__}.{coroutine.func.__name__}')
    while(i < attempts):    
        i+=1
        try:
            task = asyncio.create_task(coroutine())
            result = await task
            logging.info(f'Company: {company}. Function {coroutine.func.__module__}.{coroutine.func.__name__} is done successfully! (Attempt number {i})')
            return result
        except Exception as e:
            logging.error(f"Company: {company}. In function {coroutine.func.__module__}.{coroutine.func.__name__} error occurs: {e}. Try through {minutes} minutes. (Attempt number {i})\n {traceback.format_exc()}")
            task.cancel()
            try:
                await task
            except Exception:
                pass
            await asyncio.sleep(minutes*60)
    return {}


# usage:
# from functools import partial
    # await handle_errors.handle_errors(partial(function_name, param1, param2, ...), [num_time_to_wait])

def handle_errors_sync(coroutine, minutes=1, company='unnamed_company'):
    i = 0
    logging.info(f'Company: {company}. Run function {coroutine.func.__module__}.{coroutine.func.__name__}')
    while(i < attempts):    
        i+=1
        try:
            result = coroutine()
            logging.info(f'Company: {company}. Function {coroutine.func.__module__}.{coroutine.func.__name__} is done successfully! (Attempt number {i})')
            return result
        except Exception as e:
            logging.error(f"Company: {company}. In function {coroutine.func.__module__}.{coroutine.func.__name__} error occurs: {e}. Try through {minutes} minutes. (Attempt number {i})\n {traceback.format_exc()}")
            
            time.sleep(minutes*60)
    return {}

# usage:
# from functools import partial
    # handle_errors.handle_errors(partial(function_name, param1, param2, ...), [num_time_to_wait][company])
