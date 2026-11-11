---
title: "Project 1: Design of a lighting effect"
draft: false
tags:
  - verilog
  - sequential
---

prev > [[sdp/en/qar-archive|Help: creating QAR files]]

In this first project you design **parameterisable** versions of familiar sequential circuits (counters and shift registers) and combine them into a lighting effect that moves horizontally across the board's LEDs. You will also practise verifying your designs with testbenches in ModelSim.

## Goals

- Describe sequential circuits in Verilog.
- Design parameterisable modules.
- Design hierarchical systems.
- Verify digital circuits with testbenches.

## Work to be done

- Part 1: circuit and testbench.
- Part 2: circuit and testbench.
- Part 3: circuit and testbench (including the corner case).
- Project report, with the *RTL Viewer* results, the analysis/synthesis warnings report and the commented test.

## Introduction

An efficient engineer makes the most of design time, and reusing previously designed modules is key to that. One feature of hardware description languages such as Verilog that makes reuse easier is the ability to define **parameterisable modules**.

For example, if we already have an 8-bit counter and now need a 10-bit one, the obvious solution would be to copy the description and modify it, but we would end up with a collection of files, one per size. It is much better to have **a single file** with a parameterisable counter whose width depends on a parameter chosen for each instance as needed.

This project applies that approach to the most common sequential subsystems, binary counters and shift registers, which are then instantiated and combined to animate the LEDs on the lab board.

## Part 1: Parameterisable counter

![[assets/secuenciales/estrutura_tarea/module-counter.png]]

Describe in Verilog a binary counter with the following specifications:

- Synchronous up/down counter with parameterisable modulus `modulo`.
- Operates on the rising edge of clock **CLK**.
- Asynchronous reset **RSTn** (highest priority), active low.
- Active-high **ENABLE** input that enables counting.
- If **UP_DOWN** is high the counter counts up; otherwise it counts down.
- **TC** (*Terminal Count*) output, active high when the counter reaches the end of the count.

> [!tip] Counter width
> The number of bits of the count can be computed from the parameter with the `$clog2` system function, which returns the base-2 logarithm rounded up:
> ```verilog
> parameter modulo = 20;
> localparam N = $clog2(modulo);   // bits needed to count from 0 to modulo-1
> output reg [N-1:0] COUNT;
> ```

Verify it with a simulation, using a Verilog testbench, that covers every possible combination of the inputs and checks the values of the outputs.

You can start from the Verilog code of the Tutorial lab: you will have to make the counter bidirectional and generate **TC** correctly in both directions, and extend the testbench to check all its features.

The image shows an example simulation with the counter working in up and down modes.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png]]

> [!question] Have you tested every possible operating case of the counter?

## Part 2: Parameterisable shift register

![[assets/secuenciales/estrutura_tarea/module-shiftreg.png]]

Describe in Verilog a shift register with the following specifications:

- Synchronous shift register with parameterisable width `ancho`.
- Operates on the rising edge of clock **CLK**.
- Asynchronous reset **RSTn** (highest priority), active low.
- Serial input **SHIFT_IN**.
- Serial output **SHIFT_OUT**.
- Parallel output **OUT_P**.
- Active-high **ENABLE** input that enables shifting.

Verify it with a simulation, using a Verilog testbench, that covers every possible combination of the inputs and checks the values of the outputs.

## Part 3: Integrating the lighting effect

Implement this light sequence on the green LEDs (LEDG7 to LEDG0) of the DE2-115 board:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

The design must have these inputs and outputs:

- Clock **CLK**, active on the rising edge.
- Asynchronous reset **RSTn**, active low.
- Synchronous enable **ENABLE**, active high. When active, the light moves normally; when inactive, the sequence is paused.
- 8-bit output **LEDS**, connected to LEDs LEDG0 to LEDG7.

![[assets/secuenciales/estrutura_tarea/module-luces-1.png]]

You must reuse the counter from Part 1 and the shift register from Part 2. The internal structure of the design is shown in the figure:

![[assets/secuenciales/estrutura_tarea/estructura-luces.png]]

The top level of the hierarchy must be a Verilog file that instantiates the counter and the register and contains the decoder code. Keep in mind that:

- The counter acts as a **frequency divider**: clocked by the board's 50 MHz clock, its **TC** output enables the shift register so that it shifts every **0.25 s**.
- The shift register works as a **Johnson counter**, which generates the 14 states of the light sequence. How many bits must it have?
- You must add **decoding logic** that generates the 8 LED outputs from the Johnson counter. You can use an `always` block.
- The counter's enable is controlled by switch **SW0** on the board, so you can test pausing the sequence.

> [!question]- What modulus does the divider need, and how wide is the register?
>> [!todo] 0.25 s / 20 ns = 12,500,000 cycles, so the divider has modulus 12,500,000 (`$clog2` gives 24 bits). An *n*-bit Johnson counter has 2*n* states, so 14 states need a 7-bit register.

### Verification with a testbench

Verify the design with a ModelSim simulation, using a testbench similar to those of Parts 1 and 2.

> [!tip] Speed up the simulation without touching the design
> If the lights change every 0.25 s, the simulation takes a long time. It is advisable to reduce the divider's modulus in simulation only. **We recommend (and will value)** the technique from section 2 of the Tutorial lab: add a parameter to the top level of the design so that you can simulate and implement on the board with different divider values without changing the code.

The simulation result should look like this screenshot:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png]]

By default, ModelSim only shows the signals at the top level of the testbench, not the internal signals of the design or its instances (the counter and the register). Following the procedure from the Tutorial lab, add the internal signals of the counter and the register to the wave viewer.

> [!warning] Deliverable
> Include in your report a screenshot of the result similar to the one below (where only the counter signals are shown).

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5_modificada.png]]

### Verification of a corner case

Thorough verification must also cover unlikely extreme cases, and it is up to us to anticipate them. Here, a situation that may cause problems is **disabling the system exactly when TC (the divider output) is active**.

Modify your testbench, if you have not already done so, to include this case and observe how the circuit behaves. Is it the expected behaviour? If not, why does it happen? Where is the problem? Display the internal signals of the counter and the register in ModelSim to locate it, and fix the design. If you need to change the counter or the register, verify them again with the Part 1 or Part 2 testbench to make sure they still work on their own.

> [!tip] Accessing internal signals from the testbench
> With the `.` operator you can read a module's internal signals even if they are not inputs or outputs. For example, to check whether signal **TC** in instance `duv` is 1:
> ```verilog
> if (duv.TC == 1) ...
> ```
> and to wait until it takes that value:
> ```verilog
> wait (duv.TC == 1);
> ```

### On-board verification

Implement the design on the DE2-115 board and check that it works. When you created the Quartus project you must have selected the board's FPGA, model **EP4CE115F29C7** of the **Cyclone IV E** family; if not, change it in **Assignments > Device**.

Also assign the pins, i.e. which FPGA pin each input and output connects to, using the same procedure as in the Tutorial lab. The connections are:

| Signal | Board element |
| --- | --- |
| **CLK** | 50 MHz clock **CLOCK_50** |
| **RSTn** | Push button **KEY0** |
| **ENABLE** | Switch **SW0** |
| **LEDS** | Green LEDs **LEDG0** to **LEDG7** |

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png]]

Remember that after assigning the pins you must compile the design again before programming it on the board.

next > [[sdp/en/project2-video-controller|Project 2: Design of a video controller]]
