---
title: "Tarea 1: Diseño de sistemas secuenciales"
draft: false
tags:
  - verilog
  - secuenciales
---

prev > [[sdp/es/crear-qar|Crear QAR]]

*Por Ricardo José Colom Palero*

En esta tarea se plantean las bases para el desarrollo de la primera práctica de la asignatura, en la que se aborda el diseño de sistemas digitales secuenciales mediante lenguajes de descripción hardware, en concreto **Verilog HDL**.

> [!warning] Test previo
> Antes de empezar la tarea hay que realizar en PoliformaT el test sobre sintaxis de Verilog HDL, que sirve para evaluar los conocimientos previos.

<iframe src="../../static/animaciones/secuenciales/objetivos/Objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Objetivos

El objetivo fundamental de esta tarea es aprender los conceptos básicos del lenguaje Verilog HDL y su uso en la realización de diseños, con especial atención a los bloques procedurales gobernados por el reloj para el modelado de circuitos secuenciales.

Se diseñarán elementos digitales en Verilog HDL, avanzando en el uso de la jerarquía y de los parámetros. Por último, se pondrá énfasis en la verificación del funcionamiento de los diseños mediante simulaciones que permitan comprobar de forma exhaustiva que son correctos.

## Estructura de la tarea

<iframe src="../../static/animaciones/secuenciales/estrutura_tarea/Estructura_Tarea.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Todo sistema secuencial está gobernado por una señal de reloj, que procede de un oscilador externo al dispositivo en el que se implementa el diseño. El oscilador de la placa DE2-115 tiene una frecuencia de **50 MHz**, es decir, un periodo de **20 ns**. Cuando se diseñan circuitos que controlan elementos de visualización, hay que tener en cuenta que el ojo humano no percibe cambios que duren menos de unos 50 ms. Por tanto, no se puede usar directamente el reloj de 50 MHz para producir cambios que deban ser visibles, como hacer parpadear un LED.

En esta práctica se ve cómo resolver este problema manteniendo los criterios de un diseño síncrono correcto: **todos los flip-flops del diseño deben estar gobernados por la misma señal de reloj**.

La práctica se estructura en tres subtareas:

1. Diseño de un contador parametrizable.
2. Diseño de un registro de desplazamiento.
3. Integración de los diseños anteriores para realizar el juego de luces del coche fantástico.

## Subtarea 1: Diseño de un contador parametrizable

![[assets/secuenciales/estrutura_tarea/imagen02.png]]

Describe en Verilog HDL un contador binario con las siguientes características:

- Contador síncrono ascendente/descendente de módulo parametrizable `fin_cuenta`.
- Funcionamiento por flanco de subida del reloj.
- Reset síncrono (máxima prioridad), activo a nivel bajo.
- Entrada de habilitación **enable**, activa a nivel alto, que habilita la cuenta.
- Si la entrada **UP_DOWN** está a nivel alto el contador cuenta hacia arriba; si no, cuenta hacia abajo.
- Salida **TC** (*Terminal Count*), activa cuando el contador llega al fin de cuenta.
- Dispositivo de la familia Cyclone IV E de Intel FPGA.

Verifica su funcionamiento mediante una simulación que contemple todas las combinaciones posibles de las señales de entrada y recorra completamente los valores de las salidas.

### Parametrización

Un diseñador eficiente debe aprovechar el tiempo que dedica a sus diseños, y para ello es importante reutilizar módulos ya diseñados. Una característica de los lenguajes HDL que facilita la reutilización es la **parametrización**. Por ejemplo, si ya tenemos un contador de 8 bits y necesitamos uno de 10, la solución inmediata es copiar la descripción y modificarla, pero así acabamos con una colección de archivos distintos para cada tamaño.

La mejor solución es tener **un solo archivo** con el modelo del contador, escrito en función de un parámetro de configuración que se cambia según las necesidades.

A veces hay que hacer operaciones matemáticas con el parámetro antes de usarlo. Por ejemplo, ¿cómo se obtiene el número de bits del contador a partir de su módulo? La solución es usar una función. La figura muestra cómo hacerlo con la función `CLogB2`, que calcula el logaritmo en base 2 **redondeado al entero superior**, es decir, el número de bits necesarios para alcanzar el fin de cuenta. `CLogB2` está definida en el fichero de funciones matemáticas [[assets/secuenciales/estrutura_tarea/mathfun.vh|MathFun.vh]], que hay que incluir en el diseño.

![[assets/secuenciales/estrutura_tarea/imagen08.png]]

