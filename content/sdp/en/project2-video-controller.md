---
title: "Project 2: Design of a video controller"
draft: false
tags:
  - verilog
  - display
  - memories
---

prev > [[sdp/en/project1-lighting-effect|Project 1: Design of a lighting effect]]

In this project you design a **video controller** for the touchscreen of the DE2-115 board. The system includes a synchronism generator and the circuitry needed to display images and text on the screen. As an optional extension, a keyboard controller can be added to show on the screen what you type.

## Goals

- Understand how a video controller works.
- Design complex sequential systems.
- Design systems based on ROM memories.
- Create and instantiate *IP cores*.
- Debug circuits with memories while they are running.

## Work to be done

**First deliverable:**

- Part 1: circuit and testbench.
- Part 2: circuit, testbench and on-board test.
- Part 3: circuit and testbench.
- Report (Parts 1 to 3 only), with the *RTL Viewer* results, the analysis/synthesis warnings report and the images generated with the *Screen Simulator*.

**Second deliverable:**

- Part 4: circuit and testbench.
- Part 5: circuit, testbench and on-board test, including the *Memory Content Editor* test to change the displayed character. The final version must generate 16 × 16 characters.
- Part 6: circuit, testbench and on-board test, including the *Memory Content Editor* test to change the displayed text.
- Report (Parts 4 to 6 only), with the *RTL Viewer* results, the analysis/synthesis warnings report and the images generated with the *Screen Simulator*.

## Introduction

### Display on a screen

In painting, graphic design, photography, printing and television, colour theory is a set of basic rules for mixing colours to obtain a desired effect by combining lights or pigments. White light can be produced by combining red, green and blue light, while combining cyan, magenta and yellow pigments produces black.

An **additive** colour system emits light directly from a light source. Additive synthesis usually uses red, green and blue light to produce all other colours: the three primaries at equal intensity give white, and varying the intensity of each one produces the whole spectrum.

![[assets/control-pantalla/visualizacion-en-una-pantalla/2000px-additivecolor.png]]

The **RGB model** is based on additive synthesis: it represents a colour as the sum of the three primary light colours, red, green and blue. All colours that can be created by mixing them make up the colour spectrum; with no light we perceive black. Primary light colours are used in monitors, TVs, projectors and, in general, any system that combines materials emitting in the red, green and blue ranges.

#### Representation of images

Formally, an image is the spatial distribution of light irradiated on a plane: a continuous function of two variables, the **x** and **y** coordinates, that gives the light intensity at each point. To represent it digitally, coordinates and intensity must be discretised: a digital image is one in which both are finite and discrete. Each point with discrete coordinates is a **pixel** (*picture element*). A digital image is usually a rectangular grid of **N** columns and **M** rows: an image of **N × M pixels**.

![[assets/control-pantalla/representacion-imagenes/imagen01.png]]

> [!note] Notation
> In mathematics a matrix is described as rows × columns (here, **M × N**). For screens, however, the horizontal dimension, i.e. the columns, is always given first, which is why we say the image has **N × M** pixels.

The first pixel is the top-left one, at coordinates **(0, 0)**. Each pixel holds colour information in separate channels (sub-pixels) that represent the primary components of the colour model in use, RGB or any other.

**Colour depth**, in bits per pixel (bpp), is the number of bits used to represent the colour of a pixel. With **n** bits each pixel can take **2ⁿ** values, i.e. **2ⁿ** colours. Since the byte is the almost universal basic unit of storage, colour depths are usually divisors or multiples of 8 (1, 2, 4, 8, 16, 24 and 32), except for a few such as 10 or 15 used by some graphics devices.

#### Onscreen image

To show an image on a screen you must take its characteristics into account, mainly the size of the display area and the colour depth. The size given by the manufacturer (horizontal first, in pixels) refers to the **display area**: how many pixels are visible.

