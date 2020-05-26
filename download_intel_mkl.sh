#!/usr/bin/env bash

intel_dir=/data/assets/intel
mkdir -p $intel_dir

cd $intel_dir

wget https://github.com/intel/mkl-dnn/releases/download/v0.17.4/mklml_lnx_2019.0.1.20180928.tgz
tar -zxvf mklml_lnx_2019.0.1.20180928.tgz
mv mklml_lnx_2019.0.1.20180928 mklml_lnx
tar -czvf $intel_dir/mklml_lnx.tgz mklml_lnx
rm -rf mklml_lnx mklml_lnx_2019.0.1.20180928.tgz

wget https://anaconda.org/anaconda/cudnn/7.3.1/download/linux-64/cudnn-7.3.1-cuda10.0_0.tar.bz2 -O ./cudnn.tar.bz2
wget https://github.com/Intel-bigdata/mkl_wrapper_for_non_CDH/raw/master/mkl_wrapper.jar
wget https://github.com/Intel-bigdata/mkl_wrapper_for_non_CDH/raw/master/mkl_wrapper.so