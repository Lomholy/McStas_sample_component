# McStas Sample Component

This repository contains validation examples, analytical benchmarks, and recreation scripts for a generalized sample scattering component developed for **McStas**. The examples cover a range of neutron scattering processes including incoherent scattering, powder diffraction, single-crystal diffraction, specular reflection, and small-angle neutron scattering (SANS).

The repository is structured such that each scattering scenario is implemented as an independent validation case containing:

- A McStas instrument description (`*.instr`)
- Analytical reference calculations (`Analytical.ipynb`)
- Supporting crystallographic or material input files
- Recreation scripts used to generate publication figures

The purpose of the repository is to demonstrate and validate the physical correctness of the sample component through comparison against analytical solutions and crystallographic calculations.

---

# Repository Structure

```text
McStas_sample_component/
├── Incoherent/
├── Powder/
├── Reflecting/
├── Sans/
├── Single_crystal/
├── recreation/
└── README.md
```

---

# Directory Overview

## Incoherent/

Validation case for isotropic incoherent scattering.

### Contents

```text
Incoherent/
├── Analytical.ipynb
└── inc.instr
```

### Files

#### `inc.instr`

McStas instrument file used to simulate incoherent scattering from the sample component.

#### `Analytical.ipynb`

Jupyter notebook containing analytical calculations used as a reference solution against which the Monte Carlo simulation results can be compared.

### Purpose

This example validates the incoherent scattering implementation of the sample component and demonstrates agreement between simulation and analytical theory.

---

## Powder/

Validation case for powder diffraction.

### Contents

```text
Powder/
├── Analytical.ipynb
├── DMC.instr
├── Full_test.hkl
├── Full_test.pcr
├── NaCaAlF.cif
├── NaCaAlF_no_debye.cif
├── NaCaAlF.txt
├── NaCaAlF_no_debye.txt
├── NaCaAlF.xyz
├── NaCaAlf.lau
├── NaCaAlf.laz
└── NaCaAlf2.laz
```

### Files

#### `DMC.instr`

McStas instrument describing the powder diffraction experiment.

#### `Analytical.ipynb`

Contains analytical calculations and diffraction pattern validation.

#### `Full_test.hkl`

Reflection list used for crystallographic diffraction calculations.

#### `Full_test.pcr`

Parameter file associated with diffraction calculations or crystallographic refinement.

#### `NaCaAlF.cif`

Crystallographic information file describing the NaCaAlF crystal structure.

#### `NaCaAlF_no_debye.cif`

Alternative structural description without Debye-Waller factors.

#### `NaCaAlF.txt`

Exported structural information.

#### `NaCaAlF_no_debye.txt`

Exported structural information corresponding to the modified structure.

#### `NaCaAlF.xyz`

Atomic coordinates in XYZ format.

#### `NaCaAlf.lau`

Laue-group information.

#### `NaCaAlf.laz`

Auxiliary crystallographic data.

#### `NaCaAlf2.laz`

Additional crystallographic data.

### Purpose

This example validates powder diffraction behavior by comparing simulated diffraction patterns against analytical and crystallographic predictions for NaCaAlF materials.

---

## Reflecting/

Validation case for specular reflection.

### Contents

```text
Reflecting/
├── Analytical.ipynb
├── analytical.rfl
└── Refl.instr
```

### Files

#### `Refl.instr`

McStas instrument used to simulate reflection from the sample.

#### `analytical.rfl`

Reflectivity reference file used for validation.

#### `Analytical.ipynb`

Analytical calculations for comparison with simulated reflectivity curves.

### Purpose

Demonstrates reflective scattering behavior and validates the reflected intensity against analytical expectations.

---

## Sans/

Validation case for small-angle neutron scattering (SANS).

### Contents

```text
Sans/
├── Analytical.ipynb
└── sans.instr
```

### Files

#### `sans.instr`

McStas instrument configured for SANS simulations.

#### `Analytical.ipynb`

Analytical calculations used to validate the SANS response.

### Purpose

This example verifies that the sample component reproduces expected small-angle scattering behavior and detector distributions.

---

## Single_crystal/

Validation case for single-crystal diffraction.

### Contents

```text
Single_crystal/
├── Analytical.ipynb
├── Copper.cif
├── Copper_mat_proj.cif
├── Copper.txt
├── DMC.instr
├── YBaCuO.cif
├── YBaCuO.ncmat
└── YBaCuO.txt
```

### Files

