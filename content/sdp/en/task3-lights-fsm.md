---
title: "Task 3: Upgraded lighting effect with FSMs"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[sdp/en/task2-screen-control|Task 2 - Control and display on a screen]]

In this project the lighting effect from [[sdp/en/task1-sequential-systems|Task 1]] is redesigned using **state machines**, and a speed control using the board's push buttons is added.

## Goals

- Describe finite state machines in Verilog.
- Design Moore and Mealy state machines.
- Design circuits to read push buttons.
- Create structured testbenches using *tasks*.

## Project structure

The project is carried out in three incremental steps in which blocks are added to the design: first the Task 1 lighting effect is rebuilt with a state machine, then a circuit that reads the push buttons to control the speed is implemented and, finally, everything is integrated into a single module.

The same pin assignments for inputs and outputs are used in every part:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png]]

## Work to be done

- Part 1: circuit and testbench.
- Part 2: circuit and testbench.
- Part 3: circuit, testbench and on-board test.
- Project report.

> [!warning] Structured testbenches
> The testbenches in this project must be well structured: appropriate use of *tasks*, timing based on counting clock edges instead of fixed delays, etc.

## Part 1: Lighting effect using a state machine

In the first part, the Task 1 lighting effect is implemented again using a state machine. The circuit schematic is as follows:

![[assets/disenyo-fsm/2024/proy3_ap1.png]]

The ***FSM_lights*** block is a **Moore machine of the Medvedev type** that replaces the Johnson counter and the decoder from Task 1. It must have **14 states** and generate the specified light sequence, shown again here:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

There is also a counter (***counter***) that acts as a frequency divider; it can be the same one used in the previous tasks. For the on-board test, use a modulus of **5,000,000** so that the TC signal has a frequency of **10 Hz**.

Describe the design in Verilog and compile it.

> [!question] Has Quartus detected the state machine? Which state encoding has it chosen?
> Include the *State Machine Viewer* results in your report.

Write a testbench to validate the design in simulation. You can start from the Task 1 testbench, but it must now be well structured (appropriate use of *tasks*, timing based on counting clock edges instead of fixed delays, etc.).

Also test the design on the board to check the movement of the lights. Push button **KEY[0]** is used as reset and switch **SW[0]** as enable, which starts or pauses the movement.

> [!tip] Different divider in simulation and on the board
> Remember the Task 1 technique for using different frequency divider values in simulation and on the board without changing the code (for example, overriding the parameter when the design is instantiated in the testbench).

## Part 2: Speed control

In the second part you implement the speed control subsystem. The final design will have two push buttons as inputs, to increase and decrease the speed. The block consists of a counter whose value goes up or down by one with each press of the corresponding button; a state machine connects the buttons to the counter, translating each press into the right control signals.

![[assets/disenyo-fsm/2024/proy3_ap2.png]]

The *counter* is the one from previous designs, now with **modulus 16**. The ***FSM_speed*** block is a **Mealy** machine that generates the counter's **ENABLE** and **UP_DOWN** signals, so that pressing **KEY[1]** (connected to KEY_UP) increases the counter by 1 and pressing **KEY[2]** (connected to KEY_DN) decreases it by 1. Keep in mind that:

- The buttons are **active low**: the signal is 0 while the button is pressed and 1 when it is released.
- The counter must change **only once per press**, even if the button is held down for several clock cycles.

![[assets/disenyo-fsm/2024/cronograma_mealy.png]]

Describe the design in Verilog and write a testbench that verifies it in simulation. It must check the response to different test cases, **including realistic button presses** (lasting many clock cycles), and be well structured, preferably with *tasks*. In the report, the simulation screenshots should **include the state variables** (`state`/`next_state`, if any).

Also test the design on the board, connecting the counter's 4-bit output to the red LEDs **LEDR[3:0]** to see its value in binary.

## Part 3: Integrating the complete design

Finally, all the previous blocks are integrated into the complete design, whose schematic is shown in the figure:

![[assets/disenyo-fsm/2024/proy3_ap3.png]]

Essentially, the Part 1 design is modified by adding an extra frequency divider, the ***counter_variable*** module: a 4-bit counter with a **variable modulus**. That is, the modulus *is not a parameter*, fixed at compile time, *but an input signal* whose value can change during operation. Its **END_COUNT** input gives the maximum count value, so the modulus is END_COUNT + 1. END_COUNT will take a value between 0 and 15 generated by the speed control from Part 2: the larger it is, the larger the modulus of *counter_variable* and the slower the lights move.

This is the complete Verilog code of *counter_variable*:

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

> [!question]- Why does the counter compare with `>=` instead of `==` when wrapping?
>> [!todo] If END_COUNT decreases while the count is above the new value, with `==` the counter would keep going until it overflows (15 → 0) before honouring the new modulus. With `>=` it returns to 0 on the next enabled cycle.

Describe the complete design in Verilog and verify it with a testbench; you can build on those from the previous parts to simulate different button presses and the effect of the enable signal. Also test the design on the board, connecting the output of the variable counter to the red LEDs **LEDR[7:4]** so that you can see its value together with that of the Part 2 counter.

next > [[sdp/en/task3-fsm-stepper|Task 3 - Design of finite state machines]]
