CC=gcc
CFLAGS=-Wall -Wno-endif-labels -lpcap

makesniff: sniffex.c
	$(CC) -o sniffex.x sniffex.c $(CFLAGS)

debug: sniffex.c
	$(CC) -o sniffex.x sniffex.c $(CFLAGS) -DDEBUG

clean:
	rm ./*.x
