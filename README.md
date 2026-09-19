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

[ Board State Scan ] ──► [ Frontier Extraction ] ──► [ Subset Difference Reduction ] ──► [ Deterministic Action / Zero-Certainty Fallback (probability based) ]


### 1. Frontier Set Reduction
The algorithm scans visible tiles to form constraint equations:
Creates list of pairs for each revealed tile 
hidden_neighbor : number_of_nearby_mines
By recombination get subset and reveal safe tiles.

<img width="372" height="373" alt="image" src="https://github.com/user-attachments/assets/03530b17-3a25-427f-9d9f-fce64bea12ba" />
<img width="753" height="343" alt="image" src="https://github.com/user-attachments/assets/0f301595-0092-40ef-9028-bcba76b546dd" />


### 2. Probabilistic Guessing
When no deterministic deductions exist, cumulative probability contributions from adjacent numbers are normalized across overlapping constraints. The system identifies and queries the cell with the strictly minimal joint probability of harboring a mine.
