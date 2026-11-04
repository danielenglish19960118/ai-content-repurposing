"""
Rate Limiter & Token Cost Telemetry Module
"""
import time
from config import config


class TokenRateLimiter:
    def __init__(self, max_tokens_per_min: int = config.MAX_TOKENS_PER_MIN):
        self.max_tokens = max_tokens_per_min
        self.tokens_used_current_minute = 0
        self.last_reset_time = time.time()

    def _reset_if_needed(self):
        now = time.time()
        if now - self.last_reset_time >= 60.0:
            self.tokens_used_current_minute = 0
            self.last_reset_time = now

    def estimate_tokens(self, text: str) -> int:
        """Rough estimation: ~1 token per 4 characters for English / ~1 token per character for CJK."""
        return max(1, len(text) // 3)

    def check_and_track(self, input_text: str) -> tuple[bool, int, float]:
        """
        Tracks estimated token consumption.
        Returns: (is_allowed, estimated_tokens, estimated_cost_usd)
        """
        self._reset_if_needed()
        estimated_tokens = self.estimate_tokens(input_text)
        
        if self.tokens_used_current_minute + estimated_tokens > self.max_tokens:
            return False, estimated_tokens, 0.0

        self.tokens_used_current_minute += estimated_tokens
        estimated_cost = (estimated_tokens / 1000.0) * config.ESTIMATED_COST_PER_1K_TOKENS
        return True, estimated_tokens, estimated_cost
