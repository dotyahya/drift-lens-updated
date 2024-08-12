#
<div align="center">
  <img src="docs/source/_static/Drift_Lens_Logo.png" width="300"/>
  <h4>Unsupervised Concept Drift Detection <br> from Deep Learning
Representations on Unstructured Data in Real-time</h4>
</div>
<br/>

![Version](https://img.shields.io/pypi/v/driftlens?color=blue)](https://pypi.org/project/driftlens)

*DriftLens* is an **unsupervised drift detection** framework for deep learning classifiers on unstructured data.

The *DriftLens* methodology and its evaluation is currently **Under Review**. 

The preliminary idea was first proposed in the paper: 
[Drift Lens: Real-time unsupervised Concept Drift detection by evaluating per-label embedding distributions](https://ieeexplore.ieee.org/document/9679880) **(Greco et al., 2021)**

*DriftLens* as been also implemented in a web application tool [GitHub](https://github.com/grecosalvatore/DriftLensDemo).

## Table of Contents
- [Installation](#installation)
- [Example of usage](#example-of-usage)
- [DriftLens Methodology](#driftlens-methodology)
- [Experiments Reproducibility](#experiments-reproducibility)
- [References](#references)
- [Authors](#authors)

## Installation
DriftLens is available on PyPI and can be installed with pip for Python >= 3:
**Warning: currently the package is avalaible only under test pypi repository because is under development. It will be available on pypi soon.**
```bash
# Install latest stable version
pip install driftlens

# Alternatively, install latest development version
pip install git+https://github.com/grecosalvatore/drift-lens
```

## Example of usage
```python
from driftlens.driftlens import DriftLens

# DriftLens parameters
batch_n_pc = 150 # Number of principal components to reduce per-batch embeddings
per_label_n_pc = 75 # Number of principal components to reduce per-label embeddings
window_size = 1000 # Window size for drift detection
threshold_number_of_estimation_samples = 1000 # Number of sampled windows to estimate the threshold values

# Initialize DriftLens
dl = DriftLens()

# Estimate the baseline (offline phase)
baseline = dl.estimate_baseline(E=E_train,
                                Y=Y_predicted_train,
                                label_list=training_label_list,
                                batch_n_pc=batch_n_pc,
                                per_label_n_pc=per_label_n_pc)

# Estimate the threshold values with DriftLens (offline phase)
per_batch_distances_sorted, per_label_distances_sorted = dl.random_sampling_threshold_estimation(
                                                            label_list=training_label_list,
                                                            E=E_test,
                                                            Y=Y_predicted_test,
                                                            batch_n_pc=batch_n_pc,
                                                            per_label_n_pc=per_label_n_pc,
                                                            window_size=window_size,
                                                            n_samples=threshold_number_of_estimation_samples,
                                                            flag_shuffle=True,
                                                            flag_replacement=True)

# Compute the window distribution distances (Frechet Inception Distance) with DriftLens
dl_distance = dl.compute_window_distribution_distances(E_windows[0], Y_predicted_windows[0])

```

## DriftLens Methodology
<div align="center">
  <img src="docs/source/_static/drift-lens-architecture.png" width="600"/>
  <h4>DriftLens Methodology.</h4>
</div>
<br/>

DriftLens is an unsupervised drift detection technique based on distribution distances within the embedding representations generated by deep learning models.
The methodology includes an *offline* and an *online* phases. 


In the *offline* phase, DriftLens, takes in input a historical dataset (i.e., baseline and threshold datasets), then: 

1) Estimates the reference distributions from the baseline dataset (e.g., training dataset). The reference
distributions, called **baseline**, represent the distribution of features (i.e., embedding) that the model has learned during the training phase (i.e., they represent the absence of drift).
2) Estimates threshold distance values from the threshold dataset to discriminate between drift and no-drift conditions.

In the *online* phase, the new data stream is processed in windows of fixed size. For each window, DriftLens:

3) Estimates the distributions of the new data windows 
4) it computes the distribution distances with respect to the reference distributions
5) it evaluates the distances against the threshold values.  If the distance exceeds the threshold, the presence of drift is predicted.

In both phases, the distributions are estimated as multivariate normal distribution by computing the mean and the covariance over the embedding vectors.

DriftLens uses the Frechet Distance to measure the similarity between the reference (i.e., baseline) and the new window distributions.

## Experiments Reproducibility
Instructions and scripts for the experimental evaluation reproducibility are located in the [experiments folder](experiments/README.md).

## References
If you use the DriftLens, please cite the following papers:

1) DriftLens methodology and evaluation
The paper is currently **under review**. The pre-print is available at:
```bibtex
@misc{greco2024unsupervisedconceptdriftdetection,
      title={Unsupervised Concept Drift Detection from Deep Learning Representations in Real-time}, 
      author={Salvatore Greco and Bartolomeo Vacchetti and Daniele Apiletti and Tania Cerquitelli},
      year={2024},
      eprint={2406.17813},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2406.17813}, 
}
```

2) Preliminary idea 
```bibtex
@INPROCEEDINGS{driftlens,
  author={Greco, Salvatore and Cerquitelli, Tania},
  booktitle={2021 International Conference on Data Mining Workshops (ICDMW)}, 
  title={Drift Lens: Real-time unsupervised Concept Drift detection by evaluating per-label embedding distributions}, 
  year={2021},
  volume={},
  number={},
  pages={341-349},
  doi={10.1109/ICDMW53433.2021.00049}
  }
```

3) Webapp tool
```bibtex
@inproceedings{greco2024driftlens,
  title={DriftLens: A Concept Drift Detection Tool},
  author={Greco, Salvatore and Vacchetti, Bartolomeo and Apiletti, Daniele and Cerquitelli, Tania and others},
  booktitle={Advances in Database Technology},
  volume={27},
  pages={806--809},
  year={2024},
  organization={Open proceedings}
}
```

# Authors

- **Salvatore Greco**, *Politecnico di Torino* - [Homepage](https://grecosalvatore.github.io/) - [GitHub](https://github.com/grecosalvatore) - [Twitter](https://twitter.com/_salvatoregreco)
- **Bartolomeo Vacchetti**, *Politecnico di Torino* - [Homepage]()
- **Daniele Apiletti**, *Politecnico di Torino* - [Homepage](https://www.polito.it/en/staff?p=daniele.apiletti)
- **Tania Cerquitelli**, *Politecnico di Torino* - [Homepage](https://dbdmg.polito.it/dbdmg_web/people/tania-cerquitelli/)