Internally, however, the screen has a much larger area: around the visible region there are "black" zones (grey in the image) used to let the synchronism signals settle. They are called ***Horizontal Back Porch*** and ***Horizontal Front Porch*** to the left and right of the visible area, and ***Vertical Back Porch*** and ***Vertical Front Porch*** above and below it.

![[assets/control-pantalla/visualizacion-en-pantalla/imagen02.png]]

These zones are not symmetrical: the back porches are larger than the front porches, because the syncs need more settling time before display. A display controller must take these zones into account.

#### How image display works

Screens usually rely on the same technique as the old cathode ray tubes (CRT), in which an electron beam swept a phosphorescent surface to "draw" the image. Thanks to the phosphorescence and the persistence of vision the image looked stable although the beam kept moving; it took about 20 ms to sweep the whole screen and draw one image or **frame**.

Flat panels have no electron beam, but the technique is the same: the screen is scanned by a pointer called the **dot clock**. It starts at the top-left corner, outside the visible area (in the back porches), and moves one pixel to the right on each clock edge; it is named after the clock signal that drives this movement and must be supplied to the screen. When it reaches the right edge, the **horizontal sync** signal, a negative pulse at the last pixel of the row, tells it to move to the next row. When it reaches the last pixel of the last row, the **vertical sync** signal, another negative pulse, tells it to go back to the first row and start a new frame.

In other words, the dot clock is a point guided from outside by three signals: a clock that advances it one pixel per edge, a horizontal sync that sends it to the start of the next row, and a vertical sync that sends it back to the start of the screen. Having to return quickly from right to left, or from bottom to top, is what justifies the porches, especially since the technique comes from CRTs, with an analogue-controlled beam.

In parallel there are three digital signals, **R**, **G** and **B**, with the intensity of each primary colour for each pixel. They must hold a valid value while the dot clock is in the visible area, and that value is the colour of the pixel it is on. RGB must therefore change **synchronously** with the dot clock, using the same clock.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/funcionamiento-de-la-visualizacion/Pantalla_ver13.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The animation emulates the scan: it shows how the dot clock moves and how the sync pulses are generated. It is much slower than reality (a real scan takes about 20 ms). The dot changes colour when it enters the visible area, to show that the RGB signals matter at that point, and at some point it takes a shortcut to the end to keep the animation short.

### LTM touchscreen

![[assets/control-pantalla/pantalla-tactil-ltm/imagen042.png]]

The LTM touchscreen, by Terasic, is designed for the Altera University Program boards such as the DE2-115 in the lab. It is a 4.3-inch screen with a 15:9 aspect ratio and a resolution of **800 × 480 pixels** at 24 bpp (up to 16 million colours). It also has an analogue-to-digital converter that captures the touch point.

#### Structure of the LTM touchscreen

![[assets/control-pantalla/estructura-pantalla-tactil-ltm/imagen043.png]]

Display and touch capture are completely independent, so this project only uses the display. The display part has a serial interface to adjust resolution, colour and so on, but the default values work, so it will not be used: the project focuses on the RGB data and sync signals.

#### Horizontal timing diagram

The figure shows the basic timing requirements for displaying each row.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen133.png]]

An active-low pulse of length **t_hpw** is the horizontal sync (**HD**), which marks the end of one line and the start of the next. After it, the RGB data are ignored during the *horizontal back porch* (**t_hbp**). Then comes the display time (**t_hd**), when the data are applied to the pixels of the row and the display enable (**DEN**) must be high. Finally, during the *horizontal front porch* (**t_hfp**) the data are ignored again, and a new HD pulse follows.

All signals are synchronous with clock **NCLK** and change on its rising edge. The screen is a passive device and uses this clock as its reference for the data and syncs.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen135.png]]

The table gives the values for 800 × 480 pixels. The manufacturer states an optimum clock of **33.2 MHz**, but up to **40 MHz** is allowed. **25 MHz** also gives a correct display, and it is the value used in this project.

