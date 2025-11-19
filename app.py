#!/usr/bin/env python3
import argparse
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class DesignProfile:
    key: str
    name: str
    base_privacy: float     # 0–1
    base_soundness: float   # 0–1
    base_performance: float # 0–1
    description: str


PROFILES: Dict[str, DesignProfile] = {
    "aztec": DesignProfile(
        key="aztec",
        name="Aztec-style zk Rollup",
        base_privacy=0.92,
        base_soundness=0.82,
        base_performance=0.60,
        description="Privacy-first zk rollup with encrypted state and zk proofs.",
    ),
    "zama": DesignProfile(
        key="zama",
        name="Zama-style FHE Layer",
        base_privacy=0.88,
        base_soundness=0.87,
        base_performance=0.45,
        description="FHE compute stack where data and logic remain encrypted.",
    ),
    "soundness": DesignProfile(
        key="soundness",
        name="Soundness-First Protocol Lab",
        base_privacy=0.55,
        base_soundness=0.98,
        base_performance=0.70,
        description="Specification-driven engineering with strong formal proofs.",
    ),
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def score_design(
    profile: DesignProfile,
    uses_zk: bool,
    uses_fhe: bool,
    formal_proofs: bool,
    public_audit: bool,
    chain_type: str,
) -> Dict[str, Any]:
    privacy = profile.base_privacy
    soundness = profile.base_soundness
    performance = profile.base_performance

    if uses_zk:
        privacy += 0.07
        soundness += 0.03
        performance -= 0.03

    if uses_fhe:
        privacy += 0.05
        soundness += 0.04
        performance -= 0.10

    if formal_proofs:
        soundness += 0.12
        performance -= 0.02

    if public_audit:
        soundness += 0.08

    if chain_type == "rollup":
        performance += 0.05
        soundness += 0.02
    elif chain_type == "sidechain":
        performance += 0.08
        soundness -= 0.03
    elif chain_type == "appchain":
        performance += 0.04

    privacy = clamp(privacy)
    soundness = clamp(soundness)
    performance = clamp(performance)

    overall = clamp(0.45 * soundness + 0.35 * privacy + 0.20 * performance)

    grade = "experimental"
    if overall >= 0.80:
        grade = "high assurance"
    elif overall >= 0.65:
        grade = "balanced"
    elif overall >= 0.50:
        grade = "prototype"

    return {
        "profile": profile.key,
        "profileName": profile.name,
        "description": profile.description,
        "usesZk": uses_zk,
        "usesFhe": uses_fhe,
        "formalProofs": formal_proofs,
        "publicAudit": public_audit,
        "chainType": chain_type,
        "privacyScore": round(privacy, 3),
        "soundnessScore": round(soundness, 3),
        "performanceScore": round(performance, 3),
        "overallScore": round(overall, 3),
        "grade": grade,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="web3_design_scorer",
        description=(
            "Score a Web3 design along privacy, soundness, and performance "
            "dimensions, inspired by Aztec, Zama, and soundness-focused labs."
        ),
    )
    parser.add_argument(
        "--style",
        choices=list(PROFILES.keys()),
        default="aztec",
        help="Base design style (aztec, zama, soundness).",
    )
    parser.add_argument(
        "--zk",
        action="store_true",
        help="Project uses zero-knowledge proofs for core logic.",
    )
    parser.add_argument(
        "--fhe",
        action="store_true",
        help="Project uses fully homomorphic encryption (FHE).",
    )
    parser.add_argument(
        "--formal",
        action="store_true",
        help="Project relies on formal verification / machine-checked proofs.",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Project has a public, independent audit.",
    )
    parser.add_argument(
        "--chain-type",
        choices=["rollup", "sidechain", "appchain", "other"],
        default="rollup",
        help="Deployment model (rollup, sidechain, appchain, other).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of human-readable text.",
    )
    return parser.parse_args()


def print_human(result: Dict[str, Any]) -> None:
    print("🔍 Web3 Design Score")
    print(f"Base Style   : {result['profileName']} ({result['profile']})")
    print(f"Description  : {result['description']}")
    print("")
    print("Features:")
    print(f"  Uses ZK proofs       : {'yes' if result['usesZk'] else 'no'}")
    print(f"  Uses FHE             : {'yes' if result['usesFhe'] else 'no'}")
    print(f"  Formal verification  : {'yes' if result['formalProofs'] else 'no'}")
    print(f"  Public audit         : {'yes' if result['publicAudit'] else 'no'}")
    print(f"  Chain type           : {result['chainType']}")
    print("")
    print("Scores (0–1):")
    print(f"  Privacy              : {result['privacyScore']:.3f}")
    print(f"  Soundness            : {result['soundnessScore']:.3f}")
    print(f"  Performance          : {result['performanceScore']:.3f}")
    print("")
    print(f"Overall Score          : {result['overallScore']:.3f}")
    print(f"Design Grade           : {result['grade']}")


def main() -> None:
    args = parse_args()
    profile = PROFILES[args.style]

    result = score_design(
        profile=profile,
        uses_zk=args.zk,
        uses_fhe=args.fhe,
        formal_proofs=args.formal,
        public_audit=args.audit,
        chain_type=args.chain_type,
    )

    if args.json:
        import json

        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
