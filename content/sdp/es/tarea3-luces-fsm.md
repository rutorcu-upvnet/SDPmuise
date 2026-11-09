---
title: "Tarea 3: Juego de luces mejorado con FSM"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[sdp/es/tarea2-control-pantalla|Tarea 2 - Control y visualización en una pantalla]]

En este proyecto se rediseña el juego de luces de la [[sdp/es/tarea1-sistemas-secuenciales|Tarea 1]] mediante **máquinas de estados** y se le añade un control de velocidad con los pulsadores de la placa.

## Objetivos

- Describir máquinas de estados finitos en Verilog.
- Diseñar máquinas de estados de Moore y de Mealy.
- Diseñar circuitos para la lectura de pulsadores.
- Crear *testbenches* estructurados mediante *tasks*.

## Estructura del proyecto

El proyecto se hace en tres pasos incrementales en los que se van añadiendo bloques al diseño: primero se rehace el juego de luces de la Tarea 1 con una máquina de estados, después se implementa un circuito que lee los pulsadores para controlar la velocidad y, por último, se integra todo en un único módulo.

En todos los apartados se usan las mismas asignaciones de pines para las entradas y salidas:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png]]

## Tareas a realizar

- Apartado 1: circuito y testbench.
- Apartado 2: circuito y testbench.
- Apartado 3: circuito, testbench y prueba en placa.
- Informe del proyecto.

> [!warning] Testbenches estructurados
> Los testbenches de este proyecto deben estar bien estructurados: uso adecuado de *tasks*, temporización basada en la cuenta de flancos en lugar de retardos fijos, etc.

## Apartado 1: Juego de luces mediante máquina de estados

En el primer apartado se vuelve a implementar el juego de luces de la Tarea 1 con una máquina de estados. El esquema del circuito es el siguiente:

![[assets/disenyo-fsm/2024/proy3_ap1.png]]

El bloque ***FSM_lights*** es una máquina de **Moore de tipo Medvedev** que sustituye al contador Johnson y al decodificador de la Tarea 1. Debe tener **14 estados** y generar la secuencia de luces especificada, que se repite aquí:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

Se añade también un contador (***counter***) que actúa como divisor de frecuencia; puede ser el mismo de las tareas anteriores. Para la prueba en placa se usa un módulo de **5 000 000**, de forma que la señal TC tenga una frecuencia de **10 Hz**.

Describe el diseño en Verilog y compílalo.

> [!question] ¿Ha detectado Quartus la máquina de estados? ¿Qué codificación de estados ha elegido?
> Incluye los resultados del *State Machine Viewer* en el informe.

Escribe un testbench para validar el diseño en simulación. Puedes partir del de la Tarea 1, pero ahora debe estar bien estructurado (uso adecuado de *tasks*, temporización basada en la cuenta de flancos en lugar de retardos fijos, etc.).

Prueba también el diseño en la placa para comprobar el movimiento de las luces. Se usa el pulsador **KEY[0]** como reset y el interruptor **SW[0]** como habilitación, que activa o pausa el movimiento.

> [!tip] Divisor distinto en simulación y en placa
> Recuerda la técnica de la Tarea 1 para usar distintos valores del divisor de frecuencia en simulación y en placa sin modificar el código (por ejemplo, sobrescribiendo el parámetro al instanciar el diseño en el testbench).

## Apartado 2: Control de velocidad

En el segundo apartado se implementa el subsistema de control de velocidad. El diseño final tendrá dos pulsadores como entradas, para aumentar y disminuir la velocidad. El bloque consiste en un contador cuyo valor aumenta o disminuye en uno con cada pulsación del botón correspondiente; una máquina de estados comunica los botones con el contador, traduciendo cada pulsación en las señales de control adecuadas.

![[assets/disenyo-fsm/2024/proy3_ap2.png]]

El contador *counter* es el de los diseños anteriores, ahora con **módulo 16**. El bloque ***FSM_speed*** es una máquina de **Mealy** que genera las señales **ENABLE** y **UP_DOWN** del contador, de forma que al pulsar **KEY[1]** (conectado a KEY_UP) el contador aumente en 1 y al pulsar **KEY[2]** (conectado a KEY_DN) disminuya en 1. Ten en cuenta que:

- Los botones son **activos a nivel bajo**: la señal vale 0 con el botón pulsado y 1 cuando no lo está.
- El contador debe cambiar **una sola vez por pulsación**, aunque el botón se mantenga pulsado durante varios ciclos de reloj.

![[assets/disenyo-fsm/2024/cronograma_mealy.png]]

Describe el diseño en Verilog y escribe un testbench que verifique su funcionamiento en simulación. Debe comprobar la respuesta en distintos casos de test, **incluyendo pulsaciones realistas** (que duran muchos ciclos de reloj), y estar bien estructurado, preferentemente con *tasks*. En el informe se valorará que las capturas de simulación **incluyan las variables de estado** (`state`/`next_state`, si procede).

Prueba también el diseño en la placa, conectando la salida de 4 bits del contador a los LEDs rojos **LEDR[3:0]** para ver su valor en binario.

## Apartado 3: Integración del diseño completo

Por último se integran todos los bloques anteriores en el diseño completo, cuyo esquema es el de la figura:

![[assets/disenyo-fsm/2024/proy3_ap3.png]]

En esencia, se modifica el diseño del apartado 1 añadiendo un divisor de frecuencia adicional, el módulo ***counter_variable***: un contador de 4 bits de **módulo variable**. Es decir, el módulo *no es un parámetro*, que queda fijo al compilar, *sino una señal de entrada* cuyo valor puede cambiar durante el funcionamiento. Su entrada **END_COUNT** indica el valor máximo de la cuenta, de modo que el módulo es END_COUNT + 1. END_COUNT tomará un valor entre 0 y 15 generado por el control de velocidad del apartado 2: cuanto mayor sea, mayor es el módulo de *counter_variable* y más despacio se mueven las luces.

Este es el código Verilog completo de *counter_variable*:

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

> [!question]- ¿Por qué se compara con `>=` y no con `==` al reiniciar la cuenta?
>> [!todo] Si END_COUNT disminuye mientras la cuenta es mayor que el nuevo valor, con `==` el contador seguiría hasta desbordar (15 → 0) antes de volver a respetar el nuevo módulo. Con `>=` vuelve a 0 en el siguiente ciclo habilitado.

Describe el diseño completo en Verilog y verifícalo con un testbench; puedes basarte en los de los apartados anteriores para simular distintas pulsaciones y el efecto de la habilitación. Prueba también el diseño en la placa, conectando la salida del contador variable a los LEDs rojos **LEDR[7:4]** para ver su valor a la vez que el del contador del apartado 2.

next > [[sdp/es/tarea3-fsm-motor|Tarea 3 - Diseño de máquinas de estados finitos]]
