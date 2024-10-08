import time
import ujson as json

from aiohttp import ClientError
from .log import log
from .stack_error import stack_error


async def check_github_api_rate_limit(headers, session):
    try:
        url = 'https://api.github.com/rate_limit'

        async with session.get(url, headers=headers, ssl=False) as r:
            r_json = await r.json()

            if r.status == 200:
                rate_limit = r_json['rate']
                remaining_requests = rate_limit['remaining']
                reset_time = rate_limit['reset']
                reset_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))
                log.info(f' 🔄 剩余请求次数: {remaining_requests}')
            else:
                log.error('⚠ Github请求数检查失败，网络错误')

        if remaining_requests == 0:
            log.warning(f'⚠ GitHub API 请求数已用尽，将在 {reset_time_formatted} 重置, 不想等生成一个填配置文件里')
    except ClientError as e:
        log.error(f'⚠ 检查Github API 请求数失败，{stack_error(e)}')