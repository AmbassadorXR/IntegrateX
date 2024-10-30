import aiohttp
import logging_config

GITHUB_API_URL = "https://api.github.com"

logger = logging_config.get_logger(__name__)


async def fetch_repos(username):
    logger.info(f"Fetching repos for user: {username}")
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return None
