# web3_design_scorer

A tiny CLI tool that assigns a simple privacy, soundness, and performance score to a Web3 protocol design.  
The scoring model is inspired by ecosystems and ideas around Aztec-style zk rollups, Zama-style FHE stacks, and soundness-first formal verification labs.

There are exactly two files in this repository:
- app.py
- README.md


## Concept

The tool helps you reason about architectural trade-offs for a Web3 project:

- Does your design use zero-knowledge proofs like Aztec does for private rollups?
- Are you experimenting with fully homomorphic encryption like Zama?
- Are you investing heavily in formal proofs and soundness like verification-focused labs?

Given a few boolean flags and a base style, the script computes three scores between 0 and 1:

- privacyScore
- soundnessScore
- performanceScore

It then aggregates them into an overallScore and a simple design grade such as experimental, prototype, balanced, or high assurance.


## Installation

Requirements:
- Python 3.10 or newer

Steps:

1. Create a new GitHub repository with any name.
2. Place app.py and this README.md in the root directory.
3. Ensure python is available on your system PATH.
4. No extra dependencies are required; the script uses only the Python standard library.


## Usage

Run from the project root.

Basic example using an Aztec-style zk rollup base:

python app.py --style aztec --zk --formal --audit

Model a Zama-like FHE design that also uses zk for some components:

python app.py --style zama --fhe --zk --formal

Model a soundness-first rollup with strong proofs and audits:

python app.py --style soundness --formal --audit --chain-type rollup

Model an experimental sidechain with ZK but no FHE or formal proofs:

python app.py --style aztec --zk --chain-type sidechain


## JSON mode

For integration with dashboards or scripts, you can request JSON output:

python app.py --style aztec --zk --formal --audit --json

The JSON payload includes the base profile, the selected features, the three sub-scores, the overallScore, and the resulting grade.


## Interpretation

This tool is deliberately simple and opinionated:

- Adding zk typically improves privacy and soundness but hurts performance slightly.
- Adding FHE improves privacy and soundness further but imposes a larger performance cost.
- Formal verification strongly improves soundness at a small performance cost.
- Public audits improve soundness without changing performance.
- Chain type affects the performance and soundness balance (rollups vs sidechains vs appchains).

The numeric values are illustrative only and do not reflect real-world measurements.  
Use them as a way to structure design discussions, not as absolute truth.


## Relation to Aztec, Zama, and soundness

The predefined styles are conceptual:

- aztec represents a privacy-first zk rollup with encrypted balances and proofs over Ethereum.
- zama represents a design centered on fully homomorphic encryption for encrypted compute in Web3.
- soundness represents a lab or team that leads with formal specifications, proofs, and soundness guarantees.

By toggling flags on top of these base styles, you can approximate how your own project sits between privacy, cryptographic ambition, and operational performance.
