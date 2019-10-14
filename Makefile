default: bench

RUSTPATH ?= ../rustomata/

bench: 
	./bench.sh ${RUSTPATH}