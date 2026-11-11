---
title: "Help: creating QAR files"
draft: false
tags:
  - tools
---

prev > [[sdp/en/quartus-installation|Help: installing Quartus]]

When working with an electronic design tool such as Quartus, you often need to copy your work, either to share it with someone or to continue on another computer. Since Quartus works with projects, the obvious approach is to copy the whole project folder or compress it.

There is a much better alternative: Quartus includes a utility that packs the project into a single file with the **.QAR** extension, including only the files that are needed. It automatically selects the essential files using predefined configurations, so the archive is as small as possible, and since the **.QAR** extension is associated with Quartus, a double click unpacks the project and opens it.

## Procedure

1. In the Quartus menu, select **Project > Archive Project**. The **Archive Project** window opens:
   ![[assets/generar-qar/imagen009.jpg]]
2. Type the file name in **Archive file name**.
3. Click **Advanced...** to open the window where you choose which files are included:
   ![[assets/generar-qar/imagen012.jpg]]
4. Under **File set**, select the **Service request** preset:
   ![[assets/generar-qar/imagen011.jpg]]
5. Click **OK** to return to **Archive Project**.
6. Click **Archive**. Quartus creates a file with the given name and the **.QAR** extension containing the project files, in the project folder unless you chose another location.

> [!tip] Memory initialisation files
> The `.hex` or `.mif` files that initialise memories are not always included by default. Add them manually in the **Advanced...** window with the **Add...** button.

## Checking the archive

It is a good idea to unpack the **.QAR** and open it in Quartus to check that its contents are correct.

> [!danger] Do not unpack it in the original project folder
> The project could become corrupted. Copy the **.QAR** to another folder and double-click it: Quartus will open, unpack the project into a folder called `<project_name>_restored` and open it.

next > [[sdp/en/project1-lighting-effect|Project 1: Design of a lighting effect]]
