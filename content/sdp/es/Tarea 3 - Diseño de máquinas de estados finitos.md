---
title: "Tarea 3: Diseño de máquinas de estados finitos"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[Tarea 3 - Juego de luces mejorado con FSM]]

*Por Ricardo José Colom Palero*

En esta tarea se plantean las bases de la práctica dedicada al diseño de **máquinas de estados finitos** (FSM), tomando como ejemplo el diseño de un controlador para un motor paso a paso.

<iframe src="/static/animaciones/Disenyo%20FSM/Objetivos/objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Objetivos

El objetivo de la práctica es aprender los conceptos básicos de Verilog HDL para el diseño de máquinas de estados finitos. Se usarán las principales construcciones de Verilog HDL para describir FSM, con especial atención a las particularidades del diseño de máquinas de estados en Quartus. La **metodología de verificación funcional** es muy importante en esta práctica. Como ejemplo se diseñará un controlador para un motor paso a paso, que se verificará con un entorno físico desarrollado por los profesores de la asignatura.

## Control de un motor paso a paso

![[assets/Disenyo FSM/Control_Motor_PP/18866.jpg]]

Un motor paso a paso es un dispositivo electromecánico que convierte una serie de impulsos eléctricos en desplazamientos angulares discretos: avanza un número de grados (un **paso**) según sus entradas de control.

Sus ventajas son la precisión y la repetibilidad en el posicionamiento.

Los motores paso a paso más utilizados son de dos tipos: de **imán permanente** y de **reluctancia variable**. Los de imán permanente pueden ser bipolares o unipolares.

De forma simplificada, un motor bipolar de imán permanente está formado por un imán permanente giratorio rodeado por los polos del estátor, que llevan los devanados, como muestra la figura. Aplicando secuencialmente una corriente de excitación bidireccional a los devanados, el motor gira en pasos según se suceden las conmutaciones.

![[assets/Disenyo FSM/Control_Motor_PP/Dibujos_bobinado01.png]]

Para un motor de este tipo hay tres secuencias de accionamiento posibles:

**Una fase (*wave*).** Se aplica la corriente a los devanados en la secuencia AB / CD / BA / DC, donde BA significa corriente por el devanado AB en sentido opuesto. Solo hay una fase activa en cada momento:

![[assets/Disenyo FSM/Control_Motor_PP/Dibujos_bobinado02.png]]

**Dos fases (paso completo o *normal*).** Se excitan las dos fases a la vez, de modo que el rotor se alinea siempre entre dos polos. Es la secuencia habitual para un motor bipolar y la que da **mayor par**:

![[assets/Disenyo FSM/Control_Motor_PP/Dibujos_bobinado03.png]]

**Medio paso (*half*).** Combina las dos anteriores, excitando primero una fase, luego dos, luego una, etc., de modo que el motor avanza en incrementos de medio paso. Reduce a la mitad el ángulo de paso efectivo, pero da un par menos regular:

![[assets/Disenyo FSM/Control_Motor_PP/Dibujos_bobinado04.png]]

Para girar en sentido contrario (antihorario) se usan las mismas tres secuencias en orden inverso. En estos diagramas el motor tiene un ángulo de paso de 90°; los motores reales tienen muchos polos y pasos de pocos grados, pero las secuencias de accionamiento son las mismas.

![[assets/Disenyo FSM/Control_Motor_PP/stepper_motor_inside.jpg]]

### El controlador L297

Hay varios componentes electrónicos que facilitan el control de un motor paso a paso generando la secuencia de fases correcta. La figura muestra un montaje basado en los circuitos **L297** y **L298** de STMicroelectronics.

El L297 integra toda la circuitería de control necesaria para motores paso a paso bipolares y unipolares. Combinado con un driver de doble puente como el L298, forma una interfaz completa para controlar un motor bipolar desde un microprocesador.

