#!/bin/bash

# Define the input directories for the two datasets
input_dirs=("/DATA/enslam/enslamdata1"
            "/DATA/enslam/enslamdata2"
            "/DATA/enslam/enslamdata3"
            "/DATA/enslam/enslamdata4"
            "/DATA/enslam/enslamdata5"
            "/DATA/enslam/enslamdata6"
            "/DATA/enslam/enslamdata7"
            "/DATA/enslam/enslamdata8")

# Define the winsz values to loop over
winsz_values=(5 10)

# Loop over the input directories and winsz values
for input_dir in "${input_dirs[@]}"; do
  for winsz in "${winsz_values[@]}"; do
    # Define the output directory based on the input directory and winsz value
    output_dir="${input_dir}/davis346/event_frame_${winsz}"

    # Run the npzs_to_frame.py script with the appropriate arguments
    python /home/pjlab/yanchi/toolkit_for_dev-reals/src/scripts/npzs_to_frame.py \
        --input "${input_dir}/davis346/event/events.csv" \
        --output "${output_dir}" \
        --rgb "${input_dir}/rgbd/rgb" \
        --intrinsic /home/pjlab/qudelin/Co-SLAM/configs/DEVReals/devreals.yaml \
        --winsz "${winsz}"
  done
done