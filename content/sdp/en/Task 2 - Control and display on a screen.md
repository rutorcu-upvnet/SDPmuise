---
title: "Task 2: Control and display on a screen"
draft: false
tags:
  - verilog
  - display
  - memories
---

prev > [[Task 1 - Design of sequential systems]]

*By Ricardo José Colom Palero*

This task lays the foundations for designing a **synchronism generator** that drives the display on a screen. Before tackling the proposed designs, study the information on this page.

<iframe src="/static/animaciones/Control%20Pantalla/Objetivos/objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Goals

The goal of this lab is to learn the characteristics and operating modes of a display screen, which is the application the design focuses on. First, you will develop and implement a control element that generates the synchronism signals needed to display images on a screen. To do this successfully you will go deeper into the Verilog HDL features used to design control elements. The **functional verification methodology** is very important in this lab. As complementary elements, you will also use ROM memories and a keyboard.

## Display on a screen

In painting, graphic design, photography, printing and television, colour theory is a set of basic rules for mixing colours to obtain a desired effect by combining lights or pigments. White light can be produced by combining red, green and blue light, while combining cyan, magenta and yellow pigments produces black.

An **additive** colour system emits light directly from some light source. Additive synthesis usually uses red, green and blue light to produce all other colours: combining the three primaries at equal intensity gives white, and varying the intensity of each one produces the whole spectrum.

![[assets/Control Pantalla/Visualizacion en una Pantalla/2000px-AdditiveColor.png]]

**RGB** is a colour model based on additive synthesis, which represents a colour as the sum of the three primary light colours: red, green and blue. All colours that can be created by mixing these three lights make up the colour spectrum; when no light is present we perceive black. Primary light colours are used in computer monitors, TVs, video projectors and, in general, any system that combines materials emitting in the red, green and blue ranges.

### Representation of images

Formally, an image is the spatial distribution of light irradiated on a plane. Mathematically it is a continuous function of two variables, the **x** and **y** coordinates of a point on the plane, that gives the light intensity at that point. To represent an image digitally, both coordinates and intensity must be discretised: a digital image is one whose coordinate and intensity values are finite and discrete. Each point of the plane with discrete coordinates is called a **pixel** (*picture element*). A digital image is thus a set of points forming a rectangular grid of **N** columns and **M** rows: an image of **N × M pixels**.

![[assets/Control Pantalla/Representacion Imagenes/Imagen01.png]]

> [!note] Notation
> In mathematics a matrix is described as rows × columns (here, **M × N**). For screens, however, the horizontal dimension, i.e. the number of columns, is always given first, which is why we say the image has **N × M** pixels.

A digital image is therefore a rectangular grid of N × M pixels that can be shown on a monitor, on paper or on another device. The first pixel is the one in the top-left corner, at coordinate **(0, 0)**.

Each pixel must hold colour information, in separate channels or sub-pixels that represent the primary components of the colour in the model being used, RGB or any other.

**Colour depth**, or bits per pixel (bpp), is the number of bits used to represent the colour of a pixel. With a depth of **n** bits each pixel can take **2ⁿ** values, i.e. represent **2ⁿ** different colours. Since the 8-bit byte is the almost universal basic unit of storage, colour depths are usually divisors or multiples of 8 (1, 2, 4, 8, 16, 24 and 32), except for a few such as 10 or 15 that are used by some graphics devices.

### Onscreen image

To show a digital image on a screen you must take its characteristics into account, mainly the size of the display area and the colour depth. The image size given by the manufacturer (horizontal dimension first, then vertical, in pixels) refers to the **display area**, i.e. how many pixels are visible.

Internally, however, the screen has a much larger area: around the visible region there are "**black**" zones (grey in the image) that enlarge the working area of the control electronics. These zones are used to let the synchronism signals settle and have their own names: *Horizontal Back Porch* and *Horizontal Front Porch* to the left and right of the visible area, and *Vertical Back Porch* and *Vertical Front Porch* above and below it.

![[assets/Control Pantalla/Visualizacion en Pantalla/Imagen02.png]]

These zones are not symmetrical: the back porches are larger than the front porches, because the synchronism signals need more settling time before display.

When designing a display controller you must therefore account for these "black" zones around the display area.