#### Vertical timing diagram

The figure shows the timing requirements for each frame. The vertical sync is similar to the horizontal one, but its pulse means that a complete screen refresh has ended and the next begins, and the data now refer to all the rows.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen134.png]]

An active-low pulse of length **t_vpw** is the vertical sync (**VD**). After it, the data are ignored during the *vertical back porch* (**t_vbp**). Then comes the display time (**t_vd**), when data are applied only inside the visible area defined by the horizontal signals; during this time **DEN** is low in the horizontal back and front porches. Finally, during the *vertical front porch* (**t_vfp**) the data are ignored and a new VD pulse follows.

The signals in this diagram change when the line changes, because they correspond to the vertical movement of the pointer; that is why **HD** times their changes.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen136.png]]

The table values are given in units of one horizontal line (**H**): for example, the vertical back porch is 35 lines.

## Project structure

The project has six compulsory parts:

1. Synchronism signals.
2. Colour bars on the screen.
3. Black-and-white image on the screen.
4. Colour image on the screen.
5. Characters on the screen.
6. Text on the screen.

> [!note] Optional parts
> Parts 7 and 8 are optional extensions. They are not compulsory this year and do not count towards the mark; they are included for anyone who wants to build a complete application.

## Part 1: Synchronism signals

![[assets/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/imagen051.png]]

First you design the block that generates the data and sync signals, which will make it possible to display images. The screen's default configuration already displays at 800 × 480 pixels, so **you do not need to design the serial interface**: it would only be needed to change the resolution or other parameters.

Design the module that generates the syncs. As shown in the figure, it has:

- **Inputs:** clock **CLK** and asynchronous active-low reset **RST_n**.
- **Outputs:** horizontal (**HD**) and vertical (**VD**) sync, screen global reset (**GREST**), clock to the screen (**NCLK**), display enable (**DEN**), which indicates when the RGB data are valid, and two buses, **Fila** (row) and **Columna** (column), with the coordinates of the pixel being displayed.

### Representation using counters

The controller generates the horizontal and vertical syncs and the clock that guide the dot clock's scan. According to the manufacturer's timing diagrams, displaying an 800 × 480 image requires scanning **1056 × 525 positions**. The figure shows the coordinates of the corners and of the visible area.

![[assets/control-pantalla/representacion-con-cuentas/imagen05.png]]

The visible area goes from coordinate **(216, 35)** to **(1015, 514)**; the 800 × 480 pixels lie between them. In those ranges the **HDEN** and **VDEN** signals are active, indicating the display area.

### Proposed design structure

The following block diagram is a suggested starting point.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/propuesta-estructura-diseno/diagrama_bloques_ver20/Diagrama_bloques_ver20.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

- At the top left, a clock manager (a **PLL**) generates from the 50 MHz oscillator the **25 MHz** clock (**NCLK**) needed by the screen. The rest of the design runs on this clock.
- In the centre, a **modulo-1056** counter (**HCOUNT**) counts horizontal pixels, i.e. the column. It increments on each rising edge of NCLK and wraps to zero after 1055. Its terminal count **TC**, active when the count is 1055, is used to generate the horizontal sync.
- Below, a **modulo-525** counter (**VCOUNT**) counts rows. It increments every time HCOUNT reaches its terminal count, and its **TC** is used to generate the vertical sync.
- On the right, in yellow, the block that generates **DEN** from the row and column: it must be active in the visible area, from **(216, 35)** to **(1015, 514)**.
- Finally, two inverters give **HD** and **VD** the right polarity from the terminal counts of HCOUNT and VCOUNT.

> [!question]- How long does a frame take with a 25 MHz clock?
>> [!todo] 1056 × 525 cycles × 40 ns = 22.18 ms, about 45 frames per second.

### Using the *IP Catalog* to generate a PLL

