import random

from exceptions import ShortenUrlNotFound, MaximumLimitOfShortenedUrlsReached
import hashlib


class URLShortener:

    def __init__(self, base_url: str, maximum_shortened_urls_count: int = 10):
        self.base_url = base_url
        self.original_urls_to_shorten = {}
        self.shorten_urls_to_original = {}
        self.maximum_shortened_urls_count = maximum_shortened_urls_count

        # second requirement:
        # to make a pool of shortened urls
        # and get values from there (instead of hashlib.md5)
        self.pool_of_shortened_urls = [f"{self.base_url}/{idx}" for idx in range(self.maximum_shortened_urls_count)]

    def get_original_url(self, shorten_url: str) -> str:
        if shorten_url not in self.shorten_urls_to_original:
            raise ShortenUrlNotFound(f"{shorten_url} is not found!")
        return self.shorten_urls_to_original[shorten_url]

    def get_shortened_url_with_limited_pool(self, original_url: str) -> str:
        """Second requirement to have a pool of pre-generated shortened urls."""
        if original_url in self.original_urls_to_shorten:
            return self.original_urls_to_shorten[original_url]

        if len(self.shorten_urls_to_original) >= self.maximum_shortened_urls_count:
            raise MaximumLimitOfShortenedUrlsReached(f"Limit of {self.maximum_shortened_urls_count} shortened urls is reached!")

        while True:
            random_shortened_url = random.choice(self.pool_of_shortened_urls)
            if random_shortened_url in self.shorten_urls_to_original:
                continue
            break

        self.original_urls_to_shorten[original_url] = random_shortened_url
        self.shorten_urls_to_original[random_shortened_url] = original_url
        return random_shortened_url

    def shorten_url(self, original_url):
        """First implementation"""
        if original_url in self.original_urls_to_shorten:
            return self.original_urls_to_shorten[original_url]

        # there may be collisions (since we trim string by [:6] chars
        short_url = hashlib.md5(original_url.encode()).hexdigest()[:6]

        self.shorten_urls_to_original[short_url] = original_url
        self.original_urls_to_shorten[original_url] = short_url

        return short_url
