---
title: "Task 1: Design of sequential systems"
draft: false
tags:
  - verilog
  - sequential
---

prev > [[sdp/en/qar-archive|Creating a QAR archive]]

*By Ricardo José Colom Palero*

This task lays the foundations for the first lab of the course, which deals with the design of sequential digital systems using a hardware description language, namely **Verilog HDL**.

> [!warning] Preliminary test
> Before starting the task, take the Verilog HDL syntax test in PoliformaT, which assesses your previous knowledge.

<iframe src="../../static/animaciones/secuenciales/objetivos/Objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Goals

The main goal of this task is to learn the basic concepts of Verilog HDL and how to use it to build designs, with particular emphasis on clocked procedural blocks for modelling sequential circuits.

You will design digital elements in Verilog HDL, making progress in the use of hierarchy and parameters. Finally, special attention is paid to verifying the designs through simulations that thoroughly check that they work correctly.

## Structure of the task

<iframe src="../../static/animaciones/secuenciales/estrutura_tarea/Estructura_Tarea.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Every sequential system is driven by a clock signal coming from an oscillator outside the device where the design is implemented. The oscillator on the DE2-115 board runs at **50 MHz**, i.e. a period of **20 ns**. When designing circuits that drive display elements, bear in mind that the human eye cannot perceive changes that last less than about 50 ms. Therefore, the 50 MHz clock cannot be used directly to produce changes that must be visible, such as making an LED blink.

This lab shows how to solve this problem while keeping the rules of correct synchronous design: **all flip-flops in the design must be driven by the same clock signal**.

The lab is divided into three subtasks:

1. Design of a parameterisable counter.
2. Design of a shift register.
3. Integration of the previous designs to build the Knight Rider light effect.

## Subtask 1: Design of a parameterisable counter

![[assets/secuenciales/estrutura_tarea/imagen02.png]]

Describe in Verilog HDL a binary counter with the following specifications:

- Synchronous up/down counter with parameterisable modulus `fin_cuenta` (*end count*).
- Operates on the rising edge of the clock.
- Synchronous reset (highest priority), active low.
- Active-high **enable** input that enables counting.
- If the **UP_DOWN** input is high the counter counts up; otherwise it counts down.
- **TC** (*Terminal Count*) output, active when the counter reaches the end of the count.
- Intel FPGA Cyclone IV E device.

Verify its operation with a simulation that covers every possible combination of the input signals and sweeps through all values of the outputs.

### Parameterisation

An efficient designer makes the most of design time, and reusing previously designed modules is key to that. One feature of HDLs that makes reuse easier is **parameterisation**. For example, if we already have an 8-bit counter and need a 10-bit one, the obvious solution is to copy the description and modify it, but we end up with a collection of different files for each size.

The best solution is to have **a single file** with the counter model, written in terms of a configuration parameter that is changed as needed.

Sometimes the parameter must go through some arithmetic before it can be used. For example, how do you get the number of bits of the counter from its modulus? The answer is to use a function. The figure shows how to do it with the `CLogB2` function, which computes the base-2 logarithm **rounded up to the next integer**, i.e. the number of bits needed to reach the end count. `CLogB2` is defined in the maths functions file [[assets/secuenciales/estrutura_tarea/mathfun.vh|MathFun.vh]], which must be included in the design.

![[assets/secuenciales/estrutura_tarea/imagen08.png]]

### Design verification

![[assets/control-pantalla/verificacion-del-diseno/imagen061.png]]

Once the `count` module has been described in Verilog HDL, you must verify by simulation that the counter works correctly and produces both the count value and the terminal count signal properly.

For this we use a professional simulator, **ModelSim-Altera**, which needs a **testbench**: a file, also written in Verilog HDL, that describes the input stimuli for the simulation. Since you do not yet have experience writing testbenches, follow the steps below.

#### Check the Quartus configuration

Before simulating, check that the ModelSim-Altera installation path is correctly set in Quartus. In **Tools > Options…**, select **General > EDA Tool Options** in the **Category** column. In the list of tools, the ModelSim-Altera path must be `C:\intelFPGA\17.1\modelsim_ase\win32aloem` or equivalent.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2019-12-16-a-las-17.25.53.png]]

#### Writing the stimuli in Verilog HDL

Simulation stimuli are described in Verilog HDL itself. In **File > New**, select **Verilog HDL File** and type the code below.

Since this is verification code, its job is to generate stimuli; that is why the `module` has no inputs or outputs: it generates the inputs internally and drives them into the block under verification, the DUT (*Device Under Test*). Here the DUT is the `count` module, which is instantiated inside the testbench to connect the generated inputs and collect its outputs.

```verilog
// Author: Ricardo José Colom Palero
// Date: 10 December 2018

`timescale 1ns/1ps

