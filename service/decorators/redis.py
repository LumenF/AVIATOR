from AVIATOR.settings import s_redis_user


def redis_delete_user(function):
    def wrapper(*args, **kwargs):
        msg = function(*args)
        if 'tg_id' in args[0].__dict__ and args[0].__dict__['tg_id'] is not None:
            tg_id = args[0].tg_id
            s_redis_user.delete(tg_id)
        return msg

    return wrapper