### How image display works

Screens usually rely on the same technique as the old cathode ray tubes (CRT): an electron beam swept a phosphorescent surface to "draw" the image. Thanks to the phosphorescence and the persistence of human vision the image looked stable, although the beam was constantly moving. The beam took about 20 ms to sweep the whole screen and draw one image, or *frame*.

Flat panels have no electron beam and display a matrix of pixels, but the technique is the same: the screen is scanned by a pointer called the ***dot clock***. The dot clock starts at the top-left corner, outside the visible area (in the porches), and moves right one pixel on each clock edge; since this movement is driven by a clock signal that must be supplied to the screen, it is called the dot clock. When it reaches the right edge it must be told that the row is finished and that it must go to the start of the next row. This is done with the **horizontal sync** signal: a negative pulse when the dot clock is at the last pixel of the row.

When the dot clock reaches the last pixel of the last row, it must be told that the whole screen has been scanned and that it must go back to the first row. This is the job of the **vertical sync** signal: a negative pulse that marks the start of a new image or frame.

In other words, the dot clock is a point that is guided externally across the screen by three signals: a clock that advances it one pixel per edge, a horizontal sync that sends it to the start of the next row, and a vertical sync that sends it back to the start of the screen.

The fact that the dot clock must quickly return from right to left to start a new row, or from bottom to top for a new image, is what justifies the porches around the visible area, especially considering that the technique comes from CRTs, where the beam was controlled analogically.

In parallel there are three digital signals, **RGB**, that carry the intensity of each primary colour for each pixel. They must hold a valid value while the dot clock is inside the visible area, and that value is the colour of the pixel the dot clock is on. The RGB signals must therefore change **synchronously** with the movement of the dot clock, i.e. with the same clock that moves it.

<iframe src="/static/animaciones/Control%20Pantalla/Funcionamiento%20de%20la%20Visualizacion/Pantalla_ver13.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The animation emulates the screen scan: it shows how the dot clock moves and how the horizontal and vertical sync pulses are generated. It is, of course, much slower than reality so that you can see the dot, since a stable image requires the dot to scan the whole screen in about 20 ms.

Note two details: the dot changes colour when it enters the visible area, to show that the RGB signals are in use at that moment, and, to keep the animation short, at some point the dot takes a shortcut to the end of the screen.

## LTM touchscreen

![[assets/Control Pantalla/Pantalla Tactil LTM/Imagen042.png]]

This lab uses the LTM touchscreen made by Terasic for the Altera University Program boards such as the DE2-115. It is a 4.3-inch screen with a 15:9 aspect ratio and a resolution of **800 × 480 pixels** at 24 bpp, able to show about 16 million colours. It also has an analogue-to-digital converter that captures the touch point.

### Structure of the LTM touchscreen

![[assets/Control Pantalla/Estructura Pantalla Tactil LTM/Imagen043.png]]

In this screen, display and touch capture are completely independent, so the display can be used on its own, as in this lab. The display part also has a serial interface to adjust its configuration (resolution, colour settings...), but the default values work, so it will not be used. The lab focuses on the RGB data and synchronism signals.

### Horizontal timing diagram

The figure shows the basic timing requirements for displaying each row of the screen.

![[assets/Control Pantalla/Diagrama Temporización Horizontal/Imagen133.png]]

An active-low pulse of fixed length (**thpw**) is the horizontal sync signal (**HD**), which marks the end of one line and the start of the next. After the pulse, the RGB data are still invalid during the horizontal back porch (**thbp**). Then comes the display time (**thd**), when the data are applied to the pixels as the row is scanned; during this time the display enable signal (**DEN**) must be high. Finally there is the horizontal front porch (**thfp**), when the data are invalid again, after which a new horizontal sync pulse follows.

All signals are synchronous with a clock called **NCLK** and change on its rising edge. The screen is a passive device: the clock is its reference for timing the RGB data and the sync signals.

![[assets/Control Pantalla/Diagrama Temporización Horizontal/Imagen135.png]]

The table gives the horizontal timing values for 800 × 480 pixels. The manufacturer states that the optimum clock frequency is **33.2 MHz**, although other frequencies up to a maximum of **40 MHz** can be used. In particular, **25 MHz** also gives a correct display.