Although the manufacturer sets NCLK at 33.2 MHz, the screen accepts up to 40 MHz and in particular 25 MHz, like a VGA screen. The best option is for **the whole design** to run at 25 MHz instead of the board's 50 MHz oscillator.

> [!question] How can you get 25 MHz from the 50 MHz oscillator while keeping a correct synchronous design?
> With one of the FPGA's internal **PLLs**, which generate a clock with a different frequency and phase from another clock.

The internal PLLs are generated and configured with the Quartus **IP Catalog**, a library of hardware blocks and synthesisable functions that can be included in your designs. One of them is **ALTPLL**, which creates a module with the right parameters to use the FPGA's PLLs. Its configuration windows set the PLL characteristics, and the tool generates the necessary files, including an instantiation template.

The **How to create a PLL** animation shows how to generate it and which options to set to obtain 25 MHz from 50 MHz. The starting point is the Quartus project of your design.

> [!warning] Watch the check boxes
> Pay attention to which options end up ticked. In particular, ***Create an 'areset' input to asynchronously reset the PLL*** and ***Create 'locked' output*** must be **unticked**.

If you choose the wrong parameters for an IP block such as ALTPLL, or want to change them, you can reopen its configuration windows by finding it in Quartus' *Project Navigator* subwindow (top left), under *IP Components* or, if you have already compiled, *Hierarchy*.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/ip_pll_ver11/IP_PLL_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

When the PLL is generated, the IP Catalog creates several files in the project directory, including **pll_ltm_inst.v**, with an instantiation example:

```verilog
pll_ltm pll_ltm_inst (
  .inclk0 ( inclk0_sig ),
  .c0     ( c0_sig )
);
```

### Design verification

Write a Verilog testbench that verifies the **LCD_SYNC** module: that the counters work and that the horizontal and vertical syncs are generated correctly. At the very least you must scan the screen once, about **22 ms** of simulated time; such a simulation takes about 3 minutes to run.

> [!warning] Do not use a fixed time to end the simulation
> Use conditions based on the signals generated by the module (HD, VD, Fila, Columna...).

Then check in the wave viewer, using the zoom tools (magnifying glasses), that the counters and syncs work, as in these figures:

**Simulation of one row:**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_1.png]]

**End of the one-row simulation (detail):**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_2.png]]

**Simulation of a complete screen scan:**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_3.png]]

**End of the complete scan (detail):**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_4.png]]

### Speeding up the simulation

As you have seen, this design takes a very long time to simulate. The reason is the PLL, whose low-level simulation model is very complex. Once you are sure that the block containing the PLL works, you can replace the PLL with a high-level model that speeds up the simulation, but **only for simulation**: for synthesis and the on-board test we still want the real PLL.

This is done with **compiler directives**, which let the compiler "see" or "ignore" blocks of code. The `` `ifdef `` directive followed by a label means that the following code is only considered if the label is defined; `` `else `` gives the alternative and `` `endif `` closes the block:

```verilog
`ifdef LABEL
  // Code block 1: used if LABEL is defined
`else
  // Code block 2: used otherwise
`endif
```

Labels are also defined with a directive: `` `define LABEL ``.

We will use the **`MODEL_TECH`** label, which ModelSim defines automatically when simulating but Quartus does not when compiling. Since the PLL divides the clock frequency exactly by 2, it can be emulated with a modulo-2 counter, i.e. a flip-flop that toggles on every cycle. Replace the PLL instance in **LCD_SYNC** with:

```verilog
`ifdef MODEL_TECH

// High-level model of the PLL as a flip-flop
reg nclk_sim;
assign NCLK = nclk_sim;

always @(posedge CLK or negedge RST_n)
  if (~RST_n)
    nclk_sim <= 0;
  else
    nclk_sim <= ~nclk_sim;

`else

// Instance of the real PLL
// (replace these lines with the ones you used to instantiate your PLL)
pll_ltm pll_ltm_inst (
  .inclk0(CLK),
  .c0(NCLK)
);

