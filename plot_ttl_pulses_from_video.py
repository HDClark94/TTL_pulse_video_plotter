import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

def process_video(video_path, bounding_box):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    summed_values = []

    x, y, w, h = bounding_box

    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Define the bounding box and extract that part of the frame
        roi = frame[y:y+h, x:x+w]

        # Convert the region of interest to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Sum all pixel values in the grayscale image
        summed_value = np.sum(gray_roi)
        summed_values.append(summed_value)

    cap.release()
    return summed_values

def plot_bounding_box(video_path, bounding_box, name):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return

    x, y, w, h = bounding_box

    # Draw the bounding box on the frame
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Convert the frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Plot the frame with the bounding box
    plt.imshow(frame_rgb)
    plt.title(f"Bounding Box on First Frame, {name}")
    plt.axis("off")
    plt.savefig(f'/Users/harryclark/TTL_pulse_video_plotter/results/bounding_box_{name}')
    cap.release()
    plt.close()

def plot_summed_values(summed_values, name):
    plt.plot(summed_values)
    plt.title(f"LED values, {name}")
    plt.xlabel("Frame Number")
    plt.ylabel("Summed Values")
    plt.savefig(f'/Users/harryclark/TTL_pulse_video_plotter/results/ttl_pulses_{name}')
    plt.close()

def plot_original_and_replaced_values(original, replaced, name):
    plt.plot(original, color="red")
    plt.plot(replaced, color="green")
    plt.title(f"original and replace LED values, {name}")
    plt.xlabel("Frame Number")
    plt.ylabel("Summed Values")
    plt.savefig(f'/Users/harryclark/TTL_pulse_video_plotter/results/original_and_replaced_values_{name}')
    plt.close()

def process_and_plot_video(video_path, bounding_box):
    summed_values = process_video(video_path, bounding_box)
    plot_summed_values(summed_values, name=os.path.basename(video_path).split('.avi')[0])
    plot_bounding_box(video_path, bounding_box, name=os.path.basename(video_path).split('.avi')[0])

def process_and_save_csv(video_path, bounding_box, bonsai_path, save=True):
    name=os.path.basename(video_path).split('.avi')[0]
    summed_values = process_video(video_path, bounding_box)
    plot_summed_values(summed_values, name=name)
    plot_bounding_box(video_path, bounding_box, name=name)

    # Load the CSV file with a space delimiter
    df = pd.read_csv(bonsai_path, delimiter=' ', header=None)
    plot_original_and_replaced_values(original=df.iloc[:, 5], replaced=summed_values, name=name)
    # replace values with new boundary box sums
    df.iloc[:, 5] = summed_values
    # Save the DataFrame back to a CSV file with a space delimiter
    if save:
        df.to_csv(bonsai_path, sep=' ', index=False, header=False)

bounding_box = (35, 460, 20, 12)  # x, y, width, height 
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D19_OF1.avi', bounding_box=bounding_box)
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D19_OF2.avi', bounding_box=bounding_box)
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D20_OF1.avi', bounding_box=bounding_box)
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D20_OF2.avi', bounding_box=bounding_box)
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M21_D18_OF1.avi', bounding_box=bounding_box)
#process_and_plot_video(video_path='/Users/harryclark/TTL_pulse_video_plotter/M21_D18_OF2.avi', bounding_box=bounding_box)
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D20_OF2.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M20_D20_2024-05-21_14-48-00_OF2/M20_D20_OF2.csv')
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D20_OF1.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M20_D20_2024-05-21_13-47-52_OF1/M20_D20_OF1.csv')
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D19_OF1.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M20_D19_2024-05-20_13-45-54_OF1/M20_D19_OF1.csv')
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M20_D19_OF2.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M20_D19_2024-05-20_14-49-24_OF2/M20_D19_OF2.csv')
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M21_D18_OF1.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M21_D18_2024-05-20_15-33-34_OF1/M21_D18_OF1.csv')
process_and_save_csv(video_path='/Users/harryclark/TTL_pulse_video_plotter/M21_D18_OF2.avi', bounding_box=bounding_box,
                     bonsai_path='/Volumes/cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Harry/Cohort11_april2024/of/M21_D18_2024-05-20_16-42-33_OF2/M21_D18_OF2.csv')