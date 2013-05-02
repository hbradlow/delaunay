sudo apt-get update
sudo apt-get install git
sudo apt-get install gcc
sudo apt-get install pip
sudo apt-get install python-dev
sudo pip install numpy
git clone git://github.com/hbradlow/delaunay.git
cd delaunay
wget http://www.cs.berkeley.edu/~jrs/input/ttimeu10000.node.gz
wget http://www.cs.berkeley.edu/~jrs/input/ttimeu100000.node.gz
wget http://www.cs.berkeley.edu/~jrs/input/ttimeu1000000.node.gz
