from zipfile import ZipFile
from src.bh import BootstrapHelper
from src.fbpe import FullBodyPoseEmbedder
from src.pc import PoseClassifier
import pandas as pd
import glob
import os

from pathlib import Path
path = Path("/path/to/some/file.txt")
filename = path.stem


class PreProcessing:

    def __init__(self, bootstrap_images_in_zip="None", bootstrap_images_out_folder="output_images", bootstrap_csvs_out_folder="output_csvs", bootstrap_images_in_folder=None):
        if bootstrap_images_in_folder is None:
            zip_file_name_with_extension, _ = os.path.splitext(
                bootstrap_images_in_zip)
            zip_file_name = str(os.path.basename(zip_file_name_with_extension))
            self.bootstrap_images_in_folder = "tmp/"
            with ZipFile(bootstrap_images_in_zip, 'r') as zObject:
                zObject.extractall(path=self.bootstrap_images_in_folder)
            self.bootstrap_images_in_folder = self.bootstrap_images_in_folder + zip_file_name
            print("in_folder", self.bootstrap_images_in_folder)
        else:
            if bootstrap_images_in_zip == "None":
                raise Exception
            self.bootstrap_images_in_folder = bootstrap_images_in_folder

        if bootstrap_images_out_folder == "output_images":
            self.bootstrap_images_out_folder = "tmp/" + \
                bootstrap_images_out_folder+zip_file_name
            print("out_folder", self.bootstrap_images_out_folder)
        else:
            self.bootstrap_images_out_folder = "tmp/" + bootstrap_images_out_folder

        if bootstrap_csvs_out_folder == "output_csvs":
            self.bootstrap_csvs_out_folder = "tmp/" + \
                bootstrap_csvs_out_folder + zip_file_name
            print("out_csv", self.bootstrap_csvs_out_folder)
        else:
            self.bootstrap_csvs_out_folder = "tmp/" + bootstrap_csvs_out_folder

        self.bootstrap_helper = BootstrapHelper(
            images_in_folder=self.bootstrap_images_in_folder,
            images_out_folder=self.bootstrap_images_out_folder,
            csvs_out_folder=self.bootstrap_csvs_out_folder,
        )

    def apply(self):
        if os.path.exists("data/" + self.bootstrap_csvs_out_folder + "data.csv"):
            merged_df = pd.read_csv(
                "data/" + self.bootstrap_csvs_out_folder + "data.csv")
        else:
            self.bootstrap_helper.bootstrap(per_pose_class_limit=None)
            self.bootstrap_helper.align_images_and_csvs(
                print_removed_items=True)
            pose_embedder = FullBodyPoseEmbedder()

            pose_classifier = PoseClassifier(
                pose_samples_folder=self.bootstrap_csvs_out_folder,
                pose_embedder=pose_embedder,
                top_n_by_max_distance=30,
                top_n_by_mean_distance=10)
            outliers = pose_classifier.find_pose_sample_outliers()

            self.bootstrap_helper.remove_outliers(outliers)
            self.bootstrap_helper.align_images_and_csvs(
                print_removed_items=False)

            print("reached line 72")

            csv_files = glob.glob(self.bootstrap_csvs_out_folder + '/*.csv')

            print("reached line 76")
            # use os.path.basename() to extract only the file name from each path
            csv_file_names = [os.path.basename(file) for file in csv_files]

            print(csv_file_names)

            # Load squat_down.csv and drop column by index
            df1 = pd.read_csv(
                f"{self.bootstrap_csvs_out_folder}/{csv_file_names[0]}", header=None)
            df1 = df1.drop(df1.columns[0], axis=1)
            print(df1)
            # Load squat_up.csv and drop column by index
            df2 = pd.read_csv(
                f"{self.bootstrap_csvs_out_folder}/{csv_file_names[1]}", header=None)
            df2 = df2.drop(df2.columns[0], axis=1)
            print(df2)
            # Add new column to each dataframe with output values
            df1['output'] = 0
            df2['output'] = 1

            # Merge the two dataframes
            merged_df = pd.concat([df1, df2], ignore_index=True)
            
            print(merged_df)
            if not os.path.exists("data/" + self.bootstrap_csvs_out_folder):
                os.makedirs("data/" + self.bootstrap_csvs_out_folder)
            merged_df.to_csv(
                "data/" + self.bootstrap_csvs_out_folder + "/data.csv", index=False)

        return merged_df


if __name__ == "__main__":
    print("hello world")

    pre = PreProcessing(bootstrap_images_in_zip="../testing_data/pushups.zip")
    df = pre.apply()
    print(df)
