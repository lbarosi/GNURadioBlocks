#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/python/fits_sink"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/build/python/fits_sink":"$PATH"
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/build/test_modules:$PYTHONPATH
/opt/miniconda3/envs/gnuradio310/bin/python /home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/python/fits_sink/qa_fits_sink.py 
