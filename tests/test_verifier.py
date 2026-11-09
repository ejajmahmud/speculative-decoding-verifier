"""Unit tests for speculative-decoding-verifier."""
import unittest
from speculative_decoding_verifier.verifier import SpeculativeVerifier


class TestSpeculativeVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = SpeculativeVerifier()

    def test_all_accepted_when_target_higher(self):
        draft = ["a", "b", "c"]
        p_d = [0.5, 0.5, 0.5]
        p_t = [0.8, 0.9, 0.7]

        res = self.verifier.verify_tokens(draft, p_d, p_t)
        self.assertEqual(res.accepted_tokens, ["a", "b", "c"])
        self.assertIsNone(res.rejected_index)
        self.assertEqual(res.speedup_factor, 3.0)

    def test_rejection_at_zero_probability(self):
        draft = ["x", "y"]
        p_d = [0.9, 0.9]
        p_t = [0.95, 0.0]  # y will be rejected

        res = self.verifier.verify_tokens(draft, p_d, p_t)
        self.assertEqual(res.accepted_tokens, ["x"])
        self.assertEqual(res.rejected_index, 1)
        self.assertIsNotNone(res.bonus_token)
