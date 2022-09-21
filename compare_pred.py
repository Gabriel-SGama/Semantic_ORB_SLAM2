import os
from glob import glob
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from scipy import stats

results_path = "results_10/"


if __name__ == "__main__":
    """
    models_to_compare: selects models to compare against and generate p-values (only supports two models at the same time)
    line 70: 'data = pd.read_csv(folder + "/data_ape.csv")' change to data_rpe for the RPE metric
    """

    folders = []

    models_to_compare = []
    models_to_compare = ["SP_185000_ML22", "SSP_small_180000_ML22"]

    # get folders
    print("eval results in directorys:")
    for it in os.scandir(results_path):
        if it.is_dir():
            for it2 in os.scandir(it.path):
                if it2.is_dir():
                    folders.append(it2.path)
                    print(it2.path)
    folders = sorted(folders)

    # number of sequences and models
    seq_list = []
    model_list = []
    prev_seq = folders[0].split("/")[-2]
    prev_model = folders[0].split("/")[-1]
    seq_list.append(prev_seq)
    for folder in folders:
        model = folder.split("/")[-1]
        seq = folder.split("/")[-2]

        # assumes that all sequences have the same model
        if prev_model != model and prev_seq == folders[0].split("/")[-2]:
            prev_model = model
            model_list.append(model)

        if prev_seq != seq:
            prev_seq = seq
            seq_list.append(seq)

    model_list = sorted(model_list)
    # dict for data from each sequence
    seq_data_dict = dict.fromkeys(seq_list)

    keys = ["rmse", "mean", "std", "min", "max", "sse", "labels"]
    for seq in seq_data_dict.keys():
        seq_data_dict[seq] = dict.fromkeys(keys)

        for metric in seq_data_dict[seq].keys():
            seq_data_dict[seq][metric] = []

    # read csv for the data
    prev_seq = "00"
    for folder in folders:
        model = folder.split("/")[-1]
        seq = folder.split("/")[-2]

        seq_data_dict[seq]["labels"].append(model)
        data = pd.read_csv(folder + "/data_ape.csv")
        for key in keys:
            if key == "labels":
                continue
            seq_data_dict[seq][key].append(data[key])

    # initialize list elements
    data = dict.fromkeys(model_list)
    for model in data.keys():
        data[model] = dict.fromkeys(seq_list)

    # create table
    kruskal_res = dict.fromkeys(seq_list)
    kruskal_data = dict.fromkeys(models_to_compare)
    for i, seq in enumerate(seq_list):
        metrics = seq_data_dict[seq]

        for model_metric, name in zip(metrics["mean"], metrics["labels"]):
            mean = sum(model_metric) / len(model_metric)
            data[name][seq] = mean

            if name in models_to_compare:
                kruskal_data[name] = model_metric

        if len(models_to_compare) == 2:
            kruskal_res[seq] = stats.kruskal(kruskal_data[models_to_compare[0]], kruskal_data[models_to_compare[1]])

    pvalues = []
    if len(models_to_compare) == 2:
        for seq in seq_list:
            pvalues.append(kruskal_res[seq].pvalue)

    if len(models_to_compare) == 2:
        print("kruskal_red: ", kruskal_res)

    df = pd.DataFrame(data)

    if len(models_to_compare) == 2:
        df["pvalue"] = pvalues

    df = df.round(decimals=3)
    print(df.to_latex(index=True, caption="Results of each method in the kitti dataset according to the APE metric"))

    # ------------PLOTING-------------
    # plot info
    fig, axs = plt.subplots((len(seq_list) + 1) // 2, 2, figsize=(8, 12))

    # set last ax to off if there are an odd number of sequences
    if len(seq_list) & 1:
        axs[-1, -1].axis("off")

    colors = cm.rainbow(np.linspace(0, 1, len(model_list)))

    for i, seq in enumerate(seq_list):
        line = i // 2
        column = i % 2
        ax = axs[line, column]
        metrics = seq_data_dict[seq]

        for i, label in enumerate(metrics["labels"]):
            metrics["labels"][i] = label.split("_")[0]

        # plot mean metric
        box = ax.boxplot(metrics["mean"], labels=metrics["labels"], vert=True, patch_artist=True)

        for patch, color in zip(box["boxes"], colors):
            plt.setp(patch, facecolor=color)

        ax.title.set_text("Seq: " + seq)

    fig.tight_layout()
    plt.show()
