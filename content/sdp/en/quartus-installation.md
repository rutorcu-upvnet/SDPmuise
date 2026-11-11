---
title: "Help: installing Quartus"
draft: false
tags:
  - tools
---

prev > [[sdp/en/index|home]]

The lab sessions of this course use Altera's **Quartus** software. The lab computers have version **17.1.1 Internal Build 593** installed. You can (and we recommend you do) install the same version on your own computer so that you can also work outside the lab without compatibility problems. This page explains how.

## Download

The following link takes you to the Altera download center: [Altera download center](https://www.intel.com/content/www/us/en/collections/products/fpga/software/downloads.html)

![[assets/instalar-quartus/captura-27-01-26-1.png]]

In the software drop-down menu choose **Quartus Prime Lite** and, in the next one, **version 17.1**, which is the one used in the lab. The last drop-down lets you choose between the Windows and Linux versions (there is no Mac version).

> [!warning] Be careful
> Choose the **Lite** edition, which is free, and not the **Standard** or **Pro** editions, which require a paid licence.

![[assets/instalar-quartus/captura-27-01-26-2.png]]

## Recommended packages

The complete software includes many components that are not used in any course of the degree, so we recommend downloading only the ones you need. In the **Individual Files** tab, click **Download** for these components:

- **Quartus Prime (includes Nios II EDS)**, 1.7 GB
- **ModelSim-FPGA Edition (includes Starter Edition)**, 1.1 GB
- **Cyclone IV device support**, 466.7 MB

Once downloaded, install them by double-clicking the Quartus file (`QuartusLiteSetup-17.1.0.590-windows.exe`). With the default options, all three components are installed automatically.

![[assets/instalar-quartus/captura-27-01-26-3.png]]

> [!note] Alternative: full download
> In the **Multiple Download** tab, the **Download** button downloads a 5.8 GB file with the complete, free version of Quartus, which you install following the instructions on the same page. The drawbacks are the larger download and installed size, and that you need a decompression tool (such as WinRAR) to unpack it before installing.

## Update to 17.1.1

After installing version 17.1 you must apply an update to reach **17.1.1 Internal Build 593**, the same as in the lab. On the same download page, in the **Updates** tab, download **Quartus Prime Software v17.1 Update 1** (1.6 GB) and follow the instructions on the page to install it.

![[assets/instalar-quartus/captura-27-01-26-4.png]]

next > [[sdp/en/qar-archive|Help: creating QAR files]]
