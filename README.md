# SEMANTIC_ORB_SLAM

Repository for my undergraduate project for FAPESP. The project was to add semantic information to feature extraction methods. This was done in two approaches: a handmade descriptor that uses semantic segmentation (SORB) and by mutli-task learning using the SuperPoint model.

All models were implemented using the ORB SLAM2 as framework.

## Install
```
git clone https://github.com/Gabriel-SGama/Semantic_ORB_SLAM2.git
cd Semantic_ORB_SLAM2
git submodule sync
git submodule update --init --recursive --jobs 0
```
 

## Approaches
- ORB SLAM2: Original implementation of the ORB_SLAM2 forked from the [official repository](https://github.com/raulmur/ORB_SLAM2).

- SORB SLAM2: Fusion of the ORB descriptor with a handmade semantic descriptor. First a CNN model extracts the semantic segmentation predictions and each class of certain surrounding pixels is used to calculate the distance between KeyPoints. It is similar to this [paper](https://www.sciencedirect.com/science/article/pii/S0031320321000091).

- ORB SLAM2 SuperPoint: Uses the SuperPoint model to extract the features from each frame. 


For a more detailed explanation of each method, please see the README file from the repository you are interest in.
## Evaluation scripts
At the moment the scripts only work for the KITTI dataset.

- ```build_all.sh```: Builds all versins of the ORB_SLAM2. Change *"make -j2"* parameter in each build.sh file for faster builds (my desktop only handles 2). 
- ```extract_pred_*.py```: Runs the ORB and SORB versions and saves the keyframe trajectory in a *results* folder with the specifc name.
- ```eval_pred.py```: Evaluates all trajectories in the *results* folder according to the APE and RPE metric using the [evo lib](https://github.com/MichaelGrupp/evo). The results are saved in a .csv file.
- ```compare_pred.py```: From the .csv file from each sequence calculates the mean APE or RPE and prints a LaTeX table and plots a box plot. To get the p-values, add two models to the *models_to_compare* list.

In the results_10 are the results obtained for my report. To generate another folder and evaluate the results (change the parameters in code to fit your needs):

```
./build_all.sh
python3 extract_pred_SSP.py # or python3 extract_pred_ORB.py
python3 eval_pred.py
python3 compare_pred.py
```

## Obtained results (without SORB):

Mean APE obtained from 10 runs in each sequence. P-values are between Sp and SSp (ORB is only for reference porpuses)

| Sequence | ORB     | Sp        | SSp (**ours**) | p-value |
| -------- | ------- | --------- | -------------- | ------- |
| 00       | 5.539   | 6.767     | **6.651**      | 0.705   |
| 01       | 439.985 | 286.709   | **209.985**    | 0.131   |
| 02       | 16.739  | 22.459    | **22.314**     | 0.821   |
| 03       | 1.006   | **1.319** | 1.630          | 0.003   |
| 04       | 1.177   | **0.840** | 0.905          | 0.940   |
| 05       | 4.361   | **5.803** | 6.315          | 0.821   |
| 06       | 13.327  | 11.953    | **11.833**     | 0.406   |
| 07       | 2.281   | 3.388     | **2.124**      | 1.000   |
| 08       | 37.679  | 31.324    | **26.700**     | 0.000   |
| 09       | 20.527  | 35.945    | **31.788**     | 0.001   |
| 10       | 5.071   | 5.515     | **4.953**      | 0.023   |

![SSp](imgs/box_plot_KITTI.png?raw=true "box plot KITTI")



## Citations
This repository was a byproduct of the paper: [Semantic SuperPoint: A Deep Semantic Descriptor](https://arxiv.org/abs/2211.01098). If this was repository was useful to you, please cite:

```
Not published yet
```