El L297 genera las secuencias de medio paso, paso completo de una fase y paso completo de dos fases. Se controla con dos entradas, el sentido de giro (*Dirección*) y el modo (*Half/Full*), y una señal *Reloj_paso* que hace avanzar de un paso al siguiente. Las salidas A, B, C y D proporcionan la secuencia de fases al L298, y las salidas de inhibición permiten controlarlo.

![[assets/Disenyo FSM/Control_Motor_PP/Dibujos_bobinado06.png]]

Internamente, el L297 tiene un contador de 3 bits y algo de lógica combinacional que generan una secuencia de **ocho pasos**, de la que se obtienen fácilmente las tres secuencias de accionamiento. Esta secuencia corresponde directamente al modo de medio paso, que se selecciona con *Half/Full* a nivel alto. La figura muestra las formas de onda del modo de medio paso:

![[assets/Disenyo FSM/Estructura_Tarea/Imagen09.png]]

Los modos de paso completo se obtienen saltando estados alternos de la secuencia de ocho pasos: el reloj de paso no actúa sobre la primera etapa del contador, cuyo bit menos significativo no cambia. Por eso la secuencia depende del estado en que se seleccione el paso completo (*Half/Full* a nivel bajo). Si se selecciona en un estado **impar**, se obtiene el paso completo de **dos fases**:

![[assets/Disenyo FSM/Estructura_Tarea/Imagen08.png]]

Si se selecciona en un estado **par**, se obtiene el paso completo de **una fase** (*wave*):

![[assets/Disenyo FSM/Estructura_Tarea/Imagen07.png]]

En los modos de medio paso y de una fase se generan además dos salidas, **INH1** e **INH2**: señales de inhibición que se conectan al L298 para controlar la corriente de descarga de los devanados cuando se desconectan.

## Estructura de la tarea

<iframe src="/static/animaciones/Disenyo%20FSM/Estructura_Tarea/indice.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

La práctica se centra en el diseño de máquinas de estados finitos con Verilog HDL; como aplicación se ha elegido un controlador para un motor paso a paso.

Se divide en **tres subtareas**: la primera es el diseño de la máquina de estados que controla el motor; la segunda, su verificación en hardware, usando un entorno que emula el motor en una pantalla, ya que no se dispone de un motor real; la tercera, rehacer con una máquina de estados el juego de luces del coche fantástico de la [[Tarea 1 - Diseño de sistemas secuenciales|Tarea 1]].

## Subtarea 1: Controlador para un motor paso a paso

![[assets/Disenyo FSM/Estructura_Tarea/Imagen01.png]]

Describe en Verilog HDL un controlador para un motor paso a paso que emule el comportamiento del circuito integrado **L297**. El controlador será una máquina de **ocho estados**, cada uno de los cuales determina la situación de los devanados del motor. La evolución por los estados hace girar el motor: cada cambio de estado es un paso. El controlador tendrá cinco entradas:

- **CLK**: reloj, activo por flanco de subida.
- **RESET**: asíncrono y activo a nivel bajo; lleva el controlador al estado inicial, llamado «HOME».
- **ENABLE**: activo a nivel alto; mientras está activo, el controlador hace girar el motor (va cambiando de estado).
- **UP_DOWN**: sentido de giro. A nivel alto el motor gira en sentido horario y a nivel bajo en sentido antihorario.
- **HALF_FULL**: modo de funcionamiento. A nivel alto el motor funciona en modo HALF y a nivel bajo en modo NORMAL o WAVE.

Tendrá también seis salidas, **A**, **B**, **C**, **D**, **INH1** e **INH2**, cuyo comportamiento depende del modo de funcionamiento según los diagramas temporales siguientes.

### Diagramas temporales

Las seis salidas deben ajustarse, según el modo de funcionamiento, a estos diagramas temporales:

![[assets/Disenyo FSM/Estructura_Tarea/Imagen09.png]]

![[assets/Disenyo FSM/Estructura_Tarea/Imagen08.png]]

![[assets/Disenyo FSM/Estructura_Tarea/Imagen07.png]]

De los diagramas se deduce que hay tres modos de funcionamiento según cómo evolucione la máquina:

- **HALF** (medio paso): la máquina pasa secuencialmente por todos los estados.
- **NORMAL**: el controlador solo pasa por los estados impares.
- **WAVE**: la máquina pasa por los estados pares.

En HALF el motor gira a medio paso y en los otros dos a paso completo. El modo se selecciona con **HALF_FULL**: a nivel alto el modo es HALF; a nivel bajo será NORMAL o WAVE según el estado en que se encuentre la máquina.

### Diseño de la máquina de estados

Para empezar el diseño hay que analizar las especificaciones y la información disponible, sobre todo los diagramas temporales, que indican cómo deben generarse las salidas para que el motor funcione. Analizándolos con detalle se concluye que:

- La máquina tendrá **ocho estados**, por los que irá evolucionando para hacer girar el motor.
- El paso por los estados es **cíclico** y depende de las entradas.
- El **sentido de giro** depende solo del **orden en que se recorren los estados**: ascendente para giro horario y descendente para antihorario.
- Como se ve en la figura, sea cual sea el modo (y por tanto las entradas), **las salidas solo dependen del estado**. La máquina será, por tanto, de **Moore**.

![[assets/Disenyo FSM/Estructura_Tarea/Imagen12.png]]

Antes de escribir el código Verilog hay que tener un **diagrama ASM** o un diagrama de burbujas que describa el funcionamiento de la máquina y sus transiciones.

La figura muestra el diagrama ASM de uno de los ocho estados: según las entradas se determina el `Estado Siguiente`. Al ser una máquina de Moore, las salidas solo dependen del estado y no de las entradas.

El `Estado Actual` es **`S1`**, y evaluando las entradas se determina el `Estado Siguiente`. Primero se evalúa **`ENABLE`**, que decide si el motor gira, es decir, si se mantiene el estado o se cambia. Después, **`HALF_FULL`** decide si el motor va a medio paso o a paso completo. A medio paso, el siguiente estado es **`S2`** o **`S8`**, según **`UP_DOWN`**. A paso completo, el siguiente estado es **`S3`** o **`S7`**, según el sentido de giro; en este caso solo se recorren estados impares (**`S1`**, **`S3`**, **`S5`**, **`S7`**), es decir, el motor está en modo **NORMAL**.

![[assets/Disenyo FSM/Estructura_Tarea/Estado_FSM_Motor.png]]

Una máquina de Moore se puede describir en HDL con **tres bloques procedurales**, como muestra la figura. De izquierda a derecha: el primero calcula el estado siguiente a partir de las entradas y del estado actual; el intermedio registra el estado siguiente en cada flanco de reloj, produciendo el cambio de estado; el último genera las salidas en función del estado actual.

![[assets/Disenyo FSM/Estructura_Tarea/Imagen11.png]]

La figura muestra la descripción Verilog del bloque que determina el `Estado Siguiente` a partir del `Estado Actual` y de las entradas. Es una traducción directa del diagrama ASM: una sentencia `case` que, para cada estado actual, evalúa las entradas y determina el estado siguiente.

![[assets/Disenyo FSM/Estructura_Tarea/Imagen15.png]]

> [!warning] Nombre del módulo y de los puertos
> Es imprescindible que el módulo se llame **`control_motor`** y que los puertos tengan exactamente los nombres indicados, porque el entorno de verificación de la subtarea 2 lo instancia así. La figura muestra cómo debe ser la cabecera del archivo `control_motor.v`.

![[assets/Disenyo FSM/Estructura_Tarea/Imagen14.png]]

Verifica la máquina de estados mediante una simulación que contemple todas las combinaciones posibles de las entradas y recorra completamente los valores de las salidas.

## Subtarea 2: Verificación del controlador

Para verificar físicamente el controlador haría falta un motor paso a paso, pero la placa DE2-115 no lo tiene, ni la electrónica para conectarlo. ¿Cómo se verifica entonces? Con un **emulador de motor paso a paso** desarrollado por los profesores con la placa DE2-115 y la pantalla táctil.