`endif
```

This way ModelSim only "sees" the flip-flop and Quartus only "sees" the PLL. Recompile and simulate: the design compiled by Quartus still contains a PLL, but the simulation now takes only a few seconds and gives the same results.

## Part 2: Colour bars on the screen

![[assets/control-pantalla/subtarea-3/imagen140.png]]

Once **LCD_SYNC** is designed, it must be tested on the board. You only need LCD_SYNC plus values for the RGB signals so that the colour bars in the image are displayed. The figure shows the block diagram. Since all bars have the same width and all rows are identical, the RGB value depends **only on the column**.

![[assets/control-pantalla/subtarea-3/imagen163.png]]

### Logical verification

Once **BARRAS_LCD** is designed, verify it with an RTL simulation in ModelSim. Checking it in the wave viewer is tedious, but there is a web tool that emulates the screen and builds the image from a text file. That file comes from a ModelSim simulation and contains on each line the simulation time and the values of **HD**, **VD**, **DEN**, **R**, **G** and **B**, in that order.

Here are the first lines of such a file for 24-bit RGB (8 bits per colour). Time is in picoseconds, although nanoseconds can also be used.

![[assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.11.png]]

To generate the `vga.txt` file, add these blocks to your testbench, adapted to your design. As in the previous part, the simulation must cover a complete frame (about 22 ms).

```verilog
integer fd;
event cierraFichero;
reg abierto;

initial
begin
  // Insert your simulation here (all test cases)
  // ...
  $display("Fin de la simulacion");
  -> cierraFichero;
  #10;
  $stop;
end

initial
begin
  fd = $fopen("vga.txt","w");
  abierto = 1;
  @(cierraFichero);
  disable guardaFichero;
  abierto = 0;
  $display("Cerrando fichero");
  $fclose(fd);
end

initial
forever
begin : guardaFichero
  @(posedge NCLK);
  if (abierto) $fwrite(fd,"%0t ps: %b %b %b %b %b %b\n",$time,HD,VD,DEN,R,G,B);
end
```

To check the result, use the **Screen Simulator** in the PoliformaT side bar. Select the `vga.txt` file, usually in the **simulation/modelsim** subfolder of the project, and click **Submit** to get the resulting image.

![[assets/control-pantalla/subtarea-3/screenshot.png]]

### Physical verification

Once the simulation is correct, test the design on the board with the following pin assignments:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.56.png]]

## Part 3: Black-and-white image on the screen

![[assets/control-pantalla/subtarea-3/imagen164d_2027.png]]

The goal is to display an image stored in an internal **ROM** of the FPGA. Starting from LCD_SYNC, build the design in the block diagram:

![[assets/control-pantalla/subtarea-3/imagen165bn.png]]

### Image memory

A memory block containing the image is added; each location holds the colour information of one pixel. It is an internal (*on-chip*) memory of the FPGA created with the Quartus **IP Catalog**; there is a guide below. Here you need a ROM.

A **ROM** is a set of cells holding previously stored data. To read a data word you just give the cell's address. It therefore has an input address bus, whose width depends on the number of cells, and an output data bus. The FPGA's internal memories are **synchronous**, so they need a clock.

### Addressing

Since each location corresponds to one pixel, the memory is read in the same order as the screen is scanned. The **Direccionamiento** (addressing) block generates the addresses from the row and column given by LCD_SYNC, and how it works depends on how the image is stored:

- **Continuous addressing.** Pixels are stored one after another, starting with the top-left pixel at address 0. For an **X × Y** image, row *r* starts at address *r* × X. You need a **k**-bit bus and a memory of at least X × Y locations. It uses memory optimally but complicates addressing, because Row and Column include the porches while the memory only holds the visible image.
- **X-Y addressing.** The pixels of each row are stored one after another, but each row takes **2ⁿ** locations, the smallest power of 2 **greater than or equal to** X. Row *r* starts at address *r* × 2ⁿ. For example, for 800 × 480 pixels the second row starts at 1024 and the third at 2048. Some locations are left unused, but the address is obtained simply by **concatenating** Y and X. The memory needed is about 2ⁿ × Y locations. As before, the back porch must be subtracted.

