all:
	./bootgen -image $(board)/bootgen.bif -arch $(arch) -o $(board)/BOOT.BIN
