---
title: Archiving a Quartus project (creating a QAR)
draft: false
tags:
  - tools
---

prev > [[Quartus installation]]

*By Ricardo José Colom Palero*

When working with an electronic design tool such as Quartus, you will often need to copy your work to take it to another computer. Since Quartus works with projects, the obvious approach is to copy the whole project directory or compress it into an archive.

However, Quartus includes a utility that packs the project into a single file with the **.qar** extension, selecting only the files that are needed. It has two advantages: it automatically picks the files that are really required, using predefined configurations, and since the **.qar** extension is associated with Quartus, double-clicking the file unpacks the project and opens it.

## Procedure

1. In the Quartus menu, select **Project > Archive Project**. The **Archive Project** window opens:
   ![[assets/Generar QAR/Imagen009.jpg]]
2. Enter a name for the file in the **Archive file name** field.
3. Click **Advanced...** to open the window where you can customise which files will be included:
   ![[assets/Generar QAR/Imagen012.jpg]]
4. In **File set**, select the **Service request** preset:
   ![[assets/Generar QAR/Imagen011.jpg]]
5. Click **OK** to return to the **Archive Project** window.
6. Click **Archive**. The archive is created with the given name and the **.qar** extension and contains the project files. It is saved in the project directory unless you chose another location.

## Checking the archive

Once the **.qar** file has been created, it is a good idea to check its contents by unpacking it.

> [!danger] Do not unpack it in the original project folder
> Copy the **.qar** file to another folder and double-click it: Quartus will open, unpack the project into a folder named `project_name_restored` and open it.

next > [[Task 1 - Design of sequential systems]]
