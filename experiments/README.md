# Experiments reproducibility
This folder contains the scripts and instructions to reproduce the experiments of the paper.

## Table of Contents
- [Experimental use cases](#experimental-use-cases)
- [Drift detection performance evaluation](#drift-detection-performance-evaluation)
- [Complexity evaluation](#complexity-evaluation)
- [Drift curve evaluation](#drift-curve-evaluation)
- [Parameter sensitivity evaluation](#parameter-sensitivity-evaluation)



## Experimental use cases


Each macro use case is divided into folder. 
For each macro use case, there is a folder `model_training_and_embedding_extraction` containing the following scripts:
- `{model}_training.ipynb`: Jupyter notebook to train the model
- `{model}_embedding_extraction.py`: Jupyter notebook to extract the embedding representations the model

Note that some use cases contains a single script for the model training and embedding extraction. Moreover, some use cases contains some scripts to prepare the dataset.
Each macro use case also contains a README.md file with specific information about the use case and the simulated drift.

To facilitate and speed up the reproducibility, the embedding representations already extracted will be provided soon.

<table>
  <caption>Experimental use cases.</caption>
  <thead>
    <tr>
      <th rowspan="3">Data Type</th>
      <th rowspan="3">Dataset</th>
        <th>Use Case</th>
      <th>Models</th>
      <th>F1</th>
      <th rowspan="3">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3">Text</th>
      <th rowspan="3">Ag News</th>
      <th>1.1</th>
      <td>BERT</td>
      <td>0.98</td>
      <td rowspan="3"> <b>Task</b>: Topic Classification. <BR>
<b>Training Labels</b>: <i>World</i>, <i>Business</i>, and <i>Sport</i> <BR>
<b>Drift</b>: Simulated with one new class label: <i>Science/Tech</i></td>
    </tr>
    <tr>
      <th>1.2</th>
      <td>DistillBERT</td>
      <td>0.97</td>
    </tr>
    <tr>
      <th>1.3</th>
      <td>RoBERTa</td>
      <td>0.98</td>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  <tr>
      <th rowspan="3">Text</th>
      <th rowspan="3">20 Newsgroup</th>
      <th>2.1</th>
      <td>BERT</td>
      <td>0.88</td>
      <td rowspan="3"><b>Task</b>: Topic Classification. <BR>
<b>Training Labels</b>: <i>Technology</i>, <i>Sale-Ads</i>, <i>Politics</i>, <i>Religion</i>, <i>Science</i> <BR>
<b>Drift</b>: Simulated with one new class label: <i>Recreation</i></td>
    </tr>
    <tr>
      <th>2.2</th>
      <td>DistillBERT</td>
      <td>0.87</td>
    </tr>
    <tr>
      <th>2.3</th>
      <td>RoBERTa</td>
      <td>0.88</td>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th rowspan="3">Text</th>
      <th rowspan="3">20 Newsgroup</th>
      <th rowspan="3">3</th>
      <td rowspan="3">BERT</td>
      <td rowspan="3">0.87</td>
      <td rowspan="3"><b>Task</b>: Topic Classification. <BR>
    <b>Training Labels</b>: <i>Technology</i>, <i>Sale-Ads</i>, <i>Politics</i>, <i>Religion</i>, <i>Science</i>, <i>Recreation.sports</i>  <BR>
    <b>Drift</b>: Simulated with one sub-class label: <i>Recreation.autos</i></td>
    </tr>
    <tr>
    </tr>
    <tr>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
        <tr>
      <th rowspan="3">Text</th>
      <th rowspan="3">Bias in Bios</th>
      <th rowspan="3">4</th>
      <td rowspan="3">BERT</td>
      <td rowspan="3">0.94</td>
      <td rowspan="3"><b>Task</b>: Occupation Classification. <BR>
    <b>Training Labels</b>: <i>Professor</i>, <i>Physician</i>, <i>Attorney</i>, <i>Photographer</i>, <i>Journalist</i> (Male gender); <i>Nurse</i> (Female gender)  <BR>
    <b>Drift</b>: Simulated with bios from same labels but opposite gender (Male nurses and Female for all others occupations)</i></td>
    </tr>
    <tr>
    </tr>
    <tr>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th rowspan=2">Image</th>
      <th rowspan="2">MNIST</th>
      <th>5.1</th>
      <td>VGG16</td>
      <td>0.89</td>
      <td rowspan="2"> <b>Task</b>: Image Classification. <BR>
    <b>Training Labels</b>: Digits from 0 to 7<BR>
    <b>Drift</b>: Simulated with two new class labels: Digit 8 and 9</td>
        </tr>
        <tr>
          <th>5.2</th>
          <td>VisionTransformer</td>
          <td>0.90</td>
        </tr>
        <tr class="separator">
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      <tr>
      <tr>
      <th rowspan=2">Image</th>
      <th rowspan="2">Intel-Image</th>
      <th>6.1</th>
      <td>VisionTransformer</td>
      <td>0.90</td>
      <td rowspan="2"> <b>Task</b>: Image Classification. <BR>
<b>Training Labels</b>: <i>Forest</i>, <i>Glacier</i>, <i>Mountain</i>, <i>Building</i>, <i>Street</i> <BR>
<b>Drift</b>: Simulated with one new class label: <i>Sea</i></td>
    </tr>
    <tr>
      <th>6.2</th>
      <td>VGG16</td>
      <td>0.89</td>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  <tr>
      <th rowspan="2">Image</th>
      <th rowspan="2">STL-10</th>
      <th>7.1</th>
      <td>VisionTransformer</td>
      <td>0.96</td>
      <td rowspan="2"> <b>Task</b>: Image Classification. <BR>
<b>Training Labels</b>: <i>Airplane</i>, <i>Bird</i>, <i>Car</i>, <i>Cat</i>, <i>Deer</i>, <i>Dog</i>, <i>Horse</i>, <i>Monkey</i>, <i>Ship</i> <BR>
<b>Drift</b>: Simulated with one new class label: <i>Truck</i></td>
    </tr>
    <tr>
      <th>7.2</th>
      <td>VGG16</td>
      <td>0.82</td>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th rowspan="3">Image</th>
      <th rowspan="3">STL-10</th>
      <th rowspan="3">8</th>
      <td rowspan="3">VisionTransformer</td>
      <td rowspan="3">0.90</td>
      <td rowspan="3"><b>Task</b>: Image Classification. <BR>
    <b>Training Labels</b>: <i>Airplane</i>, <i>Bird</i>, <i>Car</i>, <i>Cat</i>, <i>Deer</i>, <i>Dog</i>, <i>Horse</i>, <i>Monkey</i>, <i>Ship</i>, <i>Truck</i> <BR>
 <b>Drift</b>: Simulated injecting Gaussian blur on images belonging all classes</td>
    </tr>
    <tr>
    </tr>
    <tr>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th rowspan="3">Image</th>
      <th rowspan="3">FairFace</th>
      <th rowspan="3">9</th>
      <td rowspan="3">VisionTransformer</td>
      <td rowspan="3">0.95</td>
      <td rowspan="3"><b>Task</b>: Gender Classification. <BR>
    <b>Training Labels</b>: <i>Male</i>, <i>Female</i> - (White, Black, Middle Eastern, Latino-Hispanic, Indian races) <BR>
 <b>Drift</b>: Introduced with images from same labels but different race (East Asian and Southeast Asian)</td>
    </tr>
    <tr>
    </tr>
    <tr>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
<tr>
      <th rowspan="3">Speech</th>
      <th rowspan="3">Common Voice</th>
      <th rowspan="3">10</th>
      <td rowspan="3">Wav2Vec</td>
      <td rowspan="3">0.91</td>
      <td rowspan="3"><b>Task</b>: Gender Classification. <BR>
    <b>Training Labels</b>: <i>Male</i>, <i>Female</i> (English - US and UK accents) <BR>
    <b>Drift</b>: Simulated with speeches from difference accents (English - Australian, Canadian, Scottish)</td>
    </tr>
    <tr>
    </tr>
    <tr>
    </tr>
    <tr class="separator">
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

## Drift detection performance evaluation
This evaluation aims to determine the effectiveness of DriftLens in detecting windows containing drifted samples of varying severity.
The drift detection problem is tackled as a binary classification task. The task consists in predicting whether a window of new samples contains drift. 

The `scripts/1_drift_detection_performance_evaluation_scripts` folder contains the scripts to run the evaluation for all the use cases. These scripts can be used to reproduce Tables 3 and 4 in the paper.

All the scripts for the different use cases are similar.
An example of drift detection performance evaluation script is the following:

```bash
cd ../../..


python -m experiments.use_case_1_ag_news_science_drift.use_case_1_drift_detection_accuracy \
  --number_of_runs 10 \
  --model_name 'bert' \
  --window_size 2000 \
  --number_of_windows 100 \
  --drift_percentage 0 5 10 15 20 \
  --threshold_sensitivity 99 \
  --threshold_number_of_estimation_samples 10000 \
  --batch_n_p 150 \
  --per_label_n_pc 75 \
  --n_subsamples_sota 5000 \
  --train_embedding_filepath 'experiments/use_case_1_ag_news_science_drift/static/saved_embeddings/bert/train_embedding_0_1_2.hdf5' \
  --test_embedding_filepath 'experiments/use_case_1_ag_news_science_drift/static/saved_embeddings/bert/test_embedding_0_1_2.hdf5' \
  --new_unseen_embedding_filepath 'experiments/use_case_1_ag_news_science_drift/static/saved_embeddings/bert/new_unseen_embedding_0_1_2.hdf5' \
  --drift_embedding_filepath 'experiments/use_case_1_ag_news_science_drift/static/saved_embeddings/bert/drift_embedding_3.hdf5' \
  --output_dir 'experiments/use_case_1_ag_news_science_drift/static/outputs/bert/' \
  --save_results \
  --cuda \
  --verbose \
  --seed 42
```

 Below is an explanation of each argument used in the script:

- `--number_of_runs` (int) Specifies the number of times the evaluation should be repeated to ensure statistical significance. In the paper we used 10 runs.
  
- `--model_name` (str) The name of the model to be used for the evaluation. In this case, 'bert' indicates that the BERT model is used.
  
- `--window_size` (int) The size of the window ($m_w$), in terms of the number of samples it contains, for drift detection. In the paper, we used window sizes in range [250, 500, 1000, 2500] depending on the use case.
  
- `--number_of_windows` (int) The total number of windows to be evaluated for drift detection. At each run, the script evaluates the model's performance across different windows. In the paper, we used 100 windows.
  
- `--drift_percentage` (int) A list of percentages that define the severity of drift in each window. The script evaluates the model's performance across different levels of drift severity. In the paper, we used drift percentages in range [0, 5, 10, 15, 20].
  
- `--threshold_sensitivity` (int) The sensitivity of the drift detection threshold ($T_\alpha$). A higher value means the drift detection is more sensitive. The default value is 0.01.
  
- `--threshold_number_of_estimation_samples` (int) The number of sampled windows ($n_{th}$) used to estimate the threshold for drift detection. In the paper, we set this value to 10000 as a default.
  
- `--batch_n_p` (int) The number of principal component used to reduce the per-batch embedding ($d'$). In the paper, we set this value to 150 as a default.
  
- `--per_label_n_pc` (int) The number of principal components used to reduce the per-label embedding ($d'_l$). In the paper, we set this value to 75 as a default.
  
- `--n_subsamples_mmd` (int) The number of subsamples used to create the reference windows for the MMD detector. In the paper, we set this value to 8500 as a default. -1 indicates that no subsampling is performed.

- `--n_subsamples_lsdd` (int) The number of subsamples used to create the reference windows for the LSDD detector. In the paper, we set this value to 14000 as a default. -1 indicates that no subsampling is performed.

- `--n_subsamples_cvm` (int) The number of subsamples used to create the reference windows for the CVM detector. In the paper, we set this value to the full dataset as a default. -1 indicates that no subsampling is performed.

- `--n_subsamples_ks` (int) The number of subsamples used to create the reference windows for the KS detector. In the paper, we set this value to the full dataset as a default. -1 indicates that no subsampling is performed.
  
- `--train_embedding_filepath` (str) The file path to the saved embeddings of the training dataset. The embeddings of the training dataset are used to estimate the DriftLens baseline, and to create the reference windows for the compared state-of-the-art drift detectors.
  
- `--test_embedding_filepath` (str) The file path to the saved embeddings of the test dataset. The embedding of the test dataset are used to estimate the DriftLens threshold.
  
- `--new_unseen_embedding_filepath` (str) The file path to the saved embeddings of new, unseen samples. The embeddings of the new, unseen samples are used to generate windows without drift (i.e., with the same distribution of the training dataset).
  
- `--drift_embedding_filepath` (str) The file path to the saved embeddings specifically representing drifted samples. The embeddings of the drifted samples are used to generate windows with drift.
  
- `--output_dir` (str) The directory where the output of the script (e.g., evaluation results) will be saved.
  
- `--save_results` A flag indicating whether to save the results of the evaluation.
  
- `--cuda` A flag to enable CUDA (GPU acceleration) if available.
  
- `--verbose` A flag to enable verbose output, providing more detailed logs during execution.
  
- `--seed` The random seed for reproducibility of results.


## Complexity evaluation
This evaluation aims to ascertain the effectiveness of DriftLens to
perform near real-time drift detection. To this end, we compare the
running time of the drift detectors by varying the reference and
data stream windows sizes, and the embedding dimensionality.

The `scripts/2_complexity_evaluation_scripts` folder  contains the scripts to run the evaluation. These scripts can be used to reproduce Figures 5 and 6 in the paper.

The folder contains the following scripts:

```bash
cd ../../..


python -m experiments.running_time_comparison \
  --number_of_runs 5 \
  --training_label_list 0 1 2 \
  --drift_label_list 3 \
  --run_mmd \
  --run_ks \
  --run_lsdd \
  --run_cvm \
  --run_driftlens \
  --run_experiment_reference_window \
  --run_experiment_window_size \
  --run_experiment_embedding_dimensionality \
  --reference_window_size_range '5000:15000:2500' \
  --datastream_window_size_range '500:2500:500' \
  --embedding_dimensionality_range '500:2500:500' \
  --fixed_reference_window_size 5000 \
  --fixed_datastream_window_size 1000 \
  --fixed_embedding_dimensionality 1000 \
  --batch_n_p 150 \
  --per_label_n_pc 75 \
  --output_dir 'experiments/' \
  --save_results \
  --verbose \
  --seed 42
```



## Drift curve evaluation
This evaluation aims to measure the ability of DriftLens to coherently represent and characterize the drift curve.

The folder  contains the script to run the evaluation. These scripts can be used to reproduce Table 5 in the paper.
The script is organized as follows:

## Parameter sensitivity evaluation
This evaluation aims to determine the robustness and sensitivity of DriftLens to its parameters.

The folder  contains the script to run the evaluation. These scripts can be used to reproduce Table 6 in the paper.
The script is organized as follows: