#/bin/bash

if [ $# -lt 1 ] ; then
    echo "Usage   : $0 cmdfile.txt"
    echo "Example : $0 cmds_example.txt"
  exit 1
fi


for i in `seq 0 9` ; do 
  echo $i 
  ./bin/mg5_aMC $1
done
