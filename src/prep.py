from src.bh import BootstrapHelper
from src.fbpe import FullBodyPoseEmbedder
from src.pc import PoseClassifier
import pandas as pd
import glob
import os

class PreProcessing:
    
    def __init__(self,bootstrap_images_in_folder,bootstrap_images_out_folder,bootstrap_csvs_out_folder):
        self.bootstrap_images_in_folder = bootstrap_images_in_folder
        self.bootstrap_images_out_folder = "tmp/" + bootstrap_images_out_folder
        self.bootstrap_csvs_out_folder = "tmp/" + bootstrap_csvs_out_folder

        self.bootstrap_helper = BootstrapHelper(
            images_in_folder=self.bootstrap_images_in_folder,
            images_out_folder=self.bootstrap_images_out_folder,
            csvs_out_folder=self.bootstrap_csvs_out_folder,
        )

    def apply(self):
        if os.path.exists("data/" + self.bootstrap_csvs_out_folder + "data.csv"):
            merged_df = pd.read_csv("data/" + self.bootstrap_csvs_out_folder + "data.csv")
        else:
            self.bootstrap_helper.bootstrap(per_pose_class_limit=None)
            self.bootstrap_helper.align_images_and_csvs(print_removed_items=True)
            pose_embedder = FullBodyPoseEmbedder()


            pose_classifier = PoseClassifier(
                pose_samples_folder=self.bootstrap_csvs_out_folder,
                pose_embedder=pose_embedder,
                top_n_by_max_distance=30,
                top_n_by_mean_distance=10)
            outliers = pose_classifier.find_pose_sample_outliers()

            self.bootstrap_helper.remove_outliers(outliers)
            self.bootstrap_helper.align_images_and_csvs(print_removed_items=False)

            csv_files = glob.glob(self.bootstrap_csvs_out_folder + '/*.csv')

            # use os.path.basename() to extract only the file name from each path
            csv_file_names = [os.path.basename(file) for file in csv_files]


            # Load squat_down.csv and drop column by index
            df1 = pd.read_csv(f"{self.bootstrap_csvs_out_folder}/{csv_file_names[0]}", header=None)
            df1 = df1.drop(df1.columns[0], axis=1)

            # Load squat_up.csv and drop column by index
            df2 = pd.read_csv(f"{self.bootstrap_csvs_out_folder}/{csv_file_names[1]}", header=None)
            df2 = df2.drop(df2.columns[0], axis=1)

            # Add new column to each dataframe with output values
            df1['output'] = 0
            df2['output'] = 1

            # Merge the two dataframes
            merged_df = pd.concat([df1, df2], ignore_index=True)

            merged_df.to_csv("data/" + self.bootstrap_csvs_out_folder + "data.csv", index=False)

        return merged_df