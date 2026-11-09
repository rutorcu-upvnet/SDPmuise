---
title: Installing Quartus on your computer
draft: false
tags:
  - tools
---

prev > [[sdp/en/index|home]]

*By Ricardo José Colom Palero*

One of the goals of this course is that every digital design is not only verified in simulation but also tested physically on hardware. In the lab we use the **DE2-115** evaluation board, developed by Terasic together with the Altera University Program. Alongside the hardware we use Altera's (now Intel FPGA) **Quartus** software to build the designs.

The DE2-115 board carries an FPGA from Altera's **Cyclone IV E** family, specifically the **EP4CE115F29C7** device. The lab sessions use Quartus version **17.1.1 Internal Build 593**, which is already installed in the lab. This page explains how to get the same version on your own computer, so that you can work at home without compatibility problems.

## Download

The following link takes you to the Intel FPGA download center: [Intel FPGA Download Center](https://www.intel.com/content/www/us/en/collections/products/fpga/software/downloads.html)

![[assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.30.48.png]]

On that page, search for "17.1" to narrow down the results. Then pick **Intel Quartus Prime Lite Edition Design Software Version 17.1 for Windows** (or Linux, if that is your operating system).

> [!warning] Be careful
> Choose the **Lite** edition, which is free, and not the **Standard** or **Pro** editions, which require a paid licence.

![[assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.41.16.png]]

Under the **Multiple Download** tab, the *Download* button starts downloading a 5.8 GB file with the complete, free version of Quartus. This is the easiest option, although it includes more components than you need.

If the file is too big, you can download only the packages you will use from the **Individual Files** tab. As shown in the image, the courses in this degree only need:

- Quartus Prime (includes Nios II EDS), 1.7 GB.
- ModelSim-Intel FPGA Edition (includes Starter Edition), 1.1 GB.
- Cyclone IV device support, 466.6 MB.

![[assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.40.05.png]]

## Installation and update

Once the files are downloaded, install Quartus following the instructions on the same web page.

There is an update for version 17.1 that brings it to **17.1.1 Internal Build 593**, the same version as in the lab. Download it from the **Updates** tab, as shown in the image, and follow the instructions on the page to install it.

![[assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-16.23.00.png]]

next > [[sdp/en/qar-archive|Creating a QAR archive]]
