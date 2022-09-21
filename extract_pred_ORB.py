import os
from glob import glob
import numpy as np

PATH_TO_SEQ = "/home/gama/Documentos/datasets/kitti/data_odometry_color/dataset/sequences/"
exec_path = "Examples/Monocular/mono_kitti"
vocab_path = "Vocabulary/ORBvoc.txt"
yaml_path = "Examples/Monocular/KITTI"
yaml_options = ["00-02", "03", "04-12"]
results_path = "results_test/"


def make_command(seq, root_dir):
    index = -1
    try:
        int_seq = int(seq)
        if int_seq <= 2:
            index = 0
        elif int_seq == 3:
            index = 1
        elif int_seq >= 4 and int_seq <= 12:
            index = 2
        else:
            print("sequence ", seq, " does not have a config file registered")
            print("using last file")
            index = 2

        yaml_file = yaml_path + yaml_options[index] + ".yaml"

    except:
        print("seg is not a number, using test config")
        yaml_file = yaml_path + yaml_options[0] + ".yaml"

    command = root_dir + exec_path + " " + root_dir + vocab_path + " " + root_dir + yaml_file + " " + PATH_TO_SEQ + seq

    return command


if __name__ == "__main__":
    """
    seqs_to_eval: select the sequences to run the ORB_SLAM2_SuperPoint
    descriptor: name of the descriptor method to use
    nruns: number of times each sequence is going to executed
    add_runs: whether to number the file from the (last run index + 1) or from 0
    descriptor:
    """

    # seqs_to_eval = ["00"]
    seqs_to_eval = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

    descriptor = ["ORB", "SEM"]

    nruns = 10
    add_runs = True

    os.makedirs(results_path, exist_ok=True)

    for seq in seqs_to_eval:
        for desc in descriptor:
            root_dir = "ORB_SLAM2/" if desc == "ORB" else "SORB_SLAM2/"
            new_dir = results_path + seq + "/" + desc + "/"
            os.makedirs(new_dir, exist_ok=True)

            command = make_command(seq, root_dir)

            print("running command: ", command, "\n")

            run_files = glob(new_dir + "/*.txt")
            run_files = [file for file in run_files if file.split("/")[-1].split(".")[0].isdigit()]

            last_run = 0
            if len(run_files) > 0 and add_runs:
                last_run = int(run_files[-1].split("/")[-1].split(".")[0]) + 1

            for i in range(nruns):

                os.system(command)
                os.system("mv " + "KeyFrameTrajectory.txt " + new_dir + "/" + str(i + last_run) + ".txt")