![[assets/control-pantalla/subtarea-3/imagen167.png]]

This video explains both addressing modes and how to compute the address of a point from its coordinates:

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/direccionamiento-xy.mp4"></video>

### Colour generation

Because of the FPGA's memory limits, the image has very low colour resolution: **1 bit per pixel**, white (1) or black (0). The screen uses 24-bit RGB, so the **Datos a RGB** (data to RGB) block converts the colour: it outputs the RGB value for white or black depending on whether the memory gives 1 or 0. You can use any other two colours if you like.

### Design task

Build the design to display an **800 × 480 pixel image with X-Y addressing and 1 colour bit**, stored in the file [[assets/control-pantalla/subtarea-3/imagen2027bn.hex|imagen2027bn.hex]].

> [!warning] Warnings
> - Copy the initialisation file (the HEX) to the Quartus project folder **before** generating the ROM.
> - Memory initialisation files are not always stored in the QAR by default. See [[sdp/en/qar-archive|Help: creating QAR files]] to add them manually (**Advanced... > Add...**).

Then verify the design with ModelSim and the screen emulator from the previous part, and test it on the board.

### Generating a ROM memory

The Quartus **IP Catalog** includes a generator of internal memory blocks of various sizes and types, including the ROM for this design. The ROM is initialised with the image data from a HEX or MIF (*Memory Initialization File*) file that must be in the project folder.

The **How to generate a ROM memory** animation shows how to create it and which options to set. The starting point is the Quartus project.

> [!danger] Warning
> 1. The data width and memory size in the animation **are not the right ones for this application**; they are only for illustration. Choose the values according to the image.
> 2. Pay attention to which options end up ticked. In particular, ***'q' output port*** must be **unticked**.
> 3. Copy the initialisation file to the project folder **before** generating the ROM.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-3/ip_rom_img_ver11/IP_ROM_Img_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

When the ROM is generated, the file **ROM_image_inst.v** is created, among others, with an instantiation example:

