# McStas Sample Component

This repository contains validation examples, analytical benchmarks, and recreation scripts for a generalized sample scattering component developed for **McStas**. The examples cover a range of neutron scattering processes including incoherent scattering, powder diffraction, single-crystal diffraction, specular reflection, and small-angle neutron scattering (SANS).

The repository is structured such that each scattering scenario is implemented as an independent validation case containing:

- A McStas instrument description (`*.instr`)
- Analytical reference calculations (`Analytical.ipynb`)
- Supporting crystallographic or material input files
- Recreation scripts used to generate publication figures

The purpose of the repository is to demonstrate and validate the physical correctness of the sample component through comparison against analytical solutions and crystallographic calculations.


---

# Requirements

The repository requires:

## Core Software

I ran this repository with the following package versions on a MacOs Tahoe 26.6.2

- McStas 3.7.7
- PyFAi 2025.3.0
- Python 3.12.10

# Reproducing the Publication Results

The repository contains a dedicated recreation workflow intended to regenerate all results used in the associated publication.

## Step 1: Run All Simulations

Navigate to the recreation directory:

```bash
cd recreation
```

Execute the recreation script:

```bash
bash project_recreation.sh
```

This script is intended to run the required McStas simulations.

---

## Step 2: Generate Publication Figures

Execute:

```python
python recreation.py
```

This script:

- Loads generated datasets.
- Produces publication-quality figures.
- Applies the custom styling defined in `Diablo.mplstyle`.

---

# Citation

If you use this repository in academic work, please cite:

1. The publication associated with the sample component.
2. McStas.
3. NCrystal (when using NCrystal-based materials).
4. Any crystallographic databases used to generate the included material files.

---

# Authors

Daniel Lomholt Christensen.

---

# License

See the repository license file for licensing information.
