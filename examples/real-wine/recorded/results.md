# UCI Wine: measured results

Real public dataset; fixed design; no tuning on test outcomes.

| split seed | condition | correct / n | accuracy | balanced accuracy |
|---|---|---:|---:|---:|
| 20261023 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 20261023 | raw_5nn | 31/45 | 68.8889% | 66.8519% |
| 20261023 | zscore_train_5nn | 45/45 | 100.0000% | 100.0000% |
| 11 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 11 | raw_5nn | 32/45 | 71.1111% | 71.4815% |
| 11 | zscore_train_5nn | 42/45 | 93.3333% | 94.4444% |
| 23 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 23 | raw_5nn | 30/45 | 66.6667% | 61.6667% |
| 23 | zscore_train_5nn | 44/45 | 97.7778% | 98.1481% |
| 47 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 47 | raw_5nn | 35/45 | 77.7778% | 78.7037% |
| 47 | zscore_train_5nn | 41/45 | 91.1111% | 92.5926% |
| 71 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 71 | raw_5nn | 28/45 | 62.2222% | 60.3704% |
| 71 | zscore_train_5nn | 43/45 | 95.5556% | 96.2963% |
| 101 | majority_train | 18/45 | 40.0000% | 33.3333% |
| 101 | raw_5nn | 30/45 | 66.6667% | 66.6667% |
| 101 | zscore_train_5nn | 44/45 | 97.7778% | 98.1481% |

Primary paired difference: 31.1111 percentage points; stratified 95% percentile interval [20.0, 44.44444444444444].

Interval conditional on primary fitted models and empirical class proportions; 10,000 class-stratified paired resamples.
Six splits reuse 178 rows. Never pool their 810 prediction records as independent samples. No cross-dataset or future-vintage conclusion.
The benchmark and scaling motivation were already public; this is a new execution of an established comparison, not a novel algorithm or a full reproduction of a cited paper.

Data: https://archive.ics.uci.edu/dataset/109/wine ; DOI: 10.24432/C5PC7J ; CC BY 4.0.
Reading record and bounded interpretation: sources.json and REPORT.md in the repository case directory.
