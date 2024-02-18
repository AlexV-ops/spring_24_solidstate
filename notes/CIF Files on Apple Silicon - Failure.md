Between Friday 02/16/24 and Sunday 02/18/24, I attempted to virtualize Windows 11 on my personal device, a 2020 M1 MacBook Air, in order to run [Pearson's Crystal Data](https://www.crystalimpact.com/pcd/), which is Windows-exclusive. Multiple attempts failed, and I've resorted to using a different device altogether moving forward. A description of failures and next steps is below. 
### Dual-booting Windows 11 and Windows 11 Enterprise

Possible virtual machine monitors (VMM):
* UTM -  ([UTM Documentation](https://docs.getutm.app/settings-apple/boot/)) - open source, used previously for Linux distribution virtualization for a different project (on different device)
* VMWare - ([VMWare Fusion Player - Personal Use License](https://customerconnect.vmware.com/en/evalcenter?p=fusion-player-personal-13)) - recommended by Prof. Oliynyk, enterprise software

##### Attempt 1: UTM
1. Installed UTM from [here](https://mac.getutm.app/), following standard installation instructions (.dmg file).
2. Used CrystalFetch ([Github](https://github.com/TuringSoftware/CrystalFetch))to generate Windows 11 (Home Edition) installer ISO for ARM64 architecture. This ISO was used for all subsequent attempts, and was up-to-date as of 12/6/23. 
3. Generated drivers and SPICE tools from UTM wizard, which nominally accounts for all dependencies for smoothly installing Windows 11 on any ARM architecture (like Apple M1 silicon).
4. Generated first kernel of virtual environment, and transferred to external SSD to accommodate minimum 64 GB partition. 
5. **ERROR 1**: Boot into UEFI environment, rather than into standard Windows installation wizard. 
	**SOLUTION**: Press any key multiple times to simulate boot from external media.
6. Proceed through Windows installation wizard as normal, selecting language, region, declining to enter product activation code, and starting installation process. 
7. **ERROR 2**: ```Windows cannot install required files. The file may be corrupt or missing. Make sure all files required for installation are available, and restart the installation. Error code: 0x80070570.```
	**SOLUTION**: Return to UTM, convert file type in advanced settings to FAT files, and reinitialize. Error code 0x80070570 is usually the result of a corrupted directory, but can be circumvented by changing file types for some of the dependencies.
8. **ERROR 3**: ```Windows could not apply unattended settings during pass [offlineServicing].
9. No solution found; error plausibly tied to the SPICE tools installed (by default) alongside ISO by UTM. I transitioned to attempt 2 with VMWare.

##### Attempt 2: VMWare
1. Installed VMWare Fusion Player - Personal License [here](https://customerconnect.vmware.com/en/evalcenter?p=fusion-player-personal-13). Followed instructions (.dmg file) and entered the product activation code generated after creating an account.
2. Cleaned up the same ISO used previously in Attempt 1. 
3. Pressed a random key multiple times to go past the UEFI boot loop and enter standard Windows installation wizard.
4. **ERROR 4**: ```This PC can't run Windows 11. This PC doesn't meet the minimum system requirements to install this version of Windows. For more information, visit https://aka.ms/WindowsSysReq.```
	   **SOLUTION**: 
	1. Option+FN+F10 -> open Command Prompt
	2. ```regedit.exe``` -> open Registry Editor
	3. ```HKEY_LOCAL_MACHINES\SYSTEM\Setup``` -> Create ```New -> Key``` named LabConfig -> Create 2 instances of ```New -> DWORD (32 bit)``` named ```BypassTPMCheck``` and ```BypassSecureBootCheck```. Set both values to ```1```. Restart virtual machine and proceed with reinstallation from step 1.
5. **ERROR 5**: Software crash, MacOS freeze. 
6. No solution found, after 3 attempts. Throttling RAM usage of VMWare doesn't seem to work; I have 8 GB of RAM in total on my hard drive, of which I devoted 4 to the virtual machine. This ended up being a runaway process, which inevitably crashed both the virtual machine and my actual device. After being warned that my hard drive itself was at risk of corruption, I terminated the virtual machine and cleaned up my drive. 

#### Next Steps
I have procured a spare Windows 10 machine, and am following the recorded advice for how to use PCD (as uploaded on Teams). I still have both UTM and VMWare on my laptop, but given that I seem to have an insurmountable hardware limitation I'm abandoning virtualization, at least for now. I am working on uploading proof of CIF file extraction by EOD (02/18/24).

