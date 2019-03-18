HTML=/home/yndrd

all:

install:
	rsync -av html/ $(HTML)/
	rsync -av bin/conv2arde.pl $(HTML)/
