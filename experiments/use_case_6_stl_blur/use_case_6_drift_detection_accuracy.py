import argparse
from alibi_detect.cd import KSDrift, MMDDrift, LSDDDrift, CVMDrift, ChiSquareDrift
from experiments.windows_manager.windows_generator import WindowsGenerator
from driftlens.driftlens import DriftLens
import os
import h5py
from tqdm import tqdm
from sklearn.metrics import accuracy_score
import numpy as np
import json
import datetime
import time
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def parse_args():
    parser = argparse.ArgumentParser(description='Train model')
    parser.add_argument('--number_of_runs', type=int, default=1)
    parser.add_argument('--model_name', type=str, default='vit')
    parser.add_argument('--window_size', type=int, default=1000)
    parser.add_argument('--number_of_windows', type=int, default=10)
    parser.add_argument('--drift_percentage', type=int, nargs='+', default=[0, 5, 10, 15, 20]),
    parser.add_argument('--batch_n_pc', type=int, default=150)
    parser.add_argument('--per_label_n_pc', type=int, default=25)
    parser.add_argument('--threshold_sensitivity', type=int, default=99)
    parser.add_argument('--threshold_number_of_estimation_samples', type=int, default=10)
    parser.add_argument('--n_subsamples_sota', type=int, default=500)
    parser.add_argument('--train_embedding_filepath', type=str, default=f"{os.getcwd()}/static/saved_embeddings/vit/train_embedding.hdf5")
    parser.add_argument('--test_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/test_embedding.hdf5')
    parser.add_argument('--new_unseen_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/new_unseen_embedding.hdf5')
    parser.add_argument('--drift_5_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/drift_5_embedding_radius2.hdf5')
    parser.add_argument('--drift_10_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/drift_10_embedding_radius2.hdf5')
    parser.add_argument('--drift_15_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/drift_15_embedding_radius2.hdf5')
    parser.add_argument('--drift_20_embedding_filepath', type=str, default=f'{os.getcwd()}/static/saved_embeddings/vit/drift_20_embedding_radius2.hdf5')
    parser.add_argument('--output_dir', type=str, default=f"{os.getcwd()}/static/outputs/vit/")
    parser.add_argument('--save_results', action='store_true')
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--seed', type=int, default=42)

    return parser.parse_args()


def load_embedding(filepath, E_name=None, Y_original_name=None, Y_predicted_name=None):
    if filepath is not None:
        with h5py.File(filepath, "r") as hf:
            if E_name is None:
                E = hf["E"][()]
            else:
                E = hf[E_name][()]
            if Y_original_name is None:
                Y_original = hf["Y_original"][()]
            else:
                Y_original = hf[Y_original_name][()]
            if Y_predicted_name is None:
                Y_predicted = hf["Y_predicted"][()]
            else:
                Y_predicted = hf[Y_predicted_name][()]
    else:
        raise Exception("Error in loading the embedding file. Please set the embedding paths in the configuration file.")
    return E, Y_original, Y_predicted


def stratified_subsampling(E, Y, n_samples, unique_labels):
    # Calculate samples per class
    samples_per_class = int(n_samples / len(unique_labels))

    # Placeholder for stratified sample indices
    selected_indices = []

    for label in unique_labels:
        # Find indices where current label occurs
        label_indices = np.where(Y == label)[0]

        # If the class has fewer samples than samples_per_class, take them all
        # Otherwise, randomly choose samples_per_class from them
        if len(label_indices) <= samples_per_class:
            selected_indices.extend(label_indices)
        else:
            selected_indices.extend(np.random.choice(label_indices, samples_per_class, replace=False))

    # Now, selected_indices contains the indices of the stratified sample
    # Extract the corresponding elements from E
    E_subsample = E[selected_indices]

    return E_subsample, Y[selected_indices]


