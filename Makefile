bootgen_version ?= xlnx_rel_v2023.2

ifndef board
$(error board is not set)
endif

all: bootgen.$(bootgen_version)
	cd $(board) && ../bootgen.$(bootgen_version) -w -image bootgen.bif -arch $(arch) -o BOOT.BIN
bootgen.$(bootgen_version): bootgen.git.$(bootgen_version)
	ln -s bootgen.git.$(bootgen_version)/bootgen bootgen.$(bootgen_version)
bootgen.git.$(bootgen_version):
	git clone --branch $(bootgen_version) https://github.com/Xilinx/bootgen bootgen.git.$(bootgen_version)
	$(MAKE) -C bootgen.git.$(bootgen_version)
clean:
	rm -f $(board)/BOOT.BIN
deepclean: clean
	rm -f bootgen.$(bootgen_version)
	rm -rf bootgen.git.$(bootgen_version)
