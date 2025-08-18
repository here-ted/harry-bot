import logging
import platform
import os

logger = logging.getLogger(__name__)
tg_bot_token = os.getenv('TG_BOT_TOKEN', 'your-default-token-for-dev')
news_60_base_array = ['https://60s.viki.moe/v2/60s?encoding=text',
                      'https://60s.b23.run/v2/60s?encoding=text',
                      'https://60s-api-cf.viki.moe/v2/60s?encoding=text',
                      'https://60s-api.114128.xyz/v2/60s?encoding=text',
                      'https://60s-api-cf.114128.xyz/v2/60s?encoding=text']

system = platform.system()
if system == 'Windows':
    os.environ["http_proxy"] = "http://127.0.0.1:10808"
    os.environ["https_proxy"] = "http://127.0.0.1:10808"
elif system == 'Darwin':
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
elif system == 'Linux':
    # 处于生产环境
    pass
else:
    logger.warning('Unknown system %s', system)
