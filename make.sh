#!/bin/bash

make -f Makefile.local >& errlog.txt ; less errlog.txt
