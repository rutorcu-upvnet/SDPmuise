---
title: "Project 3: Design of an upgraded lighting effect"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[sdp/en/project2-video-controller|Project 2: Design of a video controller]]

In this project you redesign the lighting effect from [[sdp/en/project1-lighting-effect|Project 1]] using **state machines**, and add a new speed-control function using the push buttons on the board.

## Goals

- Describe finite state machines in Verilog.
- Design Moore and Mealy state machines.
- Design circuits to read push buttons.
- Create structured testbenches using *tasks*.

## Work to be done

- **Part 1:** circuit and testbench.
- **Part 2:** circuit and testbench.
- **Part 3:** circuit and testbench.
- **Project report**, including the *RTL Viewer* and *State Machine Viewer* results, the analysis/synthesis warnings report and the commented test.

> [!warning] Structured testbenches
> The testbenches in this project must be well structured: appropriate use of *tasks*, timing based on edge counting instead of fixed delays, etc.

## Project structure

The project is carried out in three incremental steps, adding blocks to the design:

1. Remake the lighting effect from Project 1 with a state machine.
2. Implement a circuit that reads button presses to control the speed.
3. Integrate everything into a single module.

The same pin assignments are used for inputs and outputs in all parts:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png]]

## Part 1: Lighting effect using a state machine

In the first part you re-implement the lighting effect from Project 1, this time with a state machine. The circuit schematic is as follows:

![[assets/disenyo-fsm/2024/proy3_ap1.png]]

The **FSM_lights** block is a **Moore** state machine that plays the role of the Johnson counter and the decoder from Project 1. It must have **14 states** and generate the specified light sequence, shown again here:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

There is also a **counter** that acts as a frequency divider; you can use the same counter as in previous projects. For the on-board test use a modulus of **5,000,000**, so that the TC signal has a frequency of **10 Hz**.

> [!question]- How many bits does the counter need for a modulus of 5,000,000?
>> [!todo] 23 bits, since 2²² = 4,194,304 < 5,000,000 ≤ 2²³ = 8,388,608. If the width is computed with `$clog2` (see [[sdp/en/project1-lighting-effect|Project 1]]) you do not need to work it out by hand.

Describe the design in Verilog and compile it.

> [!question] Questions for the report
> - Has Quartus detected the state machine?
> - Which state encoding has Quartus chosen?
>
> Do not forget to include the *State Machine Viewer* results in your report.

Write a testbench to validate the design in simulation. You can base it on the one from Project 1, but it must now be well structured (*tasks*, edge-count-based timing, etc.).

Also test the design on the board to check the movement of the lights. Push button **KEY[0]** is the reset and switch **SW[0]** is the enable, which starts or pauses the movement.

> [!tip] Different divider values in simulation and on the board
> Remember the technique from earlier projects to use one value of the frequency divider in simulation and another on the board without modifying the code: override the counter parameter from the testbench.

## Part 2: Speed control

In the second part you implement the speed-control subsystem. The final design has two push buttons as inputs, to **increase** and **decrease** the speed of the lights. The control block is a counter whose value goes up or down by one with each press of the corresponding button, and a state machine connects the buttons to the counter, translating each press into the appropriate control signals.

![[assets/disenyo-fsm/2024/proy3_ap2.png]]

The **counter** is the same as in previous designs, now with **modulus 16**. The **FSM_speed** block is a **Mealy** state machine that generates the counter's **ENABLE** and **UP_DOWN** control signals so that:

- when **KEY_UP**, connected to push button **KEY[1]**, goes low, the counter increases by 1;
- when **KEY_DN**, connected to push button **KEY[2]**, goes low, the counter decreases by 1.

Keep in mind that:

- The buttons are **active low**: the signal is 0 while the button is pressed and 1 when it is released.
- The counter must change **only once per press**, even if the button is held down for several clock cycles.

This is the same state machine as in exercise 2 of the Unit 4 exercise collection (State machines), available in PoliformaT. The figure shows the desired behaviour:

![[assets/disenyo-fsm/2024/cronograma_mealy.png]]

Describe the design in Verilog and write a testbench that checks its response in different cases, including **realistic button presses** (lasting many clock cycles). The testbench must be well structured, preferably with Verilog *tasks*; for example, a *task* that simulates a press of a given number of cycles.

Also test the design on the board. Connect the counter's **SPEED** output to the red LEDs **LEDR[3:0]** to see its value in binary.

## Part 3: Integrating the complete design

Finally, all the blocks from the previous parts are integrated into the complete design, shown in the following schematic:

![[assets/disenyo-fsm/2024/proy3_ap3.png]]

Essentially, the Part 1 design is modified by adding an extra frequency divider implemented in the **counter_variable** module. It is a 4-bit counter with a **variable** modulus: it is not a parameter, fixed at compile time, but one of the input signals, whose value may change during operation. The **END_COUNT** input is the maximum value the counter can hold, so its modulus is **END_COUNT + 1**. A value between 0 and 15 generated by the speed-control subsystem of Part 2 is used: the higher it is, the higher the modulus of counter_variable and the **lower** the speed of the lights.

This is the complete Verilog code of counter_variable:

```verilog
module counter_variable (CLK, RSTn, ENABLE, END_COUNT, COUNT, TC);

parameter width = 4;

input CLK, RSTn, ENABLE;
input [width-1:0] END_COUNT;
output reg [width-1:0] COUNT;
output TC;

always @(posedge CLK or negedge RSTn)
  if (~RSTn)
    COUNT <= 0;
  else if (ENABLE)
  begin
    if (COUNT >= END_COUNT)
      COUNT <= 0;
    else
      COUNT <= COUNT + 1;
  end

assign TC = ((COUNT == END_COUNT) && (ENABLE == 1)) ? 1 : 0;

endmodule
```

> [!question]- Why does the counter compare with `>=` instead of `==` before wrapping?
>> [!todo] Because END_COUNT may decrease while the counter is running. If COUNT is already above the new END_COUNT, with `==` the counter would keep going until it overflows (15 → 0) before respecting the new modulus.

Describe the complete design in Verilog and verify it with a testbench. You can base it on the Part 2 testbench to simulate different button presses, and on the Part 1 testbench to adapt the simulation speed and simulate the effect of the enable signal.

Also test the design on the board. In this case, connect the **COUNT** output of the variable counter to the red LEDs **LEDR[7:4]** to see its value together with the speed value from Part 2.

next > [[sdp/en/project4-touchscreen|Project 4: Design of a touchscreen interface]]
