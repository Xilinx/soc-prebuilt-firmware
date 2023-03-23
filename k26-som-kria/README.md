Steps to Flash and Boot PetaLinux Image Using WIC Image

-->To generate the WIC image in PetaLinux project see petalinux-package --wic Command Examples.
-->Go to the <plnx-proj-root>/images/linux or <plnx-proj-root>/pre-built/linux/images/ directory.For example, cd images/linux/.
-->If the WIC image is compressed with XZ format, extract the petalinux-sdimage.wic.xz file using xz command.For example, xz -d petalinux-sdimage.wic.xz
  Note: If xz package is not installed in your build machine, use the prebuilt xz binary from $PETALINUX/components/yocto/buildtools/sysroots/x86_64-petalinux-linux/usr/bin/xz
-->Flash the extracted petalinux-sdimage.wic image into the SD card
    Flash the WIC image in Linux :

To flash the WIC image to SD card in Linux machines, connect the SD card to the host system and use the dd command:
dd if=petalinux-sdimage.wic of=/dev/sd<X> conv=fsync

Note: You need sudo access to do this.
    Flash the WIC image in Windows :

To flash the WIC image to the SD card in Windows, you can use any of the following:
    BalenaEtcher tool
    Win32DiskImager
-->Insert the SD card into the board and boot the system.
-->Connect the serial port on the board to your workstation.
-->Open a console on the workstation and start the preferred serial communication program (For example: kermit, minicom, gtkterm) with the baud rate set to 115200 on that console.
-->Power off the board.
-->Set the boot mode of the board to SD boot. Refer to the board documentation for details.
-->Plug the SD card into the board.
-->Power on the board. The boot logs display on the serial console:  
