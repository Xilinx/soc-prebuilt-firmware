# prebuilt-firmware
This repository contains a series of boot asset files required to rebuild a BOOT.BIN for each target board along with a top level Makefile and simple build targets.  The full prebuilt SD card image for each target can also be found in the  [Linux Prebuilt Images](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842316/Linux+Prebuilt+Images) wiki page under the appropriate release version.

## File origins
| Folder        |Origin                                                                                                                                          |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------|
|k26-som-kria   | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|kr260-kria     | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|kv260-kria     | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|vck190-versal  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|vmk180-versal  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|vpk120-versal  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|vpk180-versal  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zc702-zynq     | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zc706-zynq     | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu102-zynqmp  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu104-zynqmp  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu106-zynqmp  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu111-zynqmp  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu1275-zynqmp | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |
|zcu216-zynqmp  | [BSP](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html) Built with PetaLinux 2023.1 |


## Command Examples

### default make target (all):
The following commands build BOOT.BIN for the board specified in the variable *board*, using target architecture specified by *arch*.  If necessary, bootgen shall be fetched and compiled from source if not already present in the working directory.

```
make board={boardname}-zynqmp arch={archname}

 make board=zcu102-zynqmp  arch=zynqmp
 make board=kr260-kria     arch=zynqmp
 make board=vck190-versal  arch=versal
```
### make clean:
Remove BOOT.BIN for a specified board:

```
make board={boardname}-zynqmp arch={archname} clean
```

### make deepclean:
Remove BOOT.BIN for the specified board and also remove the downloaded bootgen sources and compiled binary:

```
board={boardname}-zynqmp arch={archname} deepclean
```

### *bootgen_version* variable:

If a different version of bootgen is required, the variable *bootgen_version* can be used to override the default.  If used, the variable must be specified for all make targets in which it should be overwritten.  The default value of *bootgen_version* can be found in the top of the Makefile, and should reflect the latest bootgen branch.  A list of current branches can be found at https://github.com/Xilinx/bootgen/branches .  This should not be changed from the default unless there is a good reason, and these sources will not have been tested with versions other than the default.

```
make bootgen_version=xlnx_rel_v2023.1 board=kr260-kria arch=zynqmp
make bootgen_version=xlnx_rel_v2023.1 board=kr260-kria arch=zynqmp clean
make bootgen_version=xlnx_rel_v2023.1 board=kr260-kria arch=zynqmp cleanall
```

---
(c) Copyright 2023 Advanced Micro Devices, Inc / Xilinx, Inc All rights reserved.