```verilog
ROM_image ROM_image_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

## Part 4: Colour image on the screen

![[assets/control-pantalla/subtarea-3/imagen164e_2027.png]]

The goal is to display a colour image. The FPGA's memory cannot hold an 800 × 480 image with enough bits per pixel, so a **400 × 240** image that does fit is used, and the previous design must be adapted to **replicate pixels** and double its size.

![[assets/control-pantalla/subtarea-3/imagen165.png]]

The block diagram is the same, but the three lower blocks change:

- The **Memoria** (memory) has different parameters (word width and number of words) and a different initialisation file, with the colour image.
- The **Direccionamiento** (addressing) block must duplicate each pixel horizontally and vertically, making each pair of consecutive rows and columns access the same memory location.
- **Datos a RGB** must convert the colour encoding, as explained below.

### Colour format

Whenever you work with images you must take colour encoding into account. As the figure shows, there are many options, from 1 bit (black and white) or 8 bits (greyscale) up to 30-bit RGB. Each pixel in memory may take between 1 and 30 bits and must be re-encoded to the screen's 24-bit RGB. To do so:

- If there are too many bits, drop the **least significant** ones.
- If there are too few bits, place the available bits in the **most significant** positions and replicate them in the following positions, from most to least significant, until the word is complete.
- To go from greyscale to colour, use the same value for all three colours.

![[assets/control-pantalla/subtarea-3/imagen166.png]]

### Design task

Build the design to display a **400 × 240 pixel image with X-Y addressing in 24-bit RGB**, stored in the file [[assets/control-pantalla/subtarea-3/imagen2027color.hex|imagen2027color.hex]]. The screen shows **800 × 480 pixels in 24-bit RGB**, so the addressing block must **replicate pixels to double the size of the image**.

Then verify the design with ModelSim and the screen emulator, and test it on the board.

## Part 5: Characters on the screen

![[assets/control-pantalla/subtarea-4/imagen139.png]]

The goal is to display characters, specifically to fill the screen with copies of a single character (for example A, B, C...). Since the screen is constantly refreshed, a memory holding the character images is needed. You will design a module that reads the character image from that memory according to the Row and Column from LCD_SYNC and drives the RGB signals to display it.

### Character memory

Another internal ROM is used. It stores the images of all characters, **8 × 8 pixels** each with 1 bit per pixel, which indicates whether the pixel is lit. Each character is identified by its 7-bit ASCII code ([ASCII table](https://www.asciitable.com/)), so it is a memory of **8192 one-bit cells** (128 characters × 8 × 8 pixels).

![[assets/control-pantalla/subtarea-4/imagen160b.png]]

The initialisation file contains the image of each character. The animation shows the structure of a MIF with those images: addresses in decimal and data in binary, to make it easier to read.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/mif_file/MIF_File.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The file [[assets/control-pantalla/subtarea-4/char_rom.mif|char_rom.mif]] is an example MIF with the character definitions; you can use it to see what each character looks like.

> [!warning] Do not use the MIF to initialise the memory
> It gives an error in simulation. Use the HEX file instead: [[assets/control-pantalla/subtarea-4/char_rom-1.hex|char_rom-1.hex]]. Create the ROM as in the previous part, with the parameters for this case (size, width and file), and **give it a different name** so you do not overwrite the one from Part 3.

> [!question]- How are the 13 address bits of the character ROM split?
>> [!todo] 8192 = 2¹³ cells = 128 characters × 8 rows × 8 columns: 7 bits for the ASCII code, 3 for the row and 3 for the column inside the character.

### Proposed design structure

The proposed block diagram has three blocks: **LCD_SYNC**, **SELEC_COLOR** and **CHAR_ROM**.

![[assets/control-pantalla/subtarea-4/imagen147c.png]]

- **LCD_SYNC** is the block from Part 1.
- **SELEC_COLOR** generates the RGB signals: it is a multiplexer that chooses between the background colour and the foreground (character) colour according to a signal from **CHAR_ROM** that tells whether the pixel is background or character.

![[assets/control-pantalla/subtarea-4/imagen149.png]]

- **CHAR_ROM** consists of the ROM and an addressing block (**Direccionamiento**), connected as in the diagram below. Addressing computes the address from Row and Column, and the upper part of the bus is the position of the character in memory, which matches its ASCII code. The memory outputs 1 bit: 0 for background and 1 for character.

![[assets/control-pantalla/subtarea-4/imagen148b.png]]

For now, connect a constant value to the **Caracter** input of CHAR_ROM, for example `7'h30` (the digit 0). At the end of this part you will change it so that the character can be modified from Quartus.

This interactive animation shows how CHAR_ROM and SELEC_COLOR work together:

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/funcionamiento_char_rom_ver30/Funcionamiento_Char_ROM_ver30.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

### Visual improvement of the design

When you test it on the board you will see that the letters are very small: **100 × 60 characters** fit on the screen, too many for such a small display. They can be enlarged by replicating pixels horizontally and vertically, changing only the **Direccionamiento** block.

Modify the design so that characters are twice as big, **16 × 16 pixels**. If they still look small, modify it again so that they are **32 × 32**.

### Physical verification using the Memory Content Editor

Once verified on the board, the character can be changed in real time with the Quartus ***In-System Memory Content Editor***, which lets you modify memories and constants of a running design if they are configured for it. To do so, replace the constant value on the **Caracter** input of CHAR_ROM with an **LPM_CONSTANT** block from the **IP Catalog**.

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/memory-content-editor-1.mp4"></video>

