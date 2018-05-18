#!/bin/bash

if [ -f $1 = 0 ]
  then
    RESULT=0
    PARM="fichero"
elif [ -d $1 = 0 ]
  then
    RESULT=1
    PARM="directorio"
else
  RESULT=2
  PARM="otra cosa"
fi

echo "$1 es ${PARM}, exit=${RESULT}"
exit ${RESULT} 
