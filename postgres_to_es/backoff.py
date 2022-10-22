from functools import wraps
from time import sleep
import logging


logger = logging.getLogger('my_log_lord')


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100):
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост времени
    повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = start_sleep_time

            while start < border_sleep_time:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    start = start * 2**factor
                    if start > border_sleep_time:
                        start = float(border_sleep_time)
                    logger.exception(exc)
                    logger.warning('WOW! У нас тут падения,'
                                   'благо на подушки! Сейчас поднимем!')
                    logger.warning(f'Попробуем еще раз через {start}c.')
                    sleep(start)
            else:
                logger.error('Очень жаль, но не получилось :/')
                logger.error('Зовите программиста, все упало :/')

        return inner

    return func_wrapper
