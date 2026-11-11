---
title: "Proyecto 3: Diseño de un juego de luces mejorado"
draft: false
tags:
  - verilog
  - fsm
---

prev > [[sdp/es/proyecto2-controlador-video|Proyecto 2: Diseño de un controlador de vídeo]]

En este proyecto se rediseña el juego de luces del [[sdp/es/proyecto1-juego-luces|Proyecto 1]] utilizando **máquinas de estados**, y se le añade una nueva función de control de velocidad mediante los botones pulsadores de la placa.

## Objetivos

- Describir máquinas de estados finitos en Verilog.
- Diseñar máquinas de estados de Moore y de Mealy.
- Diseñar circuitos para la lectura de botones pulsadores.
- Crear *testbenches* estructurados mediante *tasks*.

## Tareas a realizar

- **Apartado 1:** circuito y *testbench*.
- **Apartado 2:** circuito y *testbench*.
- **Apartado 3:** circuito y *testbench*.
- **Informe del proyecto**, incluyendo los resultados del *RTL Viewer* y del *State Machine Viewer*, el informe de *warnings* de análisis/síntesis y el test comentado.

> [!warning] Testbenches estructurados
> Los *testbenches* de este proyecto deben estar bien estructurados: uso adecuado de *tasks*, temporización basada en la cuenta de flancos en lugar de retardos fijos, etc.

## Estructura del proyecto

El proyecto se realiza en tres pasos incrementales en los que se van añadiendo bloques al diseño:

1. Rehacer el juego de luces del Proyecto 1 mediante una máquina de estados.
2. Implementar un circuito que lea las pulsaciones de los botones para controlar la velocidad.
3. Integrar todo en un único módulo.

En todos los apartados se utilizan las mismas asignaciones de pines para las entradas y salidas:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png]]

## Apartado 1: Juego de luces mediante máquina de estados

En el primer apartado se vuelve a implementar el juego de luces del Proyecto 1, esta vez con una máquina de estados. El esquema del circuito es el siguiente:

![[assets/disenyo-fsm/2024/proy3_ap1.png]]

El bloque **FSM_lights** es una máquina de estados de **Moore** que hace el papel del contador Johnson y del decodificador del Proyecto 1. Debe tener **14 estados** y generar la secuencia de luces especificada, que se reproduce de nuevo aquí:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

Se añade también un contador (**counter**) que actúa como divisor de frecuencia; puede utilizarse el mismo contador de los proyectos anteriores. Para la prueba en placa se usa un módulo de **5 000 000**, de modo que la señal TC tenga una frecuencia de **10 Hz**.

> [!question]- ¿Cuántos bits necesita el contador para un módulo de 5 000 000?
>> [!todo] 23 bits, ya que 2²² = 4 194 304 < 5 000 000 ≤ 2²³ = 8 388 608. Con la anchura calculada mediante `$clog2` (ver el [[sdp/es/proyecto1-juego-luces|Proyecto 1]]) no hace falta calcularlo a mano.

Describe el diseño en Verilog y compílalo.

> [!question] Preguntas para el informe
> - ¿Ha detectado Quartus la máquina de estados?
> - ¿Qué codificación de estados ha elegido Quartus?
>
> No olvides incluir los resultados del *State Machine Viewer* en el informe.

Realiza un *testbench* para validar el funcionamiento en simulación. Puedes basarte en el del Proyecto 1, pero ahora debe estar bien estructurado (*tasks*, temporización basada en cuenta de flancos, etc.).

Prueba también el diseño en la placa para comprobar el movimiento de las luces. El pulsador **KEY[0]** actúa como reset y el interruptor **SW[0]** como habilitación, que activa o pausa el movimiento.

> [!tip] Divisor distinto en simulación y en placa
> Recuerda la técnica de los proyectos anteriores para usar un valor del divisor de frecuencia en simulación y otro en la placa sin modificar el código: redefinir el parámetro del contador desde el *testbench*.