### Vertical timing diagram

The figure shows the basic timing requirements for each frame. The vertical sync (**VD**) is similar to the horizontal one, except that a VD pulse means that a frame (a complete screen refresh) has ended and the next one begins; the data now refer to all the rows in the frame.

![[assets/Control Pantalla/Diagrama Temporización Vertical/Imagen134.png]]

An active-low pulse of fixed length (**tvpw**) is the vertical sync signal (**VD**), which marks the end of one frame and the start of the next. After the pulse, the RGB data are invalid during the vertical back porch (**tvbp**). Then comes the display time (**tvd**), when the data are applied to the pixels, but only inside the visible area defined by the horizontal signals; during this time **DEN** toggles and is inactive (low) during the horizontal back and front porches. Finally there is the vertical front porch (**tvfp**), with invalid data, after which a new VD pulse follows.

The signals in this diagram change when the line changes, because they correspond to the vertical movement of the pointer: the horizontal sync (**HD**) is what times their changes.

![[assets/Control Pantalla/Diagrama Temporización Vertical/Imagen136.png]]

The table gives the vertical timing values for 800 × 480 pixels. They are expressed in units of one horizontal line time (**H**): for example, the vertical back porch is 35 lines.

## Structure of the task

<iframe src="/static/animaciones/Control%20Pantalla/Estructura%20de%20la%20Tarea/indice.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The lab consists of designing a system that controls and displays images on a screen. A touchscreen has been chosen, which can report the coordinates of the touch point, but this lab only deals with the display.

The lab is divided into **seven sub-tasks**. The first one is the design of the synchronism generator; from there the complexity grows (colours, bars, images, characters) until you write on the screen the characters typed on a PS/2 keyboard connected to the board.

## Sub-task 1: Generating the synchronism signals

![[assets/Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/Imagen051.png]]

First you design the block that generates the data and synchronism signals for the screen, which will make it possible to display images. The screen's default configuration already displays at 800 × 480 pixels, so **you do not need to design the serial interface**: it is only needed to change the resolution or other parameters.

Design the module that generates the synchronism signals. As shown in the figure, it has:

- **Inputs:** clock **CLK** and active-low reset **RST_n**.
- **Outputs:** horizontal (**HD**) and vertical (**VD**) sync, screen global reset (**GREST**), clock to the screen (**NCLK**), display enable (**DEN**), which indicates when the RGB data are valid, and two buses, **Fila** (row) and **Columna** (column), with the coordinates of the pixel being displayed at each moment.

### Representation using counters

The controller basically generates the horizontal and vertical syncs and the clock that guide the scan of the dot clock. To do so you must follow the manufacturer's timing diagrams, from which it follows that displaying an 800 × 480 image requires scanning **1056 × 525 positions**. The figure shows the coordinates of the corners of the scan and the positions of the visible area.

![[assets/Control Pantalla/Representación con Cuentas/Imagen05.png]]

The visible area starts at coordinate **(216, 35)** and ends at **(1015, 514)**; the 800 × 480 pixels lie between them. In these ranges the **HDEN** and **VDEN** signals are active, indicating that the pointer is inside the display area.

### Proposed design structure

The block diagram in the image is a suggested starting point.

<iframe src="/static/animaciones/Control%20Pantalla/Propuesta%20Estructura%20Dise%C3%B1o/Diagrama_bloques_ver20.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

- At the top left there is a clock manager or **PLL**, which generates from the external 50 MHz oscillator the **25 MHz** clock needed by the screen (**NCLK**). The rest of the design must run on this 25 MHz clock.
- In the centre is the **modulo-1056** counter (**HCOUNT**), which counts horizontal pixels, i.e. the column. It increments on each rising edge of the 25 MHz clock and wraps to zero after 1055. Its terminal count output **TC** goes active when the count is 1055 and is also used to generate the horizontal sync.
- Below it is the **modulo-525** counter (**VCOUNT**), which counts rows. It increments every time HCOUNT reaches its terminal count. Its **TC** is used to generate the vertical sync.
- On the right, in yellow, is the **DEN** generator, which uses the row and column from HCOUNT and VCOUNT to activate DEN in the visible area, from **(216, 35)** to **(1015, 514)**.
- Finally, two inverters produce **HD** and **VD** from the terminal counts of HCOUNT and VCOUNT.

