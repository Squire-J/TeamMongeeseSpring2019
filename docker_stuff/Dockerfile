FROM ubuntu:18.04
MAINTAINER gaobing@uvic.ca

COPY polymer-v4.9.tar.gz /
    #here you need put the script name here.

RUN    apt-get -y update
#RUN    sed -i 's/$/ universe/' /etc/apt/sources.list
RUN    apt-get -y install software-properties-common build-essential

RUN    apt-get -y update
RUN    apt-get -y install python3 wget python3-pip
#RUN    add-apt-repository -y ppa:ubuntugis/ppa


RUN    apt-get -y install gdal-bin python-gdal python3-gdal python-pyproj libhdf4-dev python3-h5py libgrib-api-dev libgrib2c-dev libnetcdf-dev netcdf-bin
RUN    apt-get -y update

RUN    pip3 install jupyter matplotlib numpy pandas scipy
RUN    pip3 install pyepr 
RUN    pip3 install cython pyproj 
RUN   pip3 install python-hdf4 glymur lxml
RUN    pip3 install netcdf4
RUN      pip3 install h5netcdf
RUN    wget -nc https://hdfeos.org/software/pyhdf/pyhdf-0.9.0.tar.gz
RUN    tar zxvf pyhdf-0.9.0.tar.gz
WORKDIR pyhdf-0.9.0
RUN    python3 setup.py install
RUN    python3 -m wheel convert /pyhdf-0.9.0/dist/pyhdf-0.9.0-py3.6-linux-x86_64.egg
RUN    python3 -V
RUN    pip3 install /pyhdf-0.9.0/pyhdf-0.9.0-cp36-none-linux_x86_64.whl
WORKDIR ../
RUN    tar zxvf polymer-v4.9.tar.gz
WORKDIR  polymer-v4.9
RUN    make auxdata_all
RUN    python3 setup.py build_ext --inplace
RUN    make ancillary
RUN   pip3 install filelock 
COPY algorithmBoilerplate.py /polymer-v4.9
#WORKDIR ../


ENTRYPOINT [ "sh", "-c", "echo $HOME" ]
   
    
    



