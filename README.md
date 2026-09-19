# Autonomous Minesweeper Solver with Heuristic Inference

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Algorithm](https://img.shields.io/badge/Logic-Subset%20Reduction%20%7C%20Weighted%20Probability-green)
![Paradigm](https://img.shields.io/badge/Domain-Decision%20Making%20under%20Uncertainty-orange)

An algorithmic solver engineered to autonomously clear Minesweeper grids through deterministic set-reduction logic coupled with weighted probabilistic inference when analytical deduction is insufficient.

---

## 📌 Core Engineering Highlights
* **Implicit State-Space Representation:** Eliminates brute-force graph search overhead by evaluating dynamic dictionary mappings of unrevealed boundary frontiers.
* **Deterministic Set-Reduction Logic:** Recursively discovers boundary subsets, eliminating verified mine configurations and revealing safe cells without risk.
* **Weighted Probabilistic Inference:** When logic reaches an impasse, a probabilistic engine computes localized mine density per frontier cell to execute the safest move.

---

## 🧠 Algorithmic Pipeline

[ Board State Scan ] ──► [ Frontier Extraction ] ──► [ Subset Difference Reduction ]
                                         │
┌────────────────────────────────────────┴────────────────────────────────────────┐
▼                                                                                 ▼
[ Deterministic Action ]                                                         [ Zero-Certainty Fallback ]

Flag proven mines (count == hidden)                                              - Compute joint cell probabilities

Reveal proven safe (count == 0)                                                  - Execute minimal-risk probe


### 1. Frontier Set Reduction
The algorithm scans visible tiles to form constraint equations:
$$\text{Tile}_i = \{\text{Hidden Neighbors}\} : N_{\text{mines}}$$
If constraint $A \subset B$, a new deduced constraint is formed:
$$B \setminus A : (N_B - N_A)$$
Iterating this reduction resolves complex interlocking boundaries across multiple tiles without combinatorial explosion.

### 2. Probabilistic Guessing
When no deterministic deductions exist, cumulative probability contributions from adjacent numbers are normalized across overlapping constraints. The system identifies and queries the cell with the strictly minimal joint probability of harboring a mine.

---
