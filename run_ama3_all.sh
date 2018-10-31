#!/bin/bash

ulimit -v 16000000000

trap exit SIGINT

# Note: AMA3 requires huge memory and runtime for preprocessing.
# For example:
# puzzle instances require 4.5GB per process / 2 hours,
# lightsout instances require 7.5GB per process / 4 hours on Xeon E5-2676 2.4 GHz.
# Each SAS+ file may become over 1GB.

# re: behavior --- The preprocessing results are precious. They are always
# unique for each problem, irregardless of heuristics. However, due to the huge
# memory requirement, it is inefficient to preprocess the same
# problem independently.
# 
# Therefore, when a process is preprocessing an instance, other
# instances solving the same instances are waited through a file lock.
# 
# Note that even when a ama3-planner process is waiting, it consumes nearly 700MB
# for already loaded NN image.

# Desired usage of this script is "./run_ama3_all.sh | parallel -j <number of processes>"
# where the number should be adjusted for the resource capacity on your system.

#### foolproof check

# ensuring if the system is built correctly
(
    make -C lisp
    git submodule update --init --recursive
    cd downward
    ./build.py -j $(cat /proc/cpuinfo | grep -c processor) release64
)

# in the weird case this happens
chmod -R +w noise-0.6-0.12-ama3

#### job submission

key=$1
mem=${2:-64g}

proj=$(date +%Y%m%d%H%M)

common=" -mem $mem -queue x86_1h -proj $proj"
dir=$(dirname $(dirname $(readlink -ef $0)))
export PYTHONPATH=$dir:$PYTHONPATH
export PYTHONUNBUFFERED=1
export PATH=VAL:$PATH

command="jbsub $common 'helper/ama3-planner.sh {1} {2} {3}'"


parallel -j 1 --no-notice "$command" \
         ::: samples/puzzle*mnist*100_20000_0.7*/${key}*.pddl \
         ::: noise-0.6-0.12-ama3/*/latplan.puzzles.puzzle_mnist/* \
         ::: blind ff

parallel -j 1 --no-notice "$command" \
         ::: samples/puzzle*mandrill*100_20000_0.7*/${key}*.pddl \
         ::: noise-0.6-0.12-ama3/*/latplan.puzzles.puzzle_mandrill/* \
         ::: blind ff

parallel -j 1 --no-notice "$command" \
         ::: samples/puzzle*spider*100_20000_0.7*/${key}*.pddl \
         ::: noise-0.6-0.12-ama3/*/latplan.puzzles.puzzle_spider/* \
         ::: blind ff

parallel -j 1 --no-notice "$command" \
         ::: samples/lightsout*digital*100_20000_0.7*/${key}*.pddl \
         ::: noise-0.6-0.12-ama3/*/latplan.puzzles.lightsout_digital/* \
         ::: blind ff

parallel -j 1 --no-notice "$command" \
         ::: samples/lightsout*twisted*100_20000_0.7*/${key}*.pddl \
         ::: noise-0.6-0.12-ama3/*/latplan.puzzles.lightsout_twisted/* \
         ::: blind ff

# parallel -j 1 --no-notice \
#          "jbsub $common './ama3-planner.py {1} {2} {3} > {2}/{1/}_{3}.ama3.log 2> {2}/{1/}_{3}.ama3.err'" \
#          ::: samples/hanoi* \
#          ::: noise-0.6-0.12-ama3/*/latplan.puzzles.hanoi/* \
#          ::: blind ff \
         # ::: remlic-1-1-0 remlic-2-2-0 remlic-4-4-0  actionlearner rf-2-others1b-t rf-5-others1b-t rf-10-others1b-t

