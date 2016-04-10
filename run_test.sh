#!/bin/bash
#Todo: сделать как-то более нормально. М.б. созавать базу руками при старте тестов и удолять потом.
sleep 1 && python -m unittest discover -p "*_test.py"