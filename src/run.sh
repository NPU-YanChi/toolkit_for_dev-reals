python /home/pjlab/DATA/DEV-Reals/toolkit_for_dev-reals/src/scripts/npzs_to_frame.py \
    --input /home/pjlab/DATA/DEV-Reals/room1/davis346/event/events.csv \
    --output /home/pjlab/DATA/DEV-Reals/room1/davis346/event_frame \
    --rgb /home/pjlab/DATA/DEV-Reals/room1/rgbd/rgb \
    --intrinsic /home/pjlab/DATA/DEV-Reals/room1/davis346/intrinsic/intrinsic.yaml \
    --winsz 10

python /home/pjlab/DATA/DEV-Reals/toolkit_for_dev-reals/src/scripts/npzs_to_frame.py \
    --input /home/pjlab/DATA/DEV-Reals/room2/davis346/event/events.csv \
    --output /home/pjlab/DATA/DEV-Reals/room2/davis346/event_frame \
    --rgb /home/pjlab/DATA/DEV-Reals/room2/rgbd/rgb \
    --intrinsic /home/pjlab/DATA/DEV-Reals/room2/davis346/intrinsic/intrinsic.yaml \
    --winsz 10