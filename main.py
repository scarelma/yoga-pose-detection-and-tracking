from src.cpc import CustomPoseClassification
from src.cpcount import CustomRepetitionCounter
import cv2
import numpy as np

from mediapipe.python.solutions import drawing_utils as mp_drawing


def main():
    CPC = CustomPoseClassification(posename = 'squats')
    CPC.loadOrTrain()
    repetition_counter = CustomRepetitionCounter(forModel="squats")

    video_cap = cv2.VideoCapture(0)

# Get some video parameters to generate output video with classificaiton.
    video_n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_fps = video_cap.get(cv2.CAP_PROP_FPS)
    video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    from mediapipe.python.solutions import pose as mp_pose


    # Folder with pose class CSVs. That should be the same folder you using while
    # building classifier to output CSVs.
    pose_samples_folder = 'fitness_poses_csvs_out'

    # Initialize tracker.
    pose_tracker = mp_pose.Pose(min_tracking_confidence=0.92, min_detection_confidence=0.8)
    # Open output video.
    # out_video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), video_fps, (video_width, video_height))

    frame_idx = 0
    output_frame = None
    # with tqdm.tqdm(total=video_n_frames, position=0, leave=True) as pbar:
    while True:
        # Get next frame of the video.
        success, input_frame = video_cap.read()
        if not success:
            break

        # Run pose tracker.
        input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
        result = pose_tracker.process(image=input_frame)
        pose_landmarks = result.pose_landmarks

        # Draw pose prediction.
        output_frame = input_frame.copy()
        if pose_landmarks is not None:
            mp_drawing.draw_landmarks(
                image=output_frame,
                landmark_list=pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS)

        if pose_landmarks is not None:
            # Get landmarks.
            # print("yes", end=" ")
            frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
            pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                                    for lmk in pose_landmarks.landmark], dtype=np.float32)

            pose_landmarks = pose_landmarks.flatten()
            pred = CPC.predict(pose_landmarks.reshape(1, -1))
            # print(pose_landmarks.shape, end=" ")
            # print(type(pose_landmarks), end = " ")
            # print(pred)
            repetition_counter.countRepetitions(pred)

            text = str(int(repetition_counter.repetitionsCount))

    # Choose a font and size
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1

            # Determine the size of the text
            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=1)

            # Calculate the position to write the text (centered on the image)
            text_x = int((output_frame.shape[1] - text_size[0]) / 2)
            text_y = int((output_frame.shape[0] + text_size[1]) / 2)

            # Draw the text on the image
            cv2.putText(output_frame, text, (text_x, text_y), font,
                        font_scale, (255, 255, 255), thickness=1)

            # output_frame.text((output_width * 0.85,
            #                   output_height * 0.05),
            #                  str(repetitions_count))

            # assert pose_landmarks.shape == (
            #     33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)

            # # Classify the pose on the current frame.
            # pose_classification = pose_classifier(pose_landmarks)

            # # Smooth classification using EMA.
            # pose_classification_filtered = pose_classification_filter(
            #     pose_classification)

            # # Count repetitions.
            # repetitions_count = repetition_counter(
            #     pose_classification_filtered)
        # else:
            # No pose => no classification on current frame.
            # print("no", end=" ")
            # pose_classification = None

            # Still add empty classification to the filter to maintaing correct
            # smoothing for future frames.
            # pose_classification_filtered = pose_classification_filter(dict())
            # pose_classification_filtered = None

            # # Don't update the counter presuming that person is 'frozen'. Just
            # # take the latest repetitions count.
            # repetitions_count = repetition_counter.n_repeats

        # Draw classification plot and repetition counter.
        # output_frame = pose_classification_visualizer(
        #     frame=output_frame,
        #     pose_classification=pose_classification,
        #     pose_classification_filtered=pose_classification_filtered,
        #     repetitions_count=repetitions_count)

        # Save the output frame.
        # out_video.write(cv2.cvtColor(np.array(output_frame), cv2.COLOR_RGB2BGR))
        # cv2.imshow('out',np.array(output_frame))

        cv2.imshow("Output Frame", cv2.cvtColor(
            np.array(output_frame), cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(1) & 0xFF

        # exit on pressing 'q'
        if key == ord('q'):
            break  # wait for 1 millisecond to display the frame

        # Show intermediate frames of the video to track progress.
        # if frame_idx % 50 == 0:
        #   show_image(output_frame)

        # frame_idx += 1
        # pbar.update()

    # Close output video.
    video_cap.release()

    # Release MediaPipe resources.
    pose_tracker.close()

if __name__=="__main__":
    main()
# from src.prep import PreProcessing
# from src.cpc import CustomPoseClassification
# pre = PreProcessing(bootstrap_images_in_zip="testing_data/pushups.zip")
# df = pre.apply()
# exercise_name = "pushups"
# CPC = CustomPoseClassification(df=df, posename=exercise_name)
# CPC.loadOrTrain()

