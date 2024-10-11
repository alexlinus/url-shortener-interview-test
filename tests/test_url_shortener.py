import unittest

from exceptions import ShortenUrlNotFound, MaximumLimitOfShortenedUrlsReached
from url_shortener import URLShortener


class TestUrlShortener(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://revolut-shortener.com/"
        self.url_shortener = URLShortener(base_url=self.base_url, maximum_shortened_urls_count=10)

        # Given: some url to shorten
        self.some_url_to_shorten = "https://google.com/?q=412491249494941"

    def test_maximum_shortened_urls_is_reached_error(self):
        for i in range(0, 10):
            self.url_shortener.get_shortened_url(original_url=f"https://google.com/?q={i}")

        with self.assertRaises(MaximumLimitOfShortenedUrlsReached):
            self.url_shortener.get_shortened_url(original_url=f"https://google.com/asfsfe")

    def test_get_original_url_raised_not_found_error(self):
        some_other_shortened_url = "https://fb.com/feed/"

        with self.assertRaises(ShortenUrlNotFound):
            self.url_shortener.get_original_url(some_other_shortened_url)

    def test_get_shortened_url(self):
        # When: we call get_shortened_url from our URLShorter class
        shortened_url = self.url_shortener.get_shortened_url(self.some_url_to_shorten)

        # Then: let's check that our shortened url starts with base_url. Result should be True
        starts_with_base_url: bool = shortened_url.startswith(self.base_url)
        self.assertTrue(starts_with_base_url)

    def test_unique_shortened_urls_from_the_pool(self):
        shortened_urls = [self.url_shortener.get_shortened_url(f"google.com/{i}") for i in range(0, 10)]
        for shortened_url in shortened_urls:
            self.assertIn(shortened_url, self.url_shortener.pool_of_shortened_urls)

    def test_get_original_url(self):
        shortened_url = self.url_shortener.get_shortened_url(original_url=self.some_url_to_shorten)
        original_url = self.url_shortener.get_original_url(shorten_url=shortened_url)

        self.assertEqual(self.some_url_to_shorten, original_url, msg="Both urls should be equal.")