> [!question]- How long does a frame take with a 25 MHz clock?
>> [!todo] 1056 × 525 cycles × 40 ns = 22.18 ms, i.e. about 45 frames per second.

### Using the IP Catalog to create a PLL

Although the manufacturer sets NCLK at 33.2 MHz, the screen accepts frequencies up to 40 MHz, so 25 MHz is perfectly valid, as in VGA. The most suitable option is for **the whole design** to run on a 25 MHz clock instead of the 50 MHz oscillator on the board.

> [!question] How can you get 25 MHz from the 50 MHz oscillator while keeping a correct synchronous design?
> With one of the FPGA's internal **PLLs**, which generate a clock with a different frequency and phase from another clock.

The internal PLLs are generated and configured with the Quartus **IP Catalog** tool (formerly *MegaWizard Plug-In Manager*), a library of hardware blocks and synthesisable functions. One of them is **ALTPLL**, which creates a module with the right parameters to use the FPGA's PLLs. Its configuration windows set the PLL characteristics, and the tool generates the necessary files, including a template to instantiate it in your design.

The **How to create a PLL** animation shows step by step which parameters and options to set to obtain a 25 MHz clock from a 50 MHz one. The starting point is the Quartus project containing your design.

<iframe src="/static/animaciones/Control%20Pantalla/Subtarea%201%3A%20Generaci%C3%B3n%20de%20las%20se%C3%B1ales%20de%20sincronismo/IP_PLL_ver11/IP_PLL_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

When the PLL is generated, the IP Catalog creates several files in the project directory, including **pll_ltm_inst.v**, with an instantiation example:

```verilog
pll_ltm pll_ltm_inst (
  .inclk0 ( inclk0_sig ),
  .c0     ( c0_sig )
);
```

### Design verification

![[assets/Control Pantalla/Verificación del Diseño/Imagen061.png]]

Once the **LCD_SYNC** module has been described, verify by simulation that the counters work and that the horizontal and vertical syncs are generated according to the specifications. At the very least the simulation must cover one full screen scan, which means about **22 ms** of simulated time.

Write a Verilog HDL testbench that uses ***tasks*** and the Row and Column values and/or the sync signals to stop the simulation. You can first stop it after the first row and then simulate a full screen scan.

> [!warning] Do not use time to stop the simulation
> The simulation must stop based on the state of the design (row, column, syncs), not after a fixed delay.

Then check the behaviour in the wave viewer, using the zoom tools (magnifying glasses) to verify the counters and the syncs.

**Simulation of one row:**

![[assets/Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.17-1.png]]

**End of the one-row simulation (detail):**

![[assets/Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.48-1.png]]

**Simulation of a complete screen scan:**

![[assets/Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.16.01.png]]

**End of the complete scan (detail):**

![[assets/Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.17.47.png]]

## Sub-task 2: Colour bars on the screen

![[assets/Control Pantalla/Subtarea 3/Imagen140.png]]

Once **LCD_SYNC** is designed, it must be tested on the DE2-115 board. To do this you only need LCD_SYNC plus values for the colour signals (RGB) so that the screen shows the colour bars in the image above. The figure shows the block diagram. Since all bars have the same width, the RGB value depends **only on the column** produced by LCD_SYNC.

![[assets/Control Pantalla/Subtarea 3/Imagen163.png]]

Once the **BARRAS_LCD** module is designed, verify it with an RTL simulation in ModelSim. Checking the result in the wave viewer can be very tedious, but there is a web tool that emulates the screen and builds the image from a text file and the screen parameters. That file is produced by a ModelSim simulation and contains on each line the simulation time and the values of **HD, VD, DEN, R, G and B** at that instant.

Here are the first lines of such a file for 24-bit RGB (8 bits per colour). Time is given in picoseconds, although nanoseconds can also be used.

![[assets/Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.11.png]]

To get the file, simulate the design in ModelSim with a testbench, as in previous sessions, and add the following procedural blocks (adapted to your design). This generates the file `vga.txt` with the results in the right format. The simulation must last long enough for a complete frame, about **22 ms**.

