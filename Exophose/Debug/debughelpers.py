import traceback
import functools

async def try_func(include_embed: bool, func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        if (logging := args[0].bot.get_cog("Logging")) is not None:
            await logging.log_error(e, f'{args[0].__cog_name__} - {func.__name__}', traceback.format_exc())
    
    if include_embed:
        if (embeds := args[0].bot.get_cog("Embeds")) is not None:
            return embeds.unexpected_error()

def try_func_async(embed: bool = False):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            return await try_func(embed, func, *args, **kwargs)
        return wrapped
    return wrapper