### Verificación del diseño

![[assets/control-pantalla/verificacion-del-diseno/imagen061.png]]

Una vez descrito en Verilog HDL el módulo `count`, hay que verificar mediante simulación que el contador funciona correctamente y que genera bien la cuenta y la señal de fin de cuenta.

Para ello se usa un simulador profesional, **ModelSim-Altera**, que necesita un **testbench**: un archivo, escrito también en Verilog HDL, que describe los estímulos de entrada de la simulación. Como aún no tienes experiencia escribiendo testbenches, sigue los pasos que se describen a continuación.

#### Comprobar la configuración de Quartus

Antes de simular, comprueba que la ruta de instalación de ModelSim-Altera está bien configurada en Quartus. En **Tools > Options…**, selecciona **General > EDA Tool Options** en la columna **Category**. En la lista de herramientas, la ruta de ModelSim-Altera debe ser `C:\intelFPGA\17.1\modelsim_ase\win32aloem` o equivalente.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2019-12-16-a-las-17.25.53.png]]

#### Creación de los estímulos con Verilog HDL

Los estímulos de la simulación se describen en el propio Verilog HDL. En **File > New** selecciona **Verilog HDL File** y escribe el código siguiente.

Como es código de verificación, su función es generar los estímulos; por eso el `module` no tiene entradas ni salidas: genera internamente las entradas y las inyecta al bloque que se verifica, el DUT (*Device Under Test*). En este caso el DUT es el módulo `count`, que se instancia dentro del testbench para conectarle las entradas generadas y recoger sus salidas.

```verilog
// Autor: Ricardo José Colom Palero
// Fecha: 10 de diciembre de 2018

`timescale 1ns/1ps

module tb_count ();

localparam T = 20;

reg CLK, RST_n;
reg ENABLE, UP_DOWN;
wire [4:0] COUNT;
wire TC;

// Instanciación del DUT (Device Under Test)
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
  $display("SIMULANDO!!!");
  #(T*2)
  RST_n = 1'b1;
  #(T*2)
  ENABLE = 1'b1;
  UP_DOWN = 1'b1;
  #(T*24)
  $display("Fin Simulacion!!!");
  $stop;
end

always
begin
  #(T/2) CLK <= ~CLK;
end

