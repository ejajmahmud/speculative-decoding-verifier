"""Core Speculative Decoding Verifier implementation."""
import math
import random
from typing import Dict, List, Tuple, Optional, Any


class VerificationResult:
    def __init__(self, accepted_tokens: List[str], rejected_index: Optional[int], bonus_token: Optional[str], speedup_factor: float):
        self.accepted_tokens = accepted_tokens
        self.rejected_index = rejected_index
        self.bonus_token = bonus_token
        self.speedup_factor = speedup_factor


class SpeculativeVerifier:
    def __init__(self, temperature: float = 1.0):
        self.temperature = max(0.01, temperature)
        self.total_draft_tokens = 0
        self.total_accepted_tokens = 0

    def verify_tokens(
        self,
        draft_tokens: List[str],
        draft_probs: List[float],
        target_probs: List[float],
        recovery_token: str = "corrected_tok"
    ) -> VerificationResult:
        accepted = []
        rejected_idx = None

        for i, (tok, p_draft, p_target) in enumerate(zip(draft_tokens, draft_probs, target_probs)):
            self.total_draft_tokens += 1
            # Standard speculative rejection sampling criterion:
            # Accept if p_target >= p_draft, or accept with probability p_target / p_draft
            if p_target >= p_draft:
                accepted.append(tok)
                self.total_accepted_tokens += 1
            else:
                ratio = p_target / max(1e-6, p_draft)
                if random.random() < ratio:
                    accepted.append(tok)
                    self.total_accepted_tokens += 1
                else:
                    rejected_idx = i
                    break

        bonus = recovery_token if rejected_idx is not None else None
        generated_count = len(accepted) + (1 if bonus else 0)
        speedup = generated_count / 1.0  # Normalized to 1 target forward pass

        return VerificationResult(accepted, rejected_idx, bonus, speedup)

    @property
    def acceptance_rate(self) -> float:
        if self.total_draft_tokens == 0:
            return 0.0
        return self.total_accepted_tokens / self.total_draft_tokens