def main():
    print("Drift Detection Experiment - Use Case 6")

    # Parse arguments
    args = parse_args()

    print("Model name: ", args.model_name)
    print("Number of runs: ", args.number_of_runs)
    print("Window size: ", args.window_size)
    print("Number of windows: ", args.number_of_windows)
    print("Number of samples sota: ", args.n_subsamples_sota)
    print("Number of samples threshold: ", args.threshold_number_of_estimation_samples)
    print("Drift percentage: ", args.drift_percentage)
    print("Drift path: ", args.drift_5_embedding_filepath)

    training_label_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Labels used for training
    drift_label_list = training_label_list  # Labels used for drift simulation

    if args.save_results:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        ts = time.time()
        timestamp = str(datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S'))
        output_filename = f"drift_detection_accuracy_model_{args.model_name}_win_size_{args.window_size}_n_windows_{args.number_of_windows}_radius2_{timestamp}.json"

    # Parse parameters
    window_size = args.window_size
    batch_n_pc = args.batch_n_pc
    per_label_n_pc = args.per_label_n_pc
    n_windows = args.number_of_windows

    # Load the embeddings
    if args.model_name == "vgg16":
        E_train, Y_original_train, Y_predicted_train = load_embedding(args.train_embedding_filepath, E_name="embedding", Y_original_name="original_label", Y_predicted_name="predicted_label")
        E_test, Y_original_test, Y_predicted_test = load_embedding(args.test_embedding_filepath, E_name="embedding", Y_original_name="original_label", Y_predicted_name="predicted_label")
        E_new_unseen, Y_original_new_unseen, Y_predicted_new_unseen = load_embedding(args.new_unseen_embedding_filepath, E_name="embedding", Y_original_name="original_label", Y_predicted_name="predicted_label")
        E_drift, Y_original_drift, Y_predicted_drift = load_embedding(args.drift_embedding_filepath, E_name="embedding", Y_original_name="original_label", Y_predicted_name="predicted_label")
    else:
        E_train, Y_original_train, Y_predicted_train = load_embedding(args.train_embedding_filepath)
        E_test, Y_original_test, Y_predicted_test = load_embedding(args.test_embedding_filepath)
        E_new_unseen, Y_original_new_unseen, Y_predicted_new_unseen = load_embedding(args.new_unseen_embedding_filepath)
        E_drift_5, Y_original_drift_5, Y_predicted_drift_5 = load_embedding(args.drift_5_embedding_filepath)
        E_drift_10, Y_original_drift_10, Y_predicted_drift_10 = load_embedding(args.drift_10_embedding_filepath)
        E_drift_15, Y_original_drift_15, Y_predicted_drift_15 = load_embedding(args.drift_15_embedding_filepath)
        E_drift_20, Y_original_drift_20, Y_predicted_drift_20 = load_embedding(args.drift_20_embedding_filepath)

    #Y_original_drift_5 = [y-10 for y in Y_original_drift_5]
    #Y_original_drift_5 = np.array(Y_original_drift_5)

    #Y_original_drift_10 = [y-10 for y in Y_original_drift_10]
    #Y_original_drift_10 = np.array(Y_original_drift_10)

    #Y_original_drift_15 = [y-10 for y in Y_original_drift_15]
    #Y_original_drift_15 = np.array(Y_original_drift_15)

    #Y_original_drift_20 = [y-10 for y in Y_original_drift_20]
    #Y_original_drift_20 = np.array(Y_original_drift_20)

    print("Training samples:", len(E_train))
    print("Test samples:", len(E_test))
    print("New unseen samples:", len(E_new_unseen))
    print("Drift samples 5%:", len(E_drift_5))
    print("Drift samples 10%:", len(E_drift_10))
    print("Drift samples 15%:", len(E_drift_15))
    print("Drift samples 20%:", len(E_drift_20))

    ks_acc_dict = {str(p): [] for p in args.drift_percentage}
    mmd_acc_dict = {str(p): [] for p in args.drift_percentage}
    lsdd_acc_dict = {str(p): [] for p in args.drift_percentage}
    cvm_acc_dict = {str(p): [] for p in args.drift_percentage}
    driftlens_acc_dict = {str(p): [] for p in args.drift_percentage}

    output_dict_run_list = []

    output_dict = {"params": vars(args)}

    for run_id in range(args.number_of_runs):

        print(f"\nRun {run_id + 1}/{args.number_of_runs}")

        # Initialize the DriftLens
        dl = DriftLens()

        # Estimate the baseline with DriftLens
        baseline = dl.estimate_baseline(E=E_train,
                                        Y=Y_predicted_train,
                                        label_list=training_label_list,
                                        batch_n_pc=batch_n_pc,
                                        per_label_n_pc=per_label_n_pc)

        # Estimate the threshold values with DriftLens
        per_batch_distances_sorted, per_label_distances_sorted = dl.random_sampling_threshold_estimation(
            label_list=training_label_list,
            E=E_test,
            Y=Y_predicted_test,
            batch_n_pc=batch_n_pc,
            per_label_n_pc=per_label_n_pc,
            window_size=window_size,
            n_samples=args.threshold_number_of_estimation_samples,
            flag_shuffle=True,
            flag_replacement=True)

        # Calculate the threshold values
        l = np.array(per_batch_distances_sorted)
        l = l[(l > np.quantile(l, 0.01)) & (l < np.quantile(l, 0.99))].tolist()
        per_batch_th = max(l)

        E_subsample, Y_subsample = stratified_subsampling(E_train,
                                                          Y_original_train,
                                                          n_samples=args.n_subsamples_sota,
                                                          unique_labels=training_label_list)

        # Initialize drift detectors used for comparison
        ks_detector = KSDrift(E_subsample, p_val=.05)
        mmd_detector = MMDDrift(E_subsample, p_val=.05, n_permutations=100, backend="pytorch")
        lsdd_detector = LSDDDrift(E_subsample, backend='pytorch', p_val=.05)
        cvm_detector = CVMDrift(E_subsample, p_val=.05)

        for current_drift_percentage in args.drift_percentage:

            print(f" Drift percentage: {current_drift_percentage}")

            # Initialize empty lists of predictions
            ks_preds = []
            mmd_preds = []
            lsdd_preds = []
            cvm_preds = []
            dl_distances = []

            # Ground truth
            if current_drift_percentage > 0:
                ground_truth = [1] * n_windows
            else:
                ground_truth = [0] * n_windows

            # Generate windows and predict drift
            for i in tqdm(range(n_windows)):

                if current_drift_percentage > 0:

                    if current_drift_percentage == 5:
                        E_current_drift = E_drift_5
                        Y_predicted_current_dirft = Y_predicted_drift_5
                        Y_original_current_dirft = Y_original_drift_5
                    elif current_drift_percentage == 10:
                        E_current_drift = E_drift_10
                        Y_predicted_current_dirft = Y_predicted_drift_10
                        Y_original_current_dirft = Y_original_drift_10
                    elif current_drift_percentage == 15:
                        E_current_drift = E_drift_15
                        Y_predicted_current_dirft = Y_predicted_drift_15
                        Y_original_current_dirft = Y_original_drift_15
                    else:
                        E_current_drift = E_drift_20
                        Y_predicted_current_dirft = Y_predicted_drift_20
                        Y_original_current_dirft = Y_original_drift_20


                    # Initialize the WindowsGenerator - used for creating the windows
                    wg = WindowsGenerator(training_label_list,
                                          drift_label_list,
                                          E_current_drift,
                                          Y_predicted_current_dirft,
                                          Y_original_current_dirft,
                                          None,
                                          None,
                                          None)

                    # Drift
                    E_windows, Y_predicted_windows, Y_original_windows = wg.balanced_without_drift_windows_generation(window_size=window_size,
                                                                                                                      n_windows=1,
                                                                                                                      flag_shuffle=True,
                                                                                                                      flag_replacement=True)

                else:
                    # Initialize the WindowsGenerator - used for creating the windows
                    wg = WindowsGenerator(training_label_list,
                                          drift_label_list,
                                          E_new_unseen,
                                          Y_predicted_new_unseen,
                                          Y_original_new_unseen,
                                          None,
                                          None,
                                          None)

                    # No Drift
                    E_windows, Y_predicted_windows, Y_original_windows = wg.balanced_without_drift_windows_generation(window_size=window_size,
                                                                                                                      n_windows=1,
                                                                                                                      flag_shuffle=True,
                                                                                                                      flag_replacement=True)

                for w_id in range(len(E_windows)):
                    E_windows[w_id] = np.float32(E_windows[w_id])

                # Compute the window distribution distances (Frechet Inception Distance) with DriftLens
                dl_distance = dl.compute_window_distribution_distances(E_windows[0], Y_predicted_windows[0])

                # Predict drift with the drift detectors used for comparison
                ks_pred = ks_detector.predict(E_windows[0])
                mmd_pred = mmd_detector.predict(E_windows[0])
                lsdd_pred = lsdd_detector.predict(E_windows[0], return_p_val=True, return_distance=True)
                cvm_pred = cvm_detector.predict(E_windows[0], drift_type='batch', return_p_val=True, return_distance=True)

                # Append the predictions to the lists
                ks_preds.append(ks_pred["data"]["is_drift"])
                mmd_preds.append(mmd_pred["data"]["is_drift"])
                lsdd_preds.append(lsdd_pred["data"]["is_drift"])
                cvm_preds.append(cvm_pred["data"]["is_drift"])

                dl_distances.append(dl_distance)


            dl_preds = []
            for dl_distance in dl_distances:
                if dl_distance["per-batch"] > per_batch_th:
                    dl_preds.append(1)
                else:
                    dl_preds.append(0)

            # Calculate the accuracy of the drift detectors
            ks_acc = accuracy_score(ground_truth, ks_preds, normalize=True)
            mmd_acc = accuracy_score(ground_truth, mmd_preds, normalize=True)
            lsdd_acc = accuracy_score(ground_truth, lsdd_preds, normalize=True)
            cvm_acc = accuracy_score(ground_truth, cvm_preds, normalize=True)
            driftlens_acc = accuracy_score(ground_truth, dl_preds, normalize=True)

            ks_acc_dict[str(current_drift_percentage)].append(ks_acc)
            mmd_acc_dict[str(current_drift_percentage)].append(mmd_acc)
            lsdd_acc_dict[str(current_drift_percentage)].append(lsdd_acc)
            cvm_acc_dict[str(current_drift_percentage)].append(cvm_acc)
            driftlens_acc_dict[str(current_drift_percentage)].append(driftlens_acc)

            print("MMD: ", mmd_acc)
            print("KS: ", ks_acc)
            print("LSDD: ", lsdd_acc)
            print("CVM: ", cvm_acc)
            print("DriftLens: ", driftlens_acc)

            # Create the output dictionary
            output_dict_run = {f"run_id":run_id, "drift_percentage": current_drift_percentage, "KS": ks_acc, "MMD": mmd_acc, "LSDD": lsdd_acc, "CVM": cvm_acc, "DriftLens": driftlens_acc}
            output_dict_run_list.append(output_dict_run)

    output_dict["runs_log"] = output_dict_run_list

    for p in args.drift_percentage:
        output_dict[str(p)] = {"accuracy_list": {"KS": ks_acc_dict[str(p)], "MMD": mmd_acc_dict[str(p)], "LSDD": lsdd_acc_dict[str(p)], "CVM": cvm_acc_dict[str(p)], "DriftLens": driftlens_acc_dict[str(p)]},
                                  "mean_accuracy": {"KS": np.mean(ks_acc_dict[str(p)]), "MMD": np.mean(mmd_acc_dict[str(p)]), "LSDD": np.mean(lsdd_acc_dict[str(p)]), "CVM": np.mean(cvm_acc_dict[str(p)]), "DriftLens": np.mean(driftlens_acc_dict[str(p)])},
                                  "standard_deviation_accuracy": {"KS": np.std(ks_acc_dict[str(p)]), "MMD": np.std(mmd_acc_dict[str(p)]), "LSDD": np.std(lsdd_acc_dict[str(p)]), "CVM": np.std(cvm_acc_dict[str(p)]), "DriftLens": np.std(driftlens_acc_dict[str(p)])}}

        # Save the output dictionary
        with open(os.path.join(args.output_dir, output_filename), 'w') as fp:
            json.dump(output_dict, fp)

    return


if __name__ == "__main__":
    main()