---
title: "Task 3: Design of finite state machines"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[sdp/en/task3-lights-fsm|Task 3 - Upgraded lighting effect with FSMs]]

*By Ricardo José Colom Palero*

This task lays the foundations for the lab on **finite state machines** (FSMs), using the design of a stepper motor controller as an example.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/disenyo-fsm/objetivos/objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Goals

The goal of this lab is to learn the basic concepts of Verilog HDL for designing finite state machines. You will use the main Verilog HDL constructs for describing FSMs, with special attention to the particularities of state machine design in Quartus. The **functional verification methodology** is very important in this lab. As an example, you will design a stepper motor controller and verify it with a physical environment developed by the course instructors.

## Controlling a stepper motor

![[assets/disenyo-fsm/control_motor_pp/18866.jpg]]

A stepper motor is an electromechanical device that converts a series of electrical pulses into discrete angular movements: it rotates a fixed angle (a **step**) according to its control inputs.

Its advantages are precision and repeatability in positioning.

The most common stepper motors are of two types: **permanent magnet** and **variable reluctance**. Permanent magnet steppers can be bipolar or unipolar.

In simplified form, a bipolar permanent magnet motor consists of a rotating permanent magnet surrounded by stator poles carrying the coils, as shown in the figure. Applying a bidirectional excitation current to the coils in sequence makes the motor turn step by step as the commutations follow one another.

![[assets/disenyo-fsm/control_motor_pp/dibujos_bobinado01.png]]

For this type of motor there are three possible drive sequences:

**One phase (*wave*).** Current is applied to the coils in the sequence AB / CD / BA / DC, where BA means current through coil AB in the opposite direction. Only one phase is active at a time:

![[assets/disenyo-fsm/control_motor_pp/dibujos_bobinado02.png]]

**Two phases (full step or *normal*).** Both phases are energised at the same time, so the rotor always aligns halfway between two poles. This is the usual sequence for a bipolar motor and gives the **highest torque**:

![[assets/disenyo-fsm/control_motor_pp/dibujos_bobinado03.png]]

**Half step.** It combines the previous two, energising first one phase, then two, then one, and so on, so that the motor moves in half-step increments. It halves the effective step angle but gives a less even torque:

![[assets/disenyo-fsm/control_motor_pp/dibujos_bobinado04.png]]

To turn in the opposite direction (counterclockwise), the same three sequences are used in reverse order. In these diagrams the motor has a 90° step angle; real motors have many poles and steps of a few degrees, but the drive sequences are the same.

![[assets/disenyo-fsm/control_motor_pp/stepper_motor_inside.jpg]]

### The L297 controller

Several electronic components make it easier to control a stepper motor by generating the correct phase sequence. The figure shows a circuit based on the STMicroelectronics **L297** and **L298** devices.

The L297 integrates all the control circuitry needed for bipolar and unipolar stepper motors. Combined with a dual bridge driver such as the L298, it forms a complete interface for controlling a bipolar motor from a microprocessor.

The L297 generates the half-step, one-phase full-step and two-phase full-step sequences. It is controlled by two inputs, the direction of rotation (*Dirección*) and the mode (*Half/Full*), plus a *Reloj_paso* (step clock) signal that advances from one step to the next. Outputs A, B, C and D provide the phase sequence to the L298, and the inhibit outputs allow it to be controlled.

![[assets/disenyo-fsm/control_motor_pp/dibujos_bobinado06.png]]

Internally, the L297 has a 3-bit counter and some combinational logic that generate an **eight-step** sequence, from which the three drive sequences are easily obtained. This sequence corresponds directly to half-step mode, selected with *Half/Full* high. The figure shows the half-step waveforms:

![[assets/disenyo-fsm/estructura_tarea/imagen09.png]]

Full-step modes are obtained by skipping alternate states of the eight-step sequence: the step clock bypasses the first stage of the counter, whose least significant bit does not change. The resulting sequence therefore depends on the state in which full step is selected (*Half/Full* low). If it is selected in an **odd** state, you get the **two-phase** full-step sequence:

![[assets/disenyo-fsm/estructura_tarea/imagen08.png]]

If it is selected in an **even** state, you get the **one-phase** (*wave*) full-step sequence:

![[assets/disenyo-fsm/estructura_tarea/imagen07.png]]

