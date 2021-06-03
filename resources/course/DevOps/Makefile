CC=gcc
CFLAGS=-Wall -Wno-endif-labels -lpcap

makesniff: sniffex.c
	$(CC) -o sniffex.x sniffex.c $(CFLAGS)

clean:
	rm ./*.x