#### `DMC.instr`

McStas instrument describing the single-crystal diffraction setup.

#### `Analytical.ipynb`

Reference calculations used for comparison with simulated diffraction patterns.

#### `Copper.cif`

Copper crystal structure.

#### `Copper_mat_proj.cif`

Alternative crystallographic representation of copper.

#### `Copper.txt`

Exported material properties and crystal information.

#### `YBaCuO.cif`

YBaCuO crystal structure.

#### `YBaCuO.ncmat`

NCrystal material description for YBaCuO.

#### `YBaCuO.txt`

Exported structural information.

### Purpose

This example validates Bragg diffraction from oriented single crystals and verifies scattering intensities and peak positions against analytical predictions.

---

## recreation/

Contains scripts used to regenerate figures and results associated with the publication.

### Contents

```text
recreation/
├── Diablo.mplstyle
├── project_recreation.sh
└── recreation.py
```

### Files

#### `project_recreation.sh`

Shell script executing the complete reproduction workflow.

#### `recreation.py`

Python script used to post-process simulation results and generate publication figures.

#### `Diablo.mplstyle`

Custom Matplotlib styling used for generating publication-quality plots.

### Purpose

Provides a centralized workflow for recreating the simulation results and figures used in the associated article.

---

# Requirements

The repository requires:

## Core Software

- McStas 3.x or newer
- Python 3.9+
- Jupyter Notebook

## Python Packages

```bash
pip install numpy scipy matplotlib pandas notebook
```

## Optional Dependencies

- NCrystal
- FullProf or equivalent crystallographic utilities

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Lomholy/McStas_sample_component.git
cd McStas_sample_component
```

Verify that McStas is available:

```bash
mcstas --version
```

Install Python dependencies:

```bash
pip install numpy scipy matplotlib pandas notebook
```

---

# Running Individual Validation Cases

## Incoherent Scattering

```bash
cd Incoherent

mcrun inc.instr
```

Open the analytical comparison:

```bash
jupyter notebook Analytical.ipynb
```

---

## Powder Diffraction

```bash
cd Powder

mcrun DMC.instr
```

Open:

```bash
jupyter notebook Analytical.ipynb
```

to compare simulated and analytical diffraction patterns.

---

## Reflectivity

```bash
cd Reflecting

mcrun Refl.instr
```

Compare against analytical results:

```bash
jupyter notebook Analytical.ipynb
```

---

## SANS

```bash
cd Sans

mcrun sans.instr
```

Open:

```bash
jupyter notebook Analytical.ipynb
```

for validation.

---

## Single Crystal Diffraction

```bash
cd Single_crystal

mcrun DMC.instr
```

Open:

```bash
jupyter notebook Analytical.ipynb
```

to compare Bragg peak locations and intensities.

---

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

This script is intended to:

1. Run the required McStas simulations.
2. Collect simulation outputs.
3. Perform preprocessing.
4. Store intermediate data products required for figure generation.

---

## Step 2: Generate Publication Figures

Execute:

```bash
python recreation.py
```

This script:

- Loads generated datasets.
- Produces publication-quality figures.
- Applies the custom styling defined in `Diablo.mplstyle`.

---

## Step 3: Validate Against Analytical Results

Each validation directory contains an `Analytical.ipynb` notebook.

These notebooks provide analytical references for:

- Incoherent scattering
- Powder diffraction
- Reflectivity
- SANS
- Single-crystal diffraction

Agreement between simulation results and notebook predictions constitutes the primary validation procedure used throughout the repository.

---

# Scientific Validation Strategy

The sample component is validated through five representative neutron-scattering scenarios.

| Validation Case | Validation Method |
|----------------|------------------|
| Incoherent Scattering | Comparison with isotropic analytical scattering |
| Powder Diffraction | Comparison with crystallographic diffraction calculations |
| Reflectivity | Comparison with analytical reflectivity |
| SANS | Comparison with analytical small-angle scattering |
| Single Crystal Diffraction | Comparison with Bragg diffraction theory |

Together these examples provide broad coverage of common neutron-scattering processes encountered in diffraction and scattering instruments.

---

# Citation

If you use this repository in academic work, please cite:

1. The publication associated with the sample component.
2. McStas.
3. NCrystal (when using NCrystal-based materials).
4. Any crystallographic databases used to generate the included material files.

---

# Authors

Daniel Lomholt Christensen and collaborators.

---

# License

See the repository license file for licensing information.