In half-step and one-phase modes two more outputs are generated, **INH1** and **INH2**: inhibit signals connected to the L298 to control the decay current of the coils when they are switched off.

## Structure of the task

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/disenyo-fsm/estructura_tarea/indice.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

The lab focuses on designing finite state machines with Verilog HDL; the chosen application is a stepper motor controller.

It is divided into **three sub-tasks**: the first is the design of the state machine that controls the motor; the second is its verification in hardware, using an environment that emulates the motor on a screen, since no real motor is available; the third is to redo the Knight Rider light effect from [[sdp/en/task1-sequential-systems|Task 1]] with a state machine.

## Sub-task 1: Stepper motor controller

![[assets/disenyo-fsm/estructura_tarea/imagen01.png]]

Describe in Verilog HDL a stepper motor controller that emulates the behaviour of the **L297** integrated circuit. The controller is an **eight-state** machine, each state defining the condition of the motor coils. Moving through the states makes the motor turn: each state change is one step. The controller has five inputs:

- **CLK**: clock, active on the rising edge.
- **RESET**: asynchronous and active low; it takes the controller to the initial state, called "HOME".
- **ENABLE**: active high; while it is active the controller makes the motor turn (keeps changing state).
- **UP_DOWN**: direction of rotation. When high the motor turns clockwise; when low, counterclockwise.
- **HALF_FULL**: operating mode. When high the motor runs in HALF mode; when low, in NORMAL or WAVE mode.

It also has six outputs, **A**, **B**, **C**, **D**, **INH1** and **INH2**, whose behaviour depends on the operating mode as shown in the following timing diagrams.

### Timing diagrams

Depending on the operating mode, the six outputs must follow these timing diagrams:

![[assets/disenyo-fsm/estructura_tarea/imagen09.png]]

![[assets/disenyo-fsm/estructura_tarea/imagen08.png]]

![[assets/disenyo-fsm/estructura_tarea/imagen07.png]]

From the diagrams it follows that there are three operating modes, depending on how the machine evolves:

- **HALF** (half step): the machine goes through every state in sequence.
- **NORMAL**: the controller only goes through the odd states.
- **WAVE**: the machine goes through the even states.

In HALF the motor turns in half steps, and in the other two in full steps. The mode is selected with **HALF_FULL**: when high the mode is HALF; when low it is NORMAL or WAVE depending on the state the machine is in.

### Designing the state machine

Start by analysing the specifications and the available information, above all the timing diagrams, which show how the outputs must be generated for the motor to work. A detailed analysis leads to these conclusions:

- The machine has **eight states**, through which it moves to make the motor turn.
- The sequence of states is **cyclic** and depends on the inputs.
- The **direction of rotation** depends only on the **order in which the states are visited**: ascending for clockwise and descending for counterclockwise.
- As the figure shows, whatever the mode (and therefore the inputs), **the outputs depend only on the state**. The machine is therefore a **Moore** machine.

![[assets/disenyo-fsm/estructura_tarea/imagen12.png]]

Before writing the Verilog code you need an **ASM chart** or a bubble diagram describing how the machine works and its transitions.

The figure shows the ASM chart for one of the eight states: the next state (`Estado Siguiente`) is determined from the inputs. Since it is a Moore machine, the outputs depend only on the state, not on the inputs.

The current state (`Estado Actual`) is **`S1`**, and evaluating the inputs gives the next state. First **`ENABLE`** is evaluated, which decides whether the motor turns, i.e. whether the state is kept or changed. Then **`HALF_FULL`** decides between half step and full step. In half step, the next state is **`S2`** or **`S8`**, depending on **`UP_DOWN`**. In full step, the next state is **`S3`** or **`S7`**, depending on the direction; in this case only odd states are visited (**`S1`**, **`S3`**, **`S5`**, **`S7`**), so the motor is in **NORMAL** mode.

![[assets/disenyo-fsm/estructura_tarea/estado_fsm_motor.png]]

A Moore machine can be described in HDL with **three procedural blocks**, as shown in the figure. From left to right: the first computes the next state from the inputs and the current state; the middle one registers the next state on each clock edge, producing the state change; the last one generates the outputs from the current state.

![[assets/disenyo-fsm/estructura_tarea/imagen11.png]]