## Apartado 2: Control de velocidad

En el segundo apartado se implementa el subsistema de control de velocidad. El diseño final tendrá dos botones como entradas, para **aumentar** y **disminuir** la velocidad de movimiento. El bloque de control es un contador cuyo valor aumenta o disminuye en uno con cada pulsación del botón correspondiente, y una máquina de estados comunica los botones con el contador traduciendo cada pulsación en las señales de control adecuadas.

![[assets/disenyo-fsm/2024/proy3_ap2.png]]

El contador **counter** es el mismo de diseños anteriores, ahora con **módulo 16**. El bloque **FSM_speed** es una máquina de estados de **Mealy** que genera las señales de control **ENABLE** y **UP_DOWN** del contador, de forma que:

- cuando se activa a nivel bajo **KEY_UP**, conectada al pulsador **KEY[1]**, el contador aumenta su valor en 1;
- cuando se activa **KEY_DN**, conectada al pulsador **KEY[2]**, el contador disminuye su valor en 1.

Ten en cuenta que:

- Los botones son **activos a nivel bajo**: la señal vale 0 cuando el botón está pulsado y 1 cuando no lo está.
- El contador debe cambiar **una sola vez por pulsación**, aunque el botón se mantenga pulsado durante varios ciclos de reloj.

Se trata de la misma máquina descrita en el ejercicio 2 del boletín de problemas del tema 4 (Máquinas de estados), disponible en PoliformaT. La figura ilustra el comportamiento deseado:

![[assets/disenyo-fsm/2024/cronograma_mealy.png]]

Describe el diseño en Verilog y realiza un *testbench* que compruebe la respuesta frente a distintos casos, incluyendo **pulsaciones realistas** de los botones (que duran muchos ciclos de reloj). El *testbench* debe estar bien estructurado, preferentemente mediante *tasks* de Verilog; por ejemplo, una *task* que simule una pulsación de un número dado de ciclos.

Prueba también el diseño en la placa. Para ello, conecta la salida **SPEED** del contador a los LEDs rojos **LEDR[3:0]** para observar su valor en binario.

## Apartado 3: Integración del diseño completo

Por último, se integran todos los bloques de los apartados anteriores para obtener el diseño completo, cuyo esquema es el siguiente:

![[assets/disenyo-fsm/2024/proy3_ap3.png]]

En esencia, se modifica el diseño del apartado 1 añadiendo un divisor de frecuencia adicional implementado en el módulo **counter_variable**. Es un contador de 4 bits cuyo módulo es **variable**: no es un parámetro, que queda fijo al compilar, sino una de las señales de entrada, cuyo valor puede cambiar en funcionamiento. La entrada **END_COUNT** indica el valor máximo que puede contener el contador, es decir, su módulo es **END_COUNT + 1**. Se usa un valor de END_COUNT entre 0 y 15 generado por el subsistema de control de velocidad del apartado 2: cuanto mayor sea, mayor es el módulo de counter_variable y **menor** la velocidad de las luces.

Este es el código Verilog completo de counter_variable:

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
>> [!todo] Porque END_COUNT puede disminuir mientras el contador está funcionando. Si COUNT ya es mayor que el nuevo END_COUNT, con `==` el contador seguiría hasta desbordar (15 → 0) antes de volver a respetar el nuevo módulo.

Describe el diseño completo en Verilog y verifícalo mediante un *testbench*. Puedes basarte en el del apartado 2 para simular distintas pulsaciones de botones, y en el del apartado 1 para adaptar la velocidad de la simulación y simular el efecto de la habilitación.

Prueba también el diseño en la placa. En este caso, conecta la salida **COUNT** del contador variable a los LEDs rojos **LEDR[7:4]** para observar su valor a la vez que el valor de velocidad del apartado 2.

next > [[sdp/es/proyecto4-pantalla-tactil|Proyecto 4: Diseño de un interfaz para pantalla táctil]]