La figura muestra la estructura del emulador: un diseño de verificación o *testbench* que engloba el diseño bajo test (DUT), en este caso tu controlador. El testbench genera las entradas del DUT, recoge sus salidas e interactúa con la placa. En la pantalla se muestran puntos rojos y verdes alternos dispuestos en circunferencia, que representan el giro del motor.

![[assets/Disenyo FSM/Estructura_Tarea/Imagen02.png]]

El emulador usa también otros elementos de la placa:

| Elemento | Función |
| --- | --- |
| Pulsador **KEY0** | **RESET** de todo el sistema |
| Interruptor **SW0** | Entrada **ENABLE** del controlador |
| Interruptor **SW1** | Entrada **HALF_FULL** del controlador |
| Interruptor **SW2** | Entrada **UP_DOWN** del controlador |
| **LEDG0**–**LEDG5** | Salidas **A**, **B**, **C**, **D**, **INH1** e **INH2** |
| **LEDR0**–**LEDR15** | Los 16 puntos o pasos en que se divide una vuelta en la pantalla |
| Display **HEX0** | Estado de la máquina (1 a 8), deducido de las salidas A, B, C, D, INH1 e INH2 según los diagramas del L297 |
| Display **HEX1** | Letra **E** (de *estado*) |
| Display **HEX3** | Velocidad de giro, de 0 a 9; cada incremento la duplica: 0 es un paso (o medio paso) por segundo y 9, un paso cada 1,95 ms |

En la **pantalla táctil**:

- En el **centro**, 16 puntos (8 rojos y 8 verdes alternos) en trayectoria circular representan el giro. A medio paso se iluminan alternativamente puntos rojos y verdes; a paso completo solo rojos o solo verdes, según el modo sea *normal* o *wave*.
- En la **parte inferior**, dos botones **+** y **−** aumentan y disminuyen la velocidad de giro.

Para verificar el controlador con el emulador:

1. Descarga de PoliformaT el archivo [[assets/Disenyo FSM/Estructura_Tarea/motor_alumno.qar|motor_alumno.qar]].
2. Haz doble clic sobre él para desempaquetar el proyecto de Quartus que contiene el emulador. Quartus preguntará dónde desempaquetarlo y si quieres abrirlo.
3. Una vez abierto, comprueba que hay un módulo superior `Verifica_motor` que instancia dos bloques: `testbench`, que está oculto, y `control_motor`, que no existe porque es tu diseño de la subtarea anterior.
4. Copia tu archivo `control_motor.v` en el directorio del proyecto de verificación que acabas de desempaquetar.
5. Compila el proyecto. Si hay errores de sintaxis, se deberán a discrepancias en los nombres de los puertos o del módulo `control_motor`. Corrige **tu** módulo `control_motor`, **nunca** el archivo `verifica_motor`.
6. Cuando compile sin errores, programa la FPGA de la placa.
7. Prueba el funcionamiento con los distintos pulsadores e interruptores.

## Subtarea 3: Juego de luces del coche fantástico con una máquina de estados

Ahora que sabes diseñar una máquina de estados en Verilog HDL, vuelve a plantear el juego de luces del coche fantástico con un enfoque basado en FSM. Además, implementa un **variador de velocidad**: con el pulsador **KEY[2]** se disminuye la velocidad de la secuencia y con **KEY[1]** se aumenta.

El nuevo diseño debe verificarse con un testbench en ModelSim y en la placa DE2-115.

Las figuras siguientes muestran el diagrama de bloques propuesto y una sugerencia de pasos a seguir:

<iframe src="/static/animaciones/Disenyo%20FSM/SubTarea3/Diagrama_Bloques/Diagrama_bloques.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

<iframe src="/static/animaciones/Disenyo%20FSM/SubTarea3/Pasos/Pasos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Verifica el diseño mediante simulación, con un testbench que compruebe la respuesta en distintos casos de test (pulsaciones de botones, etc.).

Verifícalo también en la placa DE2-115, con la siguiente asignación de pines:

![[assets/Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.31.png]]

next > [[Tarea 4 - Diseño de una comunicación serie]]