> [!warning] Deliverable
> Use this tool to change the character constant while the design is running and check that the screen updates. Include screenshots or photos of the test in your report.

## Part 6: Text on the screen

The goal is to display a text in the centre of the screen; as an example, the names of the members of your lab group.

![[assets/control-pantalla/subtarea-5/imagen142b.png]]

### Proposed design structure

Start from the previous design, but the character to display is no longer fixed: it depends on the screen position. The simplest approach is to store the text in another ROM addressed with Row and Column; success depends on correct addressing and on generating its initialisation file correctly.

The proposal is a **screen memory** for the text: the same idea as for the image, but with characters instead of pixels. The diagram shows a proposal:

![[assets/control-pantalla/subtarea-5/imagen173_mod.jpg]]

It starts from the version with 16 × 16 characters, so **50 × 30 characters** fit. You must add a memory (green) where each location contains the character to display. To keep it simple, use **X-Y addressing**: the horizontal position goes from 0 to 49 and the vertical one from 0 to 29.

With X-Y addressing the text memory has **1920 seven-bit words** (64 × 30). It is a ROM holding the text, so you must create a **MIF** initialisation file with the character codes at their positions. Since the memory is scanned continuously, **every location** must be initialised with the blank-space code, `0` or `7'h20`.

The file [[assets/control-pantalla/subtarea-5/text_rom_ejemplo.mif|text_rom_ejemplo.mif]] is an example with the names of two students on two lines; you can use it as a starting point.

> [!note] Delay register
> The diagram adds a register for the low bits of Row and Column, which delays them by one clock cycle. It is needed because the text ROM, accessed at the same time, is synchronous and has one cycle of latency. Without it, the fields of the character memory address would be out of step and the pixels on the left edge of each character would be displayed wrongly (try removing the register!).

### Physical verification using the Memory Content Editor

Once verified on the board, use the ***In-System Memory Content Editor*** to modify the contents of the text ROM in real time.

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/memory-content-editor-2.mp4"></video>

> [!warning] Deliverable
> Modify the text memory while the design is running and check that the text updates on the screen. Include screenshots or photos of the test in your report.

## Part 7 (optional): Combining image and text

![[assets/control-pantalla/subtarea_opcional.png]]

The goal is to combine the image display (Parts 3 and 4) with the text of Part 6 on top of it. In the figure, the course name has been written over the image.

**Combine the previous designs so that the names of the members of your group appear over the image.** You can use the colour image (Part 4) or the black-and-white one (Part 3).

![[assets/control-pantalla/subtarea-3/imagen164f_2027.png]]

## Part 8 (optional): Console with keyboard entry

![[assets/control-pantalla/subtarea_opcional.png]]

To finish, you implement a module that shows on the screen the keys pressed on a **PS/2 keyboard** connected to the board:

![[assets/control-pantalla/subtarea-7/imagen145_rotate.png]]

You do not need to design the keyboard controller: the instructors provide one in [[assets/control-pantalla/subtarea-7/keyboard_demo.qar|keyboard_demo.qar]]. The module outputs the code of the key being pressed, its ***scan code***, which is unique and standard for all keyboards.

Each scan code must be translated into the ASCII code of the character to display, which is then used to fetch its image. You must design the module that performs this decoding:

![[assets/control-pantalla/subtarea-7/imagen146b.png]]

For example, the "A" key has scan code `8'h1C`, which must be translated into ASCII code `7'h41`, the position of "A" in the character ROM.

You can start from the Part 6 design, replacing the text ROM with a **dual-port RAM**: one read port that works as before and one write port for the characters coming from the keyboard.

The keyboard connects to the FPGA with two signals generated by the keyboard, over which the PS/2 serial protocol runs: one for data and one clock to capture them. The table gives their pin assignments:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.31.png]]

next > [[sdp/en/project3-lights-fsm|Project 3: Design of an upgraded lighting effect]]
