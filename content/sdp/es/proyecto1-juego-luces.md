---
title: "Proyecto 1: Diseño de un juego de luces"
draft: false
tags:
  - verilog
  - secuenciales
---

prev > [[sdp/es/crear-qar|Ayuda: creación de QAR]]

En este primer proyecto se diseñan versiones **parametrizables** de circuitos secuenciales conocidos (contadores y registros de desplazamiento) y se combinan para obtener un juego de luces que se desplazan horizontalmente por los LEDs de la placa. Además se practica la verificación de los diseños mediante *testbench* en ModelSim.

## Objetivos

- Describir circuitos secuenciales en Verilog.
- Diseñar módulos parametrizables.
- Diseñar sistemas con elementos jerárquicos.
- Verificar circuitos digitales mediante *testbench*.

## Tareas a realizar

- Apartado 1: circuito y testbench.
- Apartado 2: circuito y testbench.
- Apartado 3: circuito y testbench (incluido el caso extremo).
- Informe del proyecto, con los resultados del *RTL Viewer*, el informe de *warnings* de análisis y síntesis y el test comentado.

## Introducción

Un ingeniero eficiente debe aprovechar el tiempo que dedica a sus diseños, y para ello es importante reutilizar módulos ya diseñados. Una característica de los lenguajes de descripción hardware como Verilog que facilita la reutilización es la posibilidad de definir **módulos parametrizables**.

Por ejemplo, si ya tenemos un contador de 8 bits y ahora necesitamos uno de 10, la solución inmediata sería copiar la descripción y modificarla, pero así acabaríamos con una colección de archivos, uno para cada tamaño. Es mucho mejor tener **un único archivo** con un contador parametrizable, cuyo tamaño dependa de un parámetro que se elige en cada instancia según las necesidades.

En este proyecto se aplica esta filosofía a los subsistemas secuenciales más comunes, contadores binarios y registros de desplazamiento, que después se instancian y combinan para generar una animación con los LEDs de la placa del laboratorio.

## Apartado 1: Contador parametrizable

![[assets/secuenciales/estrutura_tarea/module-counter.png]]

Describe en Verilog un contador binario con las siguientes características:

- Contador síncrono ascendente/descendente de módulo parametrizable `modulo`.
- Funcionamiento por flanco de subida del reloj **CLK**.
- Reset asíncrono **RSTn** (máxima prioridad), activo a nivel bajo.
- Entrada **ENABLE** de habilitación de cuenta, activa a nivel alto.
- Si **UP_DOWN** está a nivel alto el contador cuenta hacia arriba; si no, hacia abajo.
- Salida **TC** (*Terminal Count*), activa a nivel alto cuando el contador llega al fin de cuenta.

> [!tip] Ancho del contador
> El número de bits de la cuenta se puede calcular a partir del parámetro con la función del sistema `$clog2`, que devuelve el logaritmo en base 2 redondeado hacia arriba:
> ```verilog
> parameter modulo = 20;
> localparam N = $clog2(modulo);   // bits necesarios para contar de 0 a modulo-1
> output reg [N-1:0] COUNT;
> ```

Verifica su funcionamiento con una simulación, mediante un testbench en Verilog, que contemple todas las combinaciones posibles de las entradas y compruebe los valores de las salidas.

Puedes partir del código Verilog de la práctica Tutorial: tendrás que modificar el contador para que sea bidireccional y genere **TC** correctamente en ambos sentidos, y el testbench para que compruebe todas sus características.

La imagen muestra un ejemplo de simulación con el contador funcionando en modo ascendente y descendente.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png]]

> [!question] ¿Has evaluado todos los casos posibles de funcionamiento del contador?

## Apartado 2: Registro de desplazamiento parametrizable

![[assets/secuenciales/estrutura_tarea/module-shiftreg.png]]

Describe en Verilog un registro de desplazamiento con las siguientes características:

- Registro de desplazamiento síncrono de anchura parametrizable `ancho`.
- Funcionamiento por flanco de subida del reloj **CLK**.
- Reset asíncrono **RSTn** (máxima prioridad), activo a nivel bajo.
- Entrada serie **SHIFT_IN**.
- Salida serie **SHIFT_OUT**.
- Salida paralelo **OUT_P**.
- Entrada **ENABLE** de habilitación del desplazamiento, activa a nivel alto.

Verifica su funcionamiento con una simulación, mediante un testbench en Verilog, que contemple todas las combinaciones posibles de las entradas y compruebe los valores de las salidas.

## Apartado 3: Integración del juego de luces

Implementa este juego de luces en los LEDs verdes (LEDG7 a LEDG0) de la placa DE2-115:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

El diseño debe tener estas entradas y salidas:

- Reloj **CLK**, activo por flanco de subida.
- Reset asíncrono **RSTn**, activo a nivel bajo.
- Habilitación síncrona **ENABLE**, activa a nivel alto. Activa, la luz se mueve con normalidad; desactivada, la secuencia queda en pausa.
- Salida **LEDS** de 8 bits, conectada a los LEDs LEDG0 a LEDG7.

![[assets/secuenciales/estrutura_tarea/module-luces-1.png]]

Debes reutilizar el contador del apartado 1 y el registro de desplazamiento del apartado 2. La estructura interna del diseño es la de la figura:

![[assets/secuenciales/estrutura_tarea/estructura-luces.png]]

El nivel superior de la jerarquía debe ser un fichero Verilog que instancie el contador y el registro y que contenga el código del decodificador. Ten en cuenta que:

- El contador funciona como **divisor de frecuencia**: con el reloj de 50 MHz de la placa, su salida **TC** habilita el registro de desplazamiento de forma que haya un desplazamiento cada **0,25 s**.
- El registro de desplazamiento funciona como un **contador Johnson**, que genera los 14 estados del juego de luces. ¿De cuántos bits debe ser?
- Debes añadir **lógica de decodificación** que genere las 8 salidas de los LEDs a partir del contador Johnson. Puedes hacerlo con un bloque `always`.
- La habilitación del contador se controla con el interruptor **SW0** de la placa, para poder probar la pausa de la secuencia.

> [!question]- ¿Qué módulo debe tener el divisor y de cuántos bits debe ser el registro?
>> [!todo] 0,25 s / 20 ns = 12 500 000 ciclos, así que el divisor es de módulo 12 500 000 (`$clog2` da 24 bits). Un contador Johnson de *n* bits tiene 2*n* estados, así que para 14 estados el registro es de 7 bits.

### Verificación con testbench

Verifica el diseño mediante una simulación en ModelSim, con un testbench similar a los de los apartados 1 y 2.

> [!tip] Acelera la simulación sin tocar el diseño
> Si las luces cambian cada 0,25 s, la simulación tarda mucho. Conviene reducir el módulo del divisor solo en simulación. **Recomendamos (y valoraremos)** la técnica de la sección 2 de la práctica Tutorial: añadir un parámetro al nivel superior del diseño que permita simular e implementar en placa con valores distintos del divisor sin modificar el código.

El resultado de la simulación debería parecerse a esta captura:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png]]

Por defecto, ModelSim muestra solo las señales del nivel superior del testbench, no las internas del diseño ni de sus instancias (el contador y el registro). Siguiendo el procedimiento de la práctica Tutorial, añade las señales internas del contador y del registro al visor de ondas.

> [!warning] Entrega
> Incluye en el informe una captura del resultado similar a la siguiente (en la que solo se ven las señales del contador).

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5_modificada.png]]

### Verificación de un caso extremo

Una verificación exhaustiva debe comprobar también los casos extremos poco probables, y es tarea nuestra anticiparlos. Aquí, una situación que puede dar problemas es **desactivar la habilitación del sistema justo cuando TC (la salida del divisor) está activa**.

Modifica el testbench, si no lo has hecho ya, para incluir este caso y observa cómo se comporta el circuito. ¿Es el comportamiento esperado? Si no, ¿por qué ocurre? ¿Dónde está el problema? Visualiza en ModelSim las señales internas del contador y del registro para localizarlo y corrige el diseño. Si tienes que modificar el contador o el registro, vuelve a verificarlos con el testbench del apartado 1 o 2 para comprobar que siguen funcionando por separado.

> [!tip] Acceso a señales internas desde el testbench
> Con el operador `.` puedes leer señales internas de un módulo aunque no sean entradas ni salidas. Por ejemplo, para comprobar si la señal **TC** de la instancia `duv` vale 1:
> ```verilog
> if (duv.TC == 1) ...
> ```
> y para esperar a que tome ese valor:
> ```verilog
> wait (duv.TC == 1);
> ```

### Verificación en placa

Implementa el diseño en la placa DE2-115 y comprueba que funciona. Al crear el proyecto de Quartus debes haber seleccionado la FPGA de la placa, el modelo **EP4CE115F29C7** de la familia **Cyclone IV E**; si no, cámbialo en **Assignments > Device**.

Asigna también los pines, es decir, a qué pin de la FPGA se conecta cada entrada y salida, con el mismo procedimiento que en la práctica Tutorial. Las conexiones son:

| Señal | Elemento de la placa |
| --- | --- |
| **CLK** | Reloj de 50 MHz **CLOCK_50** |
| **RSTn** | Pulsador **KEY0** |
| **ENABLE** | Interruptor **SW0** |
| **LEDS** | LEDs verdes **LEDG0** a **LEDG7** |

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png]]

Recuerda que, tras asignar los pines, hay que volver a compilar el diseño antes de programarlo en la placa.

next > [[sdp/es/proyecto2-controlador-video|Proyecto 2: Diseño de un controlador de vídeo]]