module tb_count ();

localparam T = 20;

reg CLK, RST_n;
reg ENABLE, UP_DOWN;
wire [4:0] COUNT;
wire TC;

// DUT (Device Under Test) instantiation
count #(.fin_cuenta(20)) i1 ( .iCLK(CLK),
                              .iRST_n(RST_n),
                              .iENABLE(ENABLE),
                              .iUP_DOWN(UP_DOWN),
                              .oCOUNT(COUNT),
                              .oTC(TC));

initial
begin
  RST_n = 1'b0;
  CLK = 1'b0;
  ENABLE = 1'b0;
  UP_DOWN = 1'b0;
  $display("SIMULATING!!!");
  #(T*2)
  RST_n = 1'b1;
  #(T*2)
  ENABLE = 1'b1;
  UP_DOWN = 1'b1;
  #(T*24)
  $display("End of simulation!!!");
  $stop;
end

always
begin
  #(T/2) CLK <= ~CLK;
end

endmodule
```

Save it with **File > Save as...** as `tb_count.v`. This file **must not be compiled** with the rest of the project: it is not part of the design that is configured into the FPGA and is only used for verification.

Next, configure the simulation so that it finds the stimulus file. In **Assignments > Settings**, select **Simulation** in the left column:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.02.png]]

Click the **Test Benches...** button, halfway down on the right-hand side. A new window opens...

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.11.png]]

...where you click **New** to add a new testbench, configured as in the image:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.28.34.png]]

Go back by clicking **OK** in each window.

All that remains is to launch the ModelSim-Altera simulation with **Tools > Run Simulation Tool > RTL Simulation**, which simulates the RTL code before synthesis and implementation.

![[assets/control-pantalla/realizar-la-simulacion/imagen116.png]]

ModelSim-Altera opens and runs the simulation described in the testbench. Here it stops at the `$stop`, about 24 clock cycles after counting is enabled, so you can see the counter go from 0 up to 19 and back to 0.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.33.02.png]]

> [!warning] Always check the *Transcript* window
> ModelSim also reports errors when the testbench does not compile. Always check the *Transcript* window at the bottom for errors and warnings. In the screenshot below, for example, the error comes from a typo in the name of the counter module.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-26-ene.png]]

#### The ModelSim-Altera simulator

ModelSim-Altera has several windows. At the bottom is the message window, where the simulator reports, for instance, errors found in the design's Verilog HDL files. Keep an eye on it: an error in the files prevents the project from loading and therefore from being simulated.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_general.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

On the left is the hierarchy viewer, which shows the structure of the design and all its files. In the upper centre is the signal viewer, with the signals of the module selected in the hierarchy. These signals can be added to the wave viewer on the right, which shows the simulation result. Every ModelSim window can be undocked and displayed on its own, which is especially handy for the wave viewer.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_desacoplo.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The magnifying glasses in the top menu let you zoom into the results.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.09.20.png]]

Initially ModelSim-Altera simulates until it reaches the `$stop` in the testbench. All signals are displayed and the counter value is shown in binary.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.39.47.png]]

You can change how a signal is displayed: for example, to see the counter in unsigned decimal, right-click the signal and under **Radix** choose **Unsigned**.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.45.40.png]]

The simulation buttons are in the menu bar. From left to right: **Restart** resets the simulation (useful after adding signals to the wave viewer, when you need to simulate again); next comes the box with the simulation time and, beside it, the **Run** button, which simulates for that time; the last button, **Stop**, halts the simulation.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_tiempo.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

To repeat the simulation, click **Restart** and then **Run -All**: the simulation will stop at the testbench's `$stop`. You can also do this by typing the commands in the message window. Alternatively, set a time such as 300 ns and click **Run**: the simulation stops at 300 ns, because that instant comes before the `$stop`.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_restart.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

#### Checking the results

After the first simulation, modify the testbench to run a complete simulation of the counter that shows all of its operating cases. As a suggestion, change the input signals in step with the clock edges. The image shows an example simulation with the counter working in up and down modes.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png]]

> [!question] Have you tested every possible operating case of the counter?
> Reset with and without *enable*, counting up and down, passing through the end count in both directions, and changing direction in the middle of a count.

## Subtask 2: Design of a shift register

![[assets/secuenciales/estrutura_tarea/imagen04.png]]

Describe in Verilog HDL a shift register with the following specifications:

- Synchronous 7-bit shift register.
- Clock active on the rising edge.
- Synchronous reset, active low.
- Serial input.
- Serial output.
- Parallel output.
- **enable** input that allows shifting.
- Intel FPGA Cyclone IV E device.

Verify its operation with a simulation that covers every possible combination of the input signals and sweeps through all values of the outputs.

## Subtask 3: Knight Rider light effect

Implement the following light sequence on the green LEDs LEDG7 to LEDG0 of the DE2-115 board:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

This design must reuse the parameterisable counter from subtask 1 and the shift register from subtask 2, as follows:

- The counter, clocked by the 50 MHz board clock, uses its **TC** output to drive the *enable* of the shift register, so that the register shifts every **0.25 s**.
- The shift register must work as a **Johnson counter**, which generates 14 states corresponding to the 14 steps of the light sequence.
- You must also create a **decoder** that, from the state of the Johnson counter, generates the outputs to LEDs LEDG7 to LEDG0.
- The counter's *enable* is controlled by switch **SW[0]** on the board.

The top level of the hierarchy must be a Verilog HDL file that instantiates the counter and the shift register and contains the decoder code.

![[assets/secuenciales/estrutura_tarea/imagen05.png]]

> [!question]- Which `fin_cuenta` value gives one shift every 0.25 s?
>> [!todo] With a 50 MHz clock (20 ns), 0.25 s / 20 ns = 12,500,000 cycles, so `fin_cuenta = 12_500_000` and `CLogB2` yields a 24-bit counter.

### Verification with a testbench

Verify the design with a ModelSim simulation. To do so, create a testbench as you did in subtasks 1 and 2.

> [!tip] Speed up the simulation
> To make the simulation faster, reduce the modulus of the counter that times the lights. For example, use a value that updates the lights every 0.25 ms instead of every 0.25 s.

The simulation result should look like this screenshot:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png]]

The design is hierarchical and contains instances of a counter and a shift register. However, the simulation only shows the signals at the top level of the testbench, not the internal signals of these submodules. You will often want to see them, especially when debugging a design that does not work. Let us see how.

Use the two subwindows on the left of ModelSim: *Structure* and *Objects*. In the first one you can unfold the complete hierarchy of the testbench and the design, with the name of each module and of each instance. In the image, the testbench **tb_lights** contains an instance of the design **lights** called `i1`. In turn, **lights** contains an instance of the counter module **contador** called `the_counter` and an instance of the register **shift7** called `the_shiftreg`.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-2.png]]

When you select an instance in the hierarchy, the *Objects* window lists all the signals defined in that module. Select the ones you are interested in, right-click and choose **Add Wave** to add them to the waveform window (*Wave*):

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-3.png]]

Although the signals now appear in the *Wave* window, their waveforms are not shown yet: they were not in the window when the simulation was launched, so ModelSim did not record them. To see them, run the simulation again from within ModelSim (without closing the window!) using the **Restart** and **Run -All** buttons, in that order:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-4.png]]

**Restart** takes the simulation back to the start (t = 0) and **Run -All** runs it again until the testbench's `$stop`. The result is the screenshot below, where the counter's internal signals are finally visible:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5.png]]

> [!warning] Deliverable
> Do the same to display the internal signals of the shift register and include a screenshot in your submission for this task.

### On-board verification

Verify the design on the DE2-115 board. To do this, select the device (FPGA) on the board and assign the pins between the design and the FPGA.

The device is selected in **Assignments > Device...**: choose the **EP4CE115F29C7** from the Cyclone IV E family.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-17-a-las-10.14.49.png]]

Pin assignment means telling the tools which FPGA pin each input and output of the design is connected to. First identify the design's inputs and outputs and their corresponding pins. The table contains the information you need:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png]]

Pins are assigned in **Assignments > Pin Planner**. The upper part of the window shows the device package seen from below: the 780 pins of the Cyclone IV are arranged in a square grid whose rows are labelled with letters and columns with numbers. The lower part lists the design's inputs and outputs with their name (**Node Name**), direction (**Direction**), location (**Location**) and other data. The **Location** column is where you specify the pin each signal connects to. For example, the system clock (`CLOCK_50`) goes to the 50 MHz oscillator, which according to the table is connected to FPGA pin Y2, so you enter `PIN_Y2` in its **Location** column.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-16-a-las-17.18.47.png]]

After assigning the pins, close the window and recompile with **Processing > Start Compilation**. The new compilation takes the pin assignments into account.

The final verification on the board is done by configuring the Cyclone IV in **JTAG** mode. Power the board (make sure it is plugged in!) and open the programmer with **Tools > Programmer**.

If **JTAG** is not selected in **Mode**, select it. If the USB-Blaster is not selected by default, click **Hardware Setup** and select it. A `.sof` configuration file with the same name as the Quartus project should appear in the list; if not, add it with **Add**. Tick the **Program/Configure** box.

The programmer window should now look like the image. Click **Start** to configure the FPGA and check the light effect on the board.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2020-03-04-a-las-10.12.34.png]]

next > [[sdp/en/task2-screen-control|Task 2 - Control and display on a screen]]
