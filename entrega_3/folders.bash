#!/bin/bash

for i in $(seq -w 2 7); do
    mkdir "tests/test_0$i"
    cd "tests/test_0$i"
    touch "p0${i}_c.txt"
    touch "p0${i}_p.txt"
    touch "p0${i}_s.txt"
    touch "p0${i}_w.txt"

    cd "../.."
done