The figure shows the Verilog description of the block that determines the next state from the current state and the inputs. It is a direct translation of the ASM chart: a `case` statement that, for each current state, evaluates the inputs and determines the next state.

![[assets/disenyo-fsm/estructura_tarea/imagen15.png]]

> [!warning] Module and port names
> The module **must** be called **`control_motor`** and its ports must have exactly the names given above, because the verification environment in sub-task 2 instantiates it that way. The figure shows what the header of `control_motor.v` must look like.

![[assets/disenyo-fsm/estructura_tarea/imagen14.png]]

Verify the state machine with a simulation that covers every possible combination of the inputs and sweeps through all values of the outputs.

## Sub-task 2: Verifying the controller

Physically verifying the controller would require a stepper motor, but the DE2-115 board has neither a motor nor the electronics to connect one. So how can it be verified? With a **stepper motor emulator** developed by the instructors using the DE2-115 board and the touchscreen.

The figure shows the structure of the emulator: a verification design or *testbench* that wraps the design under test (DUT), in this case your controller. The testbench generates the DUT inputs, collects its outputs and interacts with the board. The screen shows alternating red and green dots arranged in a circle, which represent the rotation of the motor.

![[assets/disenyo-fsm/estructura_tarea/imagen02.png]]

The emulator also uses other elements of the board:

| Element | Function |
| --- | --- |
| Push button **KEY0** | **RESET** of the whole system |
| Switch **SW0** | Controller **ENABLE** input |
| Switch **SW1** | Controller **HALF_FULL** input |
| Switch **SW2** | Controller **UP_DOWN** input |
| **LEDG0**–**LEDG5** | Outputs **A**, **B**, **C**, **D**, **INH1** and **INH2** |
| **LEDR0**–**LEDR15** | The 16 dots or steps into which one revolution is divided on the screen |
| Display **HEX0** | Machine state (1 to 8), worked out from outputs A, B, C, D, INH1 and INH2 according to the L297 timing diagrams |
| Display **HEX1** | Letter **E** (for *estado*, state) |
| Display **HEX3** | Rotation speed, from 0 to 9; each increment doubles it: 0 is one step (or half step) per second and 9 is one step every 1.95 ms |

On the **touchscreen**:

- In the **centre**, 16 dots (8 red and 8 green, alternating) on a circular path represent the rotation. In half-step mode red and green dots light up alternately; in full-step mode only red or only green dots, depending on whether the mode is *normal* or *wave*.
- At the **bottom**, two buttons, **+** and **−**, increase and decrease the rotation speed.

To verify the controller with the emulator:

1. Download [[assets/disenyo-fsm/estructura_tarea/motor_alumno.qar|motor_alumno.qar]] from PoliformaT.
2. Double-click it to unpack the Quartus project that contains the emulator. Quartus will ask where to unpack it and whether to open it.
3. Once it is open, check that there is a top-level module `Verifica_motor` that instantiates two blocks: `testbench`, which is hidden, and `control_motor`, which does not exist because it is your design from the previous sub-task.
4. Copy your `control_motor.v` file into the directory of the verification project you have just unpacked.
5. Compile the project. Any syntax errors will be due to mismatches in the port names or in the name of the `control_motor` module. Fix **your** `control_motor` module, **never** the `verifica_motor` file.
6. Once it compiles without errors, program the FPGA on the board.
7. Test it using the different push buttons and switches.

## Sub-task 3: Knight Rider light effect with a state machine

Now that you know how to design a state machine in Verilog HDL, redo the Knight Rider light effect using an FSM-based approach. In addition, implement a **speed control**: push button **KEY[2]** decreases the speed of the sequence and **KEY[1]** increases it.

The new design must be verified with a testbench in ModelSim and on the DE2-115 board.

The following figures show the proposed block diagram and a suggested sequence of steps:

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/disenyo-fsm/subtarea3/diagrama_bloques/Diagrama_bloques.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/disenyo-fsm/subtarea3/pasos/Pasos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Verify the design by simulation, with a testbench that checks the response to different test cases (button presses, etc.).

Also verify it on the DE2-115 board, with the following pin assignments:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png]]

next > [[sdp/en/task4-serial-communication|Task 4 - Design of a serial communication]]
