# Orthopedic Rehabilitation System

Basis paper:  
Everybody Dance Now  
Caroline Chan, Shiry Ginosar, Tinghui Zhou, Alexei A. Efros  

## Prerequisites
1. [PyTorch](https://pytorch.org/)
2. Python Library [Dominate](https://github.com/Knio/dominate)
```
pip install dominate
```
3. Clone this repository
```
git clone https://github.com/AnnikaAlonzo/DSP-1-2223-C2-Orthopedic-Rehabilitation-Exercise-System.git
```


## Training

#### Global Stage
We follow similar stage training as in [pix2pixHD](https://github.com/NVIDIA/pix2pixHD). We first train a "global" stage model at 512x256 resolution
```
# train a model at 512x256 resolution
python train_fullts.py \
--name MY_MODEL_NAME_global \
--dataroot MY_TRAINING_DATASET \
--checkpoints_dir WHERE_TO_SAVE_CHECKPOINTS \
--loadSize 512 \
--no_instance \
--no_flip \
--tf_log \
--label_nc 6
```

## Testing

The full checkpoint will be loaded from --checkpoints_dir/--name (i.e. if flags: "--name foo \ ... --checkpoints_dir bar \"" are included, checkpoints will be loaded from foo/bar)
Replace --howmany flag with an upper bound on how many test examples you have

#### Global Stage
```
# test model at 512x256 resolution
python test_fullts.py \
--name MY_MODEL_NAME_global \
--dataroot MY_TEST_DATASET \
--checkpoints_dir CHECKPOINT_FILE_LOCATION \
--results_dir WHERE_TO_SAVE_RESULTS \
--loadSize 512 \
--no_instance \
--how_many 10000 \
--label_nc 6
```

## Dataset preparation

Our dataset preparation code is based on output formats from [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) and currently supports the COCO, BODY_23, and BODY_25 pose output format as well as hand and face keypoints. To install and run OpenPose please follow the directions at the [OpenPose repository](https://github.com/CMU-Perceptual-Computing-Lab/openpose).

### graph_train.py
will prepare a train dataset with subfolders
- train_label (contains 1024x512 inputs)
- train_img (contains 1024x512 targets)
- train_facetexts128 (contains face 128x128 bounding box coordinates in .txt files)
No smoothing
```
python graph_train.py \
--keypoints_dir /data/scratch/caroline/keypoints/jason_keys \
--frames_dir /data/scratch/caroline/frames/jason_frames \
--save_dir /data/scratch/caroline/savefolder \
--spread 4000 25631 1 \
--facetexts
```

### graph_avesmooth.py
will prepare a dataset with averaged smoothed keypoints with subfolders (usually for validation)
- test_label (contains 1024x512 inputs)
- test_img (contains 1024x512 targets)
- test_factexts128 (contains face 128x128 bounding box coordinates in .txt files)
```
python graph_avesmooth.py \
--keypoints_dir /data/scratch/caroline/keypoints/wholedance_keys \
--frames_dir /data/scratch/caroline/frames/wholedance \
--save_dir /data/scratch/caroline/savefolder \
--spread 500 29999 4 \
--facetexts
```

## Acknowledgements

Model code adapted from [pix2pixHD](https://github.com/NVIDIA/pix2pixHD) and [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

Data Preparation code based on outputs from [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
