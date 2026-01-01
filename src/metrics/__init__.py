"""
Metrics store for the Enterprise AI Gateway
"""

from dataclasses import dataclass, field
from typing import Dict, List
import threading


@dataclass
class MetricsStore:
    """Thread-safe metrics store for tracking gateway performance"""

    total_requests: int = 0
    successful_requests: int = 0
    blocked_requests: int = 0
    total_latency_ms: int = 0
    provider_usage: Dict[str, int] = field(default_factory=dict)
    cascade_failures: int = 0
    pii_detections: int = 0
    injection_detections: int = 0
    latency_history: List[int] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record_request(
        self,
        provider: str = None,
        latency_ms: int = 0,
        blocked: bool = False,
        pii_detected: bool = False,
        injection_detected: bool = False,
        cascade_failed: bool = False
    ):
        """Record a request with its metrics"""
        with self._lock:
            self.total_requests += 1

            if blocked:
                self.blocked_requests += 1
            else:
                self.successful_requests += 1
                self.total_latency_ms += latency_ms
                self.latency_history.append(latency_ms)
                # Keep only last 100 latency measurements
                if len(self.latency_history) > 100:
                    self.latency_history.pop(0)

            if provider:
                self.provider_usage[provider] = self.provider_usage.get(provider, 0) + 1

            if pii_detected:
                self.pii_detections += 1

            if injection_detected:
                self.injection_detections += 1

            if cascade_failed:
                self.cascade_failures += 1

    def to_dict(self) -> dict:
        """Return metrics as a dictionary"""
        with self._lock:
            avg_latency = (
                self.total_latency_ms / self.successful_requests
                if self.successful_requests > 0
                else 0
            )
            return {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "blocked_requests": self.blocked_requests,
                "average_latency_ms": round(avg_latency, 2),
                "provider_usage": dict(self.provider_usage),
                "cascade_failures": self.cascade_failures,
                "pii_detections": self.pii_detections,
                "injection_detections": self.injection_detections,
                "latency_history": list(self.latency_history[-20:]),
            }

    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self.total_requests = 0
            self.successful_requests = 0
            self.blocked_requests = 0
            self.total_latency_ms = 0
            self.provider_usage = {}
            self.cascade_failures = 0
            self.pii_detections = 0
            self.injection_detections = 0
            self.latency_history = []


# Singleton instance
metrics = MetricsStore()