![[assets/Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.33.png]]

To check the result, use the [Screen Simulator](https://is.gd/JtLbap), also linked in the PoliformaT side bar. Select the file `vga.txt`, click **Iniciar** (start) and you will get the resulting image:

![[assets/Control Pantalla/Subtarea 3/Captura de Pantalla 2022-09-21 a las 12.12.26.png]]

Once the simulation is correct, test the design on the DE2-115 board with the following pin assignments:

![[assets/Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.56.png]]

## Sub-task 3: Displaying an image on the screen

![[assets/Control Pantalla/Subtarea 3/Imagen164b.png]]

In this sub-task you display an image stored in an internal **ROM** of the Cyclone IV. Starting from the LCD_SYNC module, build the design in the block diagram:

![[assets/Control Pantalla/Subtarea 3/Imagen165.png]]

A memory holding the image is added. Each location stores the colour of one pixel, so the memory must be addressed sequentially, in the same order as the screen is scanned.

The **Direccionamiento** (addressing) block generates memory addresses from the row and column given by **LCD_SYNC**. How it works depends on the addressing mode used to store the image:

- **Continuous addressing.** Pixels are stored consecutively, starting with the top-left pixel at address 0 and following the scan to the right until the row is complete, then continuing with the next row. For an image of **X × Y** pixels you need a **k**-bit address bus and a memory of at least **X × Y** locations. This mode uses memory optimally but complicates addressing, because Row and Column include the porches while the memory only holds the visible image.
- **X-Y addressing.** The pixels of each row are stored consecutively, but each row starts at a multiple of a power of two: the first at address 0 and the second at **2ⁿ**, the smallest power of 2 **greater than or equal to** **X**. For example, for a 400 × 240 image the first row starts at address 0, the second at 512, the third at 1024, and so on. Some locations between rows are left unused, but the address is obtained simply by **concatenating** Y and X. The memory needed is about **2ⁿ × Y** locations. As before, the back porch must be subtracted when computing the address from Row and Column.

![[assets/Control Pantalla/Subtarea 3/Imagen167.png]]

Another aspect is **colour encoding**. As shown in the image, there are many options: from black and white with 1 bit or 8-bit greyscale up to 30-bit RGB. Each pixel in memory may take from 1 to 30 bits and must be re-encoded to the 24-bit RGB format used by the screen; hence the **Datos a RGB** (data to RGB) block. When re-encoding:

- If there are too many bits, drop the **least significant** ones.
- If there are too few bits, place the available bits in the **most significant** positions and replicate them in the lower positions, from most to least significant, until the word is complete.
- To go from greyscale to colour, use the same value for all three colours.

![[assets/Control Pantalla/Subtarea 3/Imagen166.png]]

Build the design to display a **400 × 240 pixel image in 16-bit RGB with X-Y addressing**, stored in the file [[assets/Control Pantalla/Subtarea 3/imagen_rgb16_xy.hex|imagen_rgb16_xy.hex]]. The screen shows **800 × 480 pixels in 24-bit RGB**, so besides re-encoding the colour, the addressing block must **replicate pixels** to double the size of the image.

> [!tip] 16-bit RGB
> The usual format is RGB565: 5 bits of red, 6 of green and 5 of blue. Apply the re-encoding rules above to each component.

Verify the design by simulation with ModelSim and the screen emulator from the previous sub-task, then test it on the DE2-115 board.

### Creating a ROM memory

The memory is an internal block of the FPGA, created with the Quartus **IP Catalog** (formerly *MegaWizard Plug-In Manager*). Its memory compiler generates several types of memory, including the ROM needed here.

The ROM stores the image and must be initialised with the provided file, which can be HEX (hexadecimal data) or MIF (*Memory Initialization File*) and must be placed in the project folder.

The **How to generate a ROM memory** animation shows how to generate the ROM and which options to set. The starting point is the Quartus project.

> [!danger] Warning
> The data width and memory size shown in the animation **are not the right ones for this application**; they are for illustration only. Choose the right values according to the characteristics of the provided image.

<iframe src="/static/animaciones/Control%20Pantalla/Subtarea%203/IP_ROM_Img_ver11/IP_ROM_Img_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

When the ROM is generated, several files are created in the project directory, including **ROM_image_inst.v**, with an instantiation example:

```verilog
ROM_image ROM_image_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

## Sub-task 4: Displaying characters on the screen

![[assets/Control Pantalla/Subtarea 4/Imagen139.png]]

The goal is to display characters, specifically to fill the whole screen with identical or different characters. This representation was chosen because it is much easier to implement and to check: the position on the screen does not matter, you only need to generate the RGB signals.

Since the screen is constantly refreshed, a memory is needed to hold the characters (for example 0, A, B...). You will design a module that reads each character from memory and drives the RGB signals according to the Row and Column from LCD_SYNC to display it.

The memory is internal to the FPGA (*on-chip*) and is created with the Quartus **IP Catalog**, as in the previous sub-task.

A **ROM** is a set of cells holding previously stored data of a given size. To read a data word you just give the address of the cell and the memory outputs its contents. It therefore has an address bus, whose width depends on the number of cells, and a data bus. The FPGA's internal memories are **synchronous**, so they need a clock signal.

![[assets/Control Pantalla/Subtarea 4/Imagen160b.png]]

The memory stores the characters, each **8 × 8 pixels**, with one bit per pixel indicating whether it is on or off. Its contents are initialised with a MIF or Intel-HEX file that sets the value of each cell and can be written in binary, hexadecimal, decimal or octal. The image shows the structure of the MIF for this sub-task: a memory of **8192 one-bit cells**, with addresses in decimal and data in binary to make it easier to read.

<iframe src="/static/animaciones/Control%20Pantalla/Subtarea%204/MIF_File.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The file [[assets/Control Pantalla/Subtarea 4/char_rom-1.mif|char_rom-1.mif]] is an example of what a MIF with the character definitions looks like.

> [!warning] Do not use this MIF to create the memory
> It gives an error in simulation. Use instead the HEX file from the *Using the IP Catalog to create a ROM* section.

> [!question]- How are the 13 address bits of the character ROM split?
>> [!todo] 8192 = 2¹³ cells = 128 characters × 8 rows × 8 columns: 7 bits for the character code, 3 for the row and 3 for the column inside the character.

### Proposed design structure

The block diagram in the image is a suggested structure with three blocks: **LCD_SYNC**, **SELEC_COLOR** and **CHAR_ROM**.

![[assets/Control Pantalla/Subtarea 4/Imagen147c.png]]

- **LCD_SYNC** is the block from sub-task 1, which generates the syncs.
- **SELEC_COLOR** generates the RGB signals: it is a multiplexer that chooses between the background colour and the foreground (character) colour, according to a signal from **CHAR_ROM** that tells whether the pixel belongs to the background or to a character.

![[assets/Control Pantalla/Subtarea 4/Imagen149.png]]

- **CHAR_ROM** consists of the ROM and an addressing block (**Direccionamiento**), connected as in the diagram below. Addressing works as in the previous sub-task: it computes the address from Row and Column. The upper part of the address bus is the position of the character in the memory, which matches its ASCII code. The memory then outputs 1 bit, the pixel at that row and column of the character: 0 for background and 1 for character.

![[assets/Control Pantalla/Subtarea 4/Imagen148b.png]]

The following interactive animation illustrates how CHAR_ROM and SELEC_COLOR work together:

<iframe src="/static/animaciones/Control%20Pantalla/Subtarea%204/Funcionamiento_Char_ROM_ver30.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

### Using the IP Catalog to create a ROM

The memory stores 8 × 8 pixel characters and is initialised with the provided HEX file, [[assets/Control Pantalla/Subtarea 4/char_rom.hex|char_rom.hex]], which defines a memory of **8192 one-bit cells**.

The **How to generate a ROM memory** animation shows which parameters, options and settings to use to instantiate the memory for this design. The starting point is the Quartus project.

<iframe src="/static/animaciones/Control%20Pantalla/Subtarea%204/IP_ROM_Char_ver11/IP_ROM_Char_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

When the ROM is generated, the file **ROM_char_inst.v** is created, among others, with an instantiation example:

```verilog
ROM_char ROM_char_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

### Visual improvement of the design

When you test the design on the board you will see that the letters are very small: **100 × 60 characters** fit on the screen, too many for such a small display.

One improvement is to **enlarge** the characters by replicating their pixels horizontally and vertically. It is a simple change that only requires modifying two lines of the **Direccionamiento** block.

Make the necessary changes so that the characters are twice as big, **16 × 16 pixels**, and easier to read.

## Sub-task 5: A message on the screen

The goal is to display the names of the members of your lab group on one line, roughly centred. You can start from the previous design, with the difference that the character to display is no longer fixed but depends on the screen position, again controlled by the row and column counters.

An important suggestion is to store the message in **another ROM**, whose contents are the addresses of the characters in CHAR_ROM and which is addressed with the row and column. Success in this exercise depends on correct addressing and on generating the MIF initialisation file correctly.

![[assets/Control Pantalla/Subtarea 5/Imagen142b.png]]

The best option is to implement a **screen memory** for the text: the same idea as for displaying an image, but with characters instead of pixels. A memory that provides the character to display at each moment is added to the previous design. The diagram shows a proposal:

![[assets/Control Pantalla/Subtarea 5/Imagen173.png]]

It starts from the version with 16 × 16 pixel characters, so **50 × 30 characters** fit on the screen. You must add a memory (green in the diagram) able to hold all of them, where each location contains the character to display. To keep it simple, use **X-Y addressing**, obtained from Column and Row by the addressing block. The position of a character is given by a horizontal coordinate between 0 and 49 and a vertical coordinate between 0 and 29.

With X-Y addressing the text memory needs **1920 seven-bit words** (64 × 30). It is a ROM holding the message, so you must create a **MIF** initialisation file with the character codes at their positions. Since the memory is scanned continuously, **every location** must be initialised with the code of the blank space, which here is either 0 or 0x20.

The file [[assets/Control Pantalla/Subtarea 5/text_rom_ejemplo.mif|text_rom_ejemplo.mif]] is an example MIF for the text memory with the names of two students on two lines. You can use it as a starting point.

Once the design has been verified on the board, you can change the text in real time with the Quartus ***In-System Memory Content Editor***, which gives access to the ROM so you can modify its contents while the design is running.

<!-- PoliformaT: In-System Memory Content Editor video (not exported) -->

> [!tip] Enable access in the ROM
> For the *In-System Memory Content Editor* to see the memory, tick *Allow In-System Memory Content Editor to capture and update content independently of the system clock* when you create it in the IP Catalog, and give it an instance ID.

> [!warning] Deliverable
> Use this tool to modify the text memory while the design is running and check that the text updates on the screen. Include screenshots and/or photos of the test in your report.

## Sub-task 6: Image and text on the screen

This sub-task combines the image display (sub-task 3) with text written on top of it (previous sub-task). In the figure, the text "Palau de les Arts" has been written over the image.

![[assets/Control Pantalla/Subtarea 6/Imagen174.png]]

## Sub-task 7: Typing on a keyboard, displaying on screen

![[assets/Control Pantalla/Subtarea_Opcional.png]]

After controlling the display and drawing characters at given positions, the goal is a module that shows on the screen the keys pressed on a **PS/2 keyboard** connected to the DE2-115 board:

![[assets/Control Pantalla/Subtarea 7/Imagen145_rotate.png]]

So that you do not need to design the keyboard controller, the instructors provide one: [[assets/Control Pantalla/Subtarea 7/visualiza.qar|visualiza.qar]]. The module outputs the code of the key being pressed, its ***scan code***, which is unique and standard for all keyboards.

The scan code must be converted into a code that selects the right character in the character ROM. You must design the module that performs this decoding:

![[assets/Control Pantalla/Subtarea 7/Imagen146.png]]

For example, pressing the "A" key produces scan code **0x1C**. The module must translate it into the code of the letter A in the CHAR_ROM MIF, i.e. address **0x41**.

You can start from the sub-task 5 design, replacing the text ROM with a **dual-port RAM**: one read port that works as before and one write port where the characters from the keyboard are written.

The keyboard is connected to the FPGA with two signals of a serial link: one for data and one clock to capture them. The table gives their pin assignments:

![[assets/Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.31.png]]

next > [[Task 3 - Upgraded lighting effect with FSMs]]
