"""CLI for speculative-decoding-verifier."""
import sys
import argparse
from .verifier import SpeculativeVerifier


def main():
    parser = argparse.ArgumentParser(description="Speculative Decoding Verifier CLI")
    parser.add_argument("--demo", action="store_true", help="Run speculative verification simulation")
    args = parser.parse_args()

    if args.demo:
        verifier = SpeculativeVerifier()
        draft = ["async", " def", " execute", "_query"]
        p_draft = [0.95, 0.90, 0.85, 0.30]
        p_target = [0.98, 0.92, 0.80, 0.10]

        res = verifier.verify_tokens(draft, p_draft, p_target)
        print("Speculative Decoding Verification Result:")
        print(f"  Accepted Tokens: {res.accepted_tokens}")
        print(f"  Rejected at index: {res.rejected_index}")
        print(f"  Bonus Correction Token: {res.bonus_token}")
        print(f"  Speedup Factor: {res.speedup_factor:.2f}x")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
