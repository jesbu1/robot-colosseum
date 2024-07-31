#!/usr/bin/env bash
#export PYOPENGL_PLATFORM=opengl
#export DISPLAY=:0.0
ngpus=1
mincpus=16
export PERACT_ROOT=$HOME/peract_dir/peract

if [ $# -eq 0 ]
  then
    echo "Collecting demos from all tasks"
    tasks=("basketball_in_hoop"
           "close_box"
           "close_laptop_lid"
           "empty_dishwasher"
           "get_ice_from_fridge"
           "hockey"
           "meat_on_grill"
           "move_hanger"
           "wipe_desk"
           "open_drawer"
           "slide_block_to_target"
           "reach_and_drag"
           "put_money_in_safe"
           "place_wine_at_rack_location"
           "insert_onto_square_peg"
           "stack_cups"
           "turn_oven_on"
           "straighten_rope"
           "setup_chess"
           "scoop_with_spatula")
else
    echo "Collectins demos from task $1"
    tasks=("$1")
fi

# idx from which to collect demos (use -1 for all idxs)
#SAVE_PATH=$HOME/data/colosseum_training_dataset
    #--container-mounts $HOME/robot-colosseum:/home/jeszhang/robot-colosseum,$HOME/data/:/home/jeszhang/data/,/tmp/.X11-unix:/tmp/.X11-unix,$HOME/.Xauthority:/home/.Xauthority \
                #bash -c "cd ../robot-colosseum && conda run --no-capture-output -n 3d_diffuser_actor xvfb-run -a /bin/bash collect_training_dataset.sh $task"
	#bash -c "cd ../robot-colosseum && xvfb-run -a bash collect_training_dataset.sh $task"
                #--partition=grizzly,polar,polar2,polar3,polar4,batch_singlenode,interactive \ # grizzly seems to have issues with display
for task in "${tasks[@]}"
do
    srun -A nvr_srl_simpler --gres gpu:$ngpus \
                --mincpus=$mincpus \
                --nodes=1 \
                --partition=polar,polar2,polar3,polar4,batch_singlenode \
                --time=4:0:0 \
                --mem=64G \
                --container-image /lustre/fsw/portfolios/nvr/users/$USER/cache/srl_jesse_3d_diffuser_image.sqsh \
                --container-mounts $HOME/robot-colosseum/collect_eval_dataset.sh:/home/jeszhang/robot-colosseum/collect_eval_dataset.sh,/home/jeszhang/data/:/home/jeszhang/data/,/usr/bin/nvidia-xconfig:/usr/bin/nvidia-xconfig \
                bash -c "cd ../robot-colosseum && xvfb-run -a conda run --no-capture-output -n 3d_diffuser_actor bash collect_eval_dataset.sh $task" &
done