endmodule
```

Guárdalo con **File > Save as...** con el nombre `tb_count.v`. Este archivo **no debe compilarse** con el resto del proyecto: no forma parte del diseño que se configura en la FPGA, solo se usa para la verificación.

A continuación configura la simulación para que encuentre el archivo de estímulos. En **Assignments > Settings**, selecciona **Simulation** en la columna izquierda:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.02.png]]

Pulsa el botón **Test Benches...**, a media altura en el margen derecho. Se abre una nueva ventana...

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.11.png]]

...en la que hay que pulsar **New** para añadir un testbench nuevo, configurado como en la imagen:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.28.34.png]]

Vuelve aceptando con **OK** en cada ventana.

Solo queda lanzar la simulación con ModelSim-Altera mediante **Tools > Run Simulation Tool > RTL Simulation**, que simula el código RTL antes de la síntesis y la implementación.

![[assets/control-pantalla/realizar-la-simulacion/imagen116.png]]

Se abre ModelSim-Altera y comienza la simulación descrita en el testbench. En este caso se detiene al llegar al `$stop`, unos 24 ciclos de reloj después de habilitar la cuenta, de modo que se ve cómo el contador evoluciona desde 0 hasta 19 y vuelve a 0.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.33.02.png]]

> [!warning] Revisa siempre la ventana *Transcript*
> ModelSim también da errores si el testbench no compila. Revisa siempre la ventana *Transcript*, en la parte inferior, para ver errores y *warnings*. En la captura siguiente, por ejemplo, el error se debe a haber escrito mal el nombre del módulo contador.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-26-ene.png]]

#### El simulador ModelSim-Altera

ModelSim-Altera tiene varias ventanas. En la parte inferior está la ventana de mensajes, donde el simulador informa, por ejemplo, de los errores detectados en los archivos Verilog HDL del diseño. Conviene revisarla, porque un error en los archivos impide cargar el proyecto y, por tanto, simular.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_general.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

A la izquierda está el visor de jerarquía, que muestra la estructura del diseño y todos sus archivos. En la parte central superior está el visor de señales, con las señales del módulo seleccionado en la jerarquía. Estas señales se pueden añadir al visor de ondas, a la derecha, donde se muestra el resultado de la simulación. Todas las ventanas de ModelSim se pueden desacoplar y mostrar por separado, lo que es especialmente útil con el visor de ondas.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_desacoplo.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Las lupas del menú superior permiten hacer zoom sobre los resultados.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.09.20.png]]

Inicialmente ModelSim-Altera simula hasta encontrar el `$stop` del testbench. Se muestran todas las señales y se ve la cuenta del contador en binario.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.39.47.png]]

Se puede cambiar la representación de una señal: por ejemplo, para ver el contador en decimal sin signo, haz clic derecho sobre la señal y en **Radix** elige **Unsigned**.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.45.40.png]]

En la barra de menú están los botones de simulación. De izquierda a derecha: **Restart** reinicia la simulación (útil cuando se añaden señales al visor de ondas y hay que volver a simular); a continuación está la casilla con el tiempo de simulación y, a su lado, el botón **Run**, que simula durante ese tiempo; el último botón, **Stop**, detiene la simulación.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_tiempo.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Para repetir la simulación pulsa **Restart** y después **Run -All**: la simulación se detendrá en el `$stop` del testbench. Estas operaciones también se pueden hacer escribiendo los comandos en la ventana de mensajes. También se puede fijar un tiempo, por ejemplo 300 ns, y pulsar **Run**: la simulación se detendrá a los 300 ns, porque ese instante es anterior al `$stop`.

<iframe src="../../static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_restart.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

#### Comprobación de resultados

Tras la primera simulación, modifica el testbench para hacer una simulación completa del contador en la que se vean todos sus casos de funcionamiento. Como sugerencia, sincroniza los cambios de las señales de entrada con los flancos del reloj. La imagen muestra un ejemplo de simulación con el contador funcionando en modo ascendente y descendente.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png]]

> [!question] ¿Has evaluado todos los casos posibles de funcionamiento del contador?
> Reset con y sin *enable*, cuenta ascendente y descendente, paso por el fin de cuenta en ambos sentidos y cambio de sentido a mitad de cuenta.

## Subtarea 2: Diseño de un registro de desplazamiento

![[assets/secuenciales/estrutura_tarea/imagen04.png]]

Describe en Verilog HDL un registro de desplazamiento con las siguientes características:

- Registro de desplazamiento síncrono de 7 bits.
- Reloj activo por flanco de subida.
- Reset síncrono, activo a nivel bajo.
- Entrada serie.
- Salida serie.
- Salida paralelo.
- Entrada de habilitación **enable**, que permite el desplazamiento.
- Dispositivo de la familia Cyclone IV E de Intel FPGA.

Verifica su funcionamiento mediante una simulación que contemple todas las combinaciones posibles de las señales de entrada y recorra completamente los valores de las salidas.

## Subtarea 3: Juego de luces del coche fantástico

Realiza en los LEDs verdes LEDG7 a LEDG0 de la placa DE2-115 el siguiente juego de luces:

![[assets/secuenciales/estrutura_tarea/imagen06.png]]

En este diseño debes reutilizar el contador parametrizable de la subtarea 1 y el registro de desplazamiento de la subtarea 2, con las siguientes consideraciones:

- El contador, que cuenta con el reloj de 50 MHz de la placa, se usa para habilitar con su salida **TC** el *enable* del registro de desplazamiento, de forma que haya un desplazamiento cada **0,25 s**.
- El registro de desplazamiento debe funcionar como un **contador Johnson**, que genera 14 estados correspondientes a los 14 pasos del juego de luces.
- Además debes crear un **decodificador** que, a partir del estado del contador Johnson, genere la salida a los LEDs LEDG7 a LEDG0.
- El *enable* del contador se controla con el interruptor **SW[0]** de la placa.

El nivel superior de la jerarquía debe ser un fichero Verilog HDL que instancie el contador y el registro de desplazamiento y que contenga el código del decodificador.

![[assets/secuenciales/estrutura_tarea/imagen05.png]]

> [!question]- ¿Qué valor de `fin_cuenta` hay que usar para desplazar cada 0,25 s?
>> [!todo] Con un reloj de 50 MHz (20 ns), 0,25 s / 20 ns = 12 500 000 ciclos, así que `fin_cuenta = 12_500_000` y `CLogB2` da un contador de 24 bits.

### Verificación con testbench

Verifica el diseño mediante una simulación en ModelSim. Para ello crea un testbench de forma similar a las subtareas 1 y 2.

> [!tip] Acelera la simulación
> Para que la simulación sea más rápida, reduce el módulo del contador que temporiza las luces. Por ejemplo, usa un valor que actualice las luces cada 0,25 ms en lugar de cada 0,25 s.

El resultado de la simulación debería parecerse a esta captura:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png]]

El diseño es jerárquico y contiene instancias de un contador y de un registro de desplazamiento. Sin embargo, en la simulación solo vemos las señales del nivel superior del testbench, no las señales internas de estos submódulos. A menudo querremos verlas, sobre todo para depurar un diseño que no funciona. Veamos cómo hacerlo.

Se usan las dos subventanas de la parte izquierda de ModelSim: *Structure* y *Objects*. En la primera se puede desplegar la jerarquía completa del testbench y del diseño, con el nombre de cada módulo y el de cada instancia. En la imagen, el testbench **tb_lights** contiene una instancia del diseño **lights** llamada `i1`. A su vez, **lights** contiene una instancia del contador **contador** llamada `the_counter` y una del registro **shift7** llamada `the_shiftreg`.

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-2.png]]

Al seleccionar una instancia en la jerarquía, la ventana *Objects* muestra todas las señales definidas en ese módulo. Selecciona las que te interesen, haz clic derecho y elige **Add Wave** para añadirlas a la ventana de formas de onda (*Wave*):

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-3.png]]

Aunque las señales ya aparecen en la ventana *Wave*, todavía no se ven sus formas de onda: no estaban en la ventana cuando se lanzó la simulación, así que ModelSim no las registró. Para verlas hay que volver a simular desde ModelSim (¡sin cerrar la ventana!) con los botones **Restart** y **Run -All**, en este orden:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-4.png]]

**Restart** devuelve la simulación al instante inicial (t = 0) y **Run -All** la ejecuta de nuevo hasta el `$stop` del testbench. El resultado es el de la captura, donde por fin se ven las señales internas del contador:

![[assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5.png]]

> [!warning] Entrega
> Haz lo mismo para ver las señales internas del registro de desplazamiento y añade una captura de pantalla a la entrega de la tarea.

### Verificación en placa

Verifica el diseño en la placa DE2-115. Para ello hay que seleccionar el dispositivo (FPGA) de la placa y asignar los pines entre el diseño y la FPGA.

El dispositivo se selecciona en **Assignments > Device...**: elige el **EP4CE115F29C7** de la familia Cyclone IV E.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-17-a-las-10.14.49.png]]

La asignación de pines consiste en indicar a qué pin de la FPGA se conecta cada entrada y salida del diseño. Primero hay que identificar las entradas y salidas del diseño y los pines que les corresponden. La tabla recoge la información necesaria:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png]]

Los pines se asignan en **Assignments > Pin Planner**. En la parte superior de la ventana se ve el encapsulado del dispositivo desde abajo: los 780 pines de la Cyclone IV se distribuyen en una matriz cuadrada cuyas filas se identifican con letras y las columnas con números. En la parte inferior aparece la lista de entradas y salidas del diseño con su nombre (**Node Name**), dirección (**Direction**), ubicación (**Location**) y otros datos. En la columna **Location** se indica el pin al que se conecta cada señal. Por ejemplo, el reloj del sistema (`CLOCK_50`) va al oscilador de 50 MHz, que según la tabla está conectado al pin Y2 de la FPGA, así que en su columna **Location** se escribe `PIN_Y2`.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-16-a-las-17.18.47.png]]

Tras asignar los pines, cierra la ventana y vuelve a compilar con **Processing > Start Compilation**. La nueva compilación tendrá en cuenta los pines asignados.

La verificación final en la placa se hace configurando la Cyclone IV en modo **JTAG**. Conecta la alimentación de la placa (¡asegúrate de que está enchufada!) y abre el programador con **Tools > Programmer**.

Si el modo **JTAG** no está seleccionado en **Mode**, selecciónalo. Si el USB-Blaster no aparece por defecto, pulsa **Hardware Setup** y selecciónalo. En la lista debe aparecer un fichero de configuración `.sof` con el mismo nombre que el proyecto de Quartus; si no, añádelo con **Add**. Marca la casilla **Program/Configure**.

La ventana del programador debe quedar como en la imagen. Pulsa **Start** para configurar la FPGA y comprueba el juego de luces en la placa.

![[assets/secuenciales/estrutura_tarea/captura-de-pantalla-2020-03-04-a-las-10.12.34.png]]

next > [[sdp/es/tarea2-control-pantalla|Tarea 2 - Control y visualización en una pantalla]]
