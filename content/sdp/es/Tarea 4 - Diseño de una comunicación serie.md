---
title: "Tarea 4: Diseño de una comunicación serie"
draft: false
tags:
  - verilog
  - comunicaciones
  - fsm
---

prev > [[Tarea 3 - Diseño de máquinas de estados finitos]]

*Por Ricardo José Colom Palero*

En esta tarea se diseña una **interfaz de comunicación serie** para comunicarse con una pantalla táctil y obtener las coordenadas del punto de la pantalla que se ha tocado.

> [!warning] Test previo
> Antes de abordar los diseños, estudia la información de esta página y responde al test correspondiente en PoliformaT.

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Objetivos/objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Objetivos

El objetivo de la práctica es aprender las características y el modo de uso de una pantalla táctil, que es la aplicación en la que se centra el diseño. Para ello hay que desarrollar e implementar una interfaz de comunicación serie como las que se usan habitualmente con los convertidores analógico-digitales. Habrá que profundizar en los conceptos de Verilog HDL orientados al diseño de elementos de control. La **metodología de verificación funcional** es muy importante en esta práctica, y se basará en el uso de modelos de comportamiento de una interfaz serie. Por último, se seguirá profundizando en la verificación física del diseño en el hardware.

## Pantalla táctil LTM

![[assets/Diseño de una Comunicación Serie/Pantalla Táctil LTM/Imagen042.png]]

En esta práctica se usa la pantalla táctil LTM fabricada por Terasic para las placas del programa universitario de Altera, como la DE2-115. Es una pantalla de 4,3 pulgadas con relación de aspecto 15:9 y resolución de 800 × 480 píxeles de 24 bits, capaz de representar unos 16 millones de colores. Dispone de un convertidor analógico-digital que captura el punto de contacto.

### Estructura de la pantalla táctil LTM

![[assets/Diseño de una Comunicación Serie/Estructura Pantalla Táctil LTM/Imagen043.png]]

En esta pantalla, la visualización y la captura del punto de contacto son totalmente independientes, lo que permite usar solo la captura del punto de contacto sin visualizar nada, como se hará en esta práctica. De la captura se encarga un convertidor analógico-digital (ADC).

### Características «touch»

El **AD7843** de Analog Devices es un ADC de **12 bits** que proporciona las coordenadas X e Y del punto de contacto. Estas coordenadas se leen a través de su interfaz serie.

![[assets/Diseño de una Comunicación Serie/Características _Touch_/Imagen044.png]]

Tanto la interfaz serie de la pantalla como la del ADC están conectadas a la FPGA a través del conector de 40 pines. Por la limitación de pines del conector, ambas comparten algunas señales: el mismo reloj (**ADC_DCLK**) y la misma habilitación (**SCEN**). Para que las comunicaciones no interfieran, la habilitación del ADC está negada mediante un inversor: cuando la pantalla LCD está habilitada (SCEN a nivel bajo) el ADC está deshabilitado, y viceversa.

Además de estas dos líneas compartidas, la interfaz serie del ADC tiene:

- **ADC_DIN**: entrada de datos, para enviar al ADC los comandos de control.
- **ADC_DOUT**: salida de datos, por donde el ADC envía en serie los 12 bits de la coordenada X o Y.
- **ADC_BUSY**: indica que el ADC está ocupado.
- **ADC_PENIRQ_n**: petición de interrupción que indica que se ha tocado la pantalla.

### Diagrama de temporización

![[assets/Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen047.png]]

La figura muestra el diagrama de temporización del protocolo de comunicación con el ADC para obtener la coordenada X o la Y. La **FPGA es el maestro** (*master*) de la comunicación y el ADC el esclavo (*slave*). Por tanto, la FPGA genera la selección **SCEN**, la señal **ADC_DIN**, con la que envía el comando de solicitud de coordenada, y **ADC_DCLK**, que fija la velocidad de la comunicación y sincroniza los bits de ADC_DIN y ADC_DOUT. El resto de señales las genera el ADC.

Aunque es la FPGA la que controla la comunicación, debe saber cuándo iniciarla: cuando algo toque la pantalla, cosa que el ADC indica mediante **ADC_PENIRQ_n**.

![[assets/Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen053.png]]

ADC_PENIRQ_n está normalmente a nivel alto y pasa a nivel bajo cuando se toca la pantalla con un lápiz o con el dedo. La FPGA debe vigilarla: cuando pase a nivel bajo, debe iniciar el protocolo de comunicación con el ADC para obtener las coordenadas.

El protocolo empieza activando **SCEN** y generando **ADC_DCLK** y **ADC_DIN** según el diagrama temporal. Por ADC_DIN se envía un comando de control que solicita la coordenada X o la Y; la tabla muestra los comandos de cada una. Como son distintos, hacen falta **dos comunicaciones**, una para cada coordenada. Cuando el ADC recibe el comando, hace la conversión y transmite en serie los 12 bits de la coordenada por ADC_DOUT, sincronizados con ADC_DCLK.

![[assets/Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen055.png]]

ADC_DIN debe permanecer a nivel bajo cuando no se usa para transmitir el comando. Además, aunque su nombre pueda confundir, **ADC_DCLK no es propiamente una señal de reloj**: en reposo está a nivel bajo y solo oscila durante la comunicación, marcando la velocidad y la sincronización de los bits. Una secuencia de transmisión y recepción de una coordenada dura **24 periodos de ADC_DCLK**, con un periodo máximo de 0,1 ms y mínimo de 0,5 µs, es decir, una velocidad de entre **10 kbps y 2 Mbps**.

![[assets/Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen054.png]]

## Planteamiento de la tarea

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Estructura%20de%20la%20Tarea/indice.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

La práctica consiste en diseñar una interfaz de comunicación serie. En este caso se aplica a una pantalla táctil: el diseño debe controlar el ADC que captura dónde se ha puesto un puntero o el dedo.

Se divide en **dos subtareas**: la primera es el diseño de la interfaz serie con el ADC y su verificación mediante simulación con un testbench proporcionado por los profesores; la segunda, probar el diseño en el hardware, comunicándose con la pantalla táctil y mostrando el punto de contacto en los displays de 7 segmentos.

## Subtarea 1: Interfaz serie con el ADC

![[assets/Diseño de una Comunicación Serie/Subtarea 1: Interface Serie del Convertidor ADC/Imagen045.png]]

Diseña la interfaz de comunicación serie con el ADC para obtener las coordenadas X e Y del punto de contacto. El diseño debe ajustarse a la temporización del AD7843 vista anteriormente. El bloque tendrá una entrada de reloj para el oscilador de 50 MHz, un reset activo a nivel bajo, las señales de comunicación con el ADC y dos buses de salida de 12 bits con las coordenadas X e Y.

> [!note] Dos velocidades distintas
> El diseño funciona con un reloj de **50 MHz**, mientras que la comunicación debe ir a una velocidad de entre **10 kbps y 2 Mbps**.

### Sugerencia: contador de semiciclos

![[assets/Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen048.png]]

Se puede usar un contador que lleve la cuenta de los **semiperiodos** necesarios para completar la secuencia de transmisión y recepción: en total **48 cuentas**, correspondientes a los semiperiodos de los 24 periodos de ADC_DCLK. Los cambios de cuenta sirven para generar ADC_DCLK y ADC_DIN y para capturar los bits recibidos por ADC_DOUT.

![[assets/Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen056.png]]

Fíjate especialmente en el instante en que se ponen los bits en **ADC_DIN**: deben cambiar al cambiar la cuenta del contador, coincidiendo con el **flanco de bajada** de ADC_DCLK. Por ejemplo, el bit A0 se pone en el cambio de la cuenta 5 a la 6 y dura las cuentas 6 y 7. El contador de semiperiodos es, por tanto, una buena referencia para generar tanto ADC_DCLK como ADC_DIN.

![[assets/Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen057.png]]

Los bits que envía el ADC por **ADC_DOUT** deben capturarse en el **punto medio** de cada bit, que es donde la línea está más estable: por ejemplo, el bit 9 en el cambio de la cuenta 22 a la 23 y el bit 8 entre las cuentas 24 y 25. La captura coincide con el **flanco de subida** de ADC_DCLK, aunque la referencia sean las cuentas del contador.

### Sugerencia: concatenación de las secuencias

![[assets/Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen058.png]]

Para obtener las dos coordenadas hay que hacer dos secuencias consecutivas de transmisión y recepción. Sin embargo, en cada secuencia hay tiempos de espera, así que se pueden eliminar **concatenando** las dos secuencias.

![[assets/Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen059.png]]

En el diagrama, la solicitud de la coordenada Y empieza cuando todavía se está recibiendo la X. Es posible porque las líneas de transmisión y recepción son independientes y se aprovecha el tiempo de espera del ADC. Así, la secuencia completa para las dos coordenadas dura solo **80 semiperiodos**.

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Sugerencia%2C%20concatenaci%C3%B3n/Temporizacion_Tactil01.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

### Propuesta de estructura del diseño

Tomando como referencia la concatenación de las dos secuencias, se puede usar como propuesta el diagrama de bloques siguiente. Todos los bloques usan el reloj de 50 MHz y la señal de reset.

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Propuesta%20estructura%20dise%C3%B1o/Diagrama_bloques_bi/Diagrama_bloques_bi.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

- A la izquierda, un contador de módulo **ADC_DCLK_CNT** (un parámetro) que fija la velocidad de transmisión entre 10 kbps y 2 Mbps. Además del fin de cuenta (TC), genera una señal que se activa a **mitad de la cuenta** (TC/2).
- En el centro, el contador de **módulo 80**, referencia de los 80 semiperiodos de la secuencia completa.
- Abajo, en amarillo, el **generador de ADC_DCLK**, que usa el fin de cuenta del primer contador.
- A la derecha, el **generador de ADC_DIN**, que depende de la cuenta de semiperiodos, y el bloque de **captura de ADC_DOUT**, que usa la cuenta de semiperiodos y, como habilitación, la señal de mitad de cuenta del primer contador.
- Arriba, una **máquina de estados** que controla todo el diseño generando las habilitaciones necesarias. Es la que inicia la secuencia a partir de **ADC_PENIRQ_n** y genera la selección **SCEN**.

En esta propuesta no se usa la línea **ADC_BUSY**.

### Propuesta de máquina de estados

La máquina de estados que gestiona el protocolo no es única y puede hacerse de muchas formas. Esta es una propuesta; los dos diagramas representan la misma máquina con distinta notación (ASM y diagrama de estados).

![[assets/Diseño de una Comunicación Serie/Propuesta FSM/Imagen060.png]]

Se trata de una máquina de cuatro estados:

- **S0**: estado inicial tras el reset. Es transitorio y sirve para inicializar las señales.
- **S1**: espera a que se toque la pantalla. Se mantiene mientras ADC_PENIRQ_n vale 1 y, cuando pasa a 0, cambia a S2.
- **S2**: inicia el protocolo activando las habilitaciones (de los contadores) y el *chip select* del ADC. Se mantiene hasta obtener las coordenadas X e Y, es decir, hasta completar los 80 semiperiodos de ADC_DCLK que marca el contador de módulo 80.
- **S3**: estado de transición que termina el protocolo e indica su final con la señal **Fin_Trans**.

### Verificación del diseño

![[assets/Diseño de una Comunicación Serie/Verificación del Diseño/Imagen061.png]]

Una vez descrita en Verilog HDL la interfaz, y sin errores de compilación, hay que hacer la verificación funcional, es decir, simularla para comprobar que funciona correctamente.

Simular la comunicación con el ADC generando las señales a mano sería complicado. Por eso se usa un **modelo funcional de la pantalla táctil** que emula la comunicación del ADC, **EMULE_ADC.vo**. La verificación se hace en ModelSim con un entorno de verificación escrito en Verilog HDL.

Para facilitarlo se ha preparado el proyecto de Quartus [[assets/Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Touch_alumno.qar|Touch_alumno.qar]], ya configurado y con todos los archivos necesarios. Incluye el archivo **ADC_CONTROL.v**, la interfaz que hay que diseñar, vacío salvo por los puertos del módulo.

#### Testbench

El entorno de verificación de Touch_alumno.qar tiene la estructura de la imagen. El testbench **tb_Touch_Control.v** es una descripción estructural que conecta el bloque que se verifica, **ADC_CONTROL.v**, con el emulador de la pantalla, **EMULE_ADC.vo**. Ambos están rodeados por **MFB.v**.

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Verificaci%C3%B3n%20del%20Dise%C3%B1o/Diagrama_verificacion_bi/Diagrama_verificacion_bi.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

MFB genera el reloj y el reset. Después simula que se ha tocado la pantalla: da unas coordenadas X e Y al emulador y activa **NEW_COORD** para que empiece la emulación. El emulador pone a nivel bajo ADC_PENIRQ_n, a lo que ADC_CONTROL debe responder iniciando el protocolo; el emulador le envía entonces las coordenadas que le dio MFB.

Cuando ADC_CONTROL obtiene las coordenadas, MFB las compara con las que dio al emulador y escribe en la consola de ModelSim si la verificación es correcta o ha fallado.

#### Procedimiento

![[assets/Diseño de una Comunicación Serie/Procedimiento/Imagen035.png]]

1. Descarga y descomprime el proyecto Touch_alumno.qar.
2. Diseña la interfaz en el archivo **ADC_CONTROL.v**, que ya incluye los puertos del módulo. Este módulo debe ser siempre el **Top** de la jerarquía, porque es el diseño que se sintetiza en la FPGA. Los archivos tb_Touch_Control.v, MFB.v y EMULE_ADC.vo solo se usan para simular: no forman parte del diseño ni son sintetizables.
3. Compila el diseño sin errores.
4. Lanza la simulación con **Tools > Run Simulation Tool > RTL Simulation**. El proyecto ya está configurado, así que no hay que ajustar nada.

![[assets/Diseño de una Comunicación Serie/Procedimiento/Imagen036.png]]

#### Comprobación

![[assets/Diseño de una Comunicación Serie/Comprobación/Imagen033.png]]

Al lanzar la simulación se abre ModelSim. A la izquierda se ve la jerarquía del testbench y a la derecha las formas de onda de la interfaz con el ADC.

La simulación se ejecuta automáticamente. Si el diseño funciona, en la consola aparece el mensaje «**Verificación del DUV correcta**».

![[assets/Diseño de una Comunicación Serie/Comprobación/Imagen034.png]]

Si no, puede ocurrir que:

1. **La simulación no empieza**, porque ModelSim ha detectado en ADC_CONTROL un error que Quartus había dejado pasar. Hay que volver a Quartus, corregirlo y relanzar la simulación.
2. **La simulación empieza pero nunca termina**, porque ADC_CONTROL no funciona bien: normalmente el protocolo no termina porque sus señales no vuelven a los valores de reposo.
3. **La simulación termina con «Error de Transmisión»**, porque las coordenadas recibidas no coinciden con las enviadas.

Cuando ADC_CONTROL supere esta simulación inicial, amplía la verificación con otros casos. Modifica **tb_Touch_Control.v** para añadir un segundo caso con **tres comunicaciones consecutivas de tres datos distintos, sin activar el reset entre ellas**. Añádelo a partir de la línea 137, donde pone «CASO 2», tomando como referencia las líneas del «CASO 1» pero **sin usar** la función `MFB.reset`.

Cuando la verificación sea correcta, pasa a la verificación física de ADC_CONTROL.

## Subtarea 2: Visualización del punto de contacto

![[assets/Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen052.png]]

La segunda subtarea es la verificación física del diseño anterior: probar ADC_CONTROL en la placa DE2-115 con la pantalla táctil de Terasic, obteniendo las coordenadas X e Y del punto tocado y mostrándolas en los **displays de 7 segmentos** en **hexadecimal**, con 12 bits por coordenada. La imagen muestra el valor de las coordenadas en cada esquina de la pantalla.

![[assets/Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen046.png]]

Necesitarás un **conversor de hexadecimal a 7 segmentos** que traduzca las coordenadas de ADC_CONTROL para mostrarlas en los displays.

Por supuesto, hay que asignar los pines adecuados para conectar con la pantalla y probar el diseño en la placa:

![[assets/Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.53.png]]

![[assets/Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.32.44.png]]

### Verificación física del diseño

Una vez configurada la placa, la primera prueba que se suele hacer es tocar la pantalla y comprobar que los displays muestran las coordenadas. Funcione o no, lo correcto es comprobar la comunicación serie observando las señales con un **analizador lógico**. Quartus incluye uno, **SignalTap**, que se integra en el diseño y permite ver las señales internas de la FPGA.

<!-- PoliformaT: vídeo de ejemplo de uso de SignalTap (no exportado) -->

Como condición de disparo para capturar la comunicación se puede usar el flanco de bajada de ADC_PENIRQ_n o que el contador de semiperiodos tome un valor concreto, por ejemplo 5. Ambas permiten obtener una captura como esta:

![[assets/Diseño de una Comunicación Serie/SignalTap/datos02.jpg]]

Como se ve, no solo se capturan las entradas y salidas, sino también el contador que sincroniza la comunicación.

> [!warning] Entrega
> Haz una captura similar que demuestre el correcto funcionamiento del diseño e inclúyela en la memoria. En la esquina superior izquierda aparecen la fecha y la hora de la captura de SignalTap, que deben coincidir con los archivos del proyecto de Quartus entregado.

En el ejemplo anterior solo se ve un toque. A veces interesa capturar varios, pero eso exigiría mucha memoria. Sin embargo, cada bit de la transmisión dura muchas muestras, cuando con un par bastaría para saber qué dato se ha recibido. SignalTap se puede configurar para no almacenar todas las muestras, sino solo algunas (*storage qualifier*), y así capturar cientos de toques con la misma memoria.

<!-- PoliformaT: vídeo de configuración del almacenamiento selectivo de SignalTap (no exportado) -->

La imagen muestra una captura con esa configuración, detenida tras 6 o 7 toques para no alargar la adquisición:

![[assets/Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_a.jpg]]

Ampliando la imagen se ve que hay varias capturas del punto de toque y que cada cuenta del contador parece durar un solo ciclo de reloj: simplemente no se guarda toda la información capturada.

![[assets/Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_b.jpg]]

### Comprobación y mejora del diseño

Una vez comprobada la comunicación serie, termina la verificación comprobando los valores de los displays, teniendo en cuenta que:

**Las esquinas son difíciles de alcanzar.** Es prácticamente imposible ver en el display las coordenadas 12'h000 o 12'hFFF, porque la superficie de toque es muy pequeña en comparación con la resolución táctil y por la limitación del marco de metacrilato. No te preocupes si no alcanzas los valores teóricos del fabricante.

**La última lectura al soltar puede ser errónea.** Con el dedo apoyado, las coordenadas son estables y aproximadamente correctas, y al arrastrarlo cambian de acuerdo con el movimiento. Pero al dejar de tocar, el último valor cambia y muestra una coordenada que no tiene que ver con la última posición (a veces solo cambia una de ellas). Se debe a que mientras se toca, el ADC lee continuamente, y al soltar todavía hace una última lectura cuando el dedo ya no toca, con lo que cambia el valor resistivo del punto. Se puede solucionar ajustando dos parámetros:

1. **La velocidad de comunicación.** Puede estar entre 10 kbps y 2 Mbps; en el diseño propuesto la fija el parámetro **ADC_DCLK_CNT**, inicialmente en unos 70 kbps. Variándolo se puede minimizar el efecto, aunque puede no bastar y haya que combinarlo con el siguiente ajuste.
2. **Una pausa entre dos adquisiciones consecutivas**, para que el ADC no convierta continuamente. Al tocar la pantalla se adquieren las coordenadas, y no se hace una nueva comunicación hasta que pase al menos **medio segundo**, aunque el dedo siga tocando. Así hay menos lecturas y se evitan las erróneas. El inconveniente es que hay que modificar ligeramente el diseño para añadir un elemento que genere esa espera, de medio segundo o de un valor ajustable.

<iframe src="/static/animaciones/Dise%C3%B1o%20de%20una%20Comunicaci%C3%B3n%20Serie/Verificaci%C3%B3n%20y%20Mejora%20del%20Dise%C3%B1o/Diagrama_bloques_mejora_bi/Diagrama_bloques_mejora_bi.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Para reducir el número de lecturas se propone añadir al diseño un contador de **módulo 25 000 000**, que con el reloj de 50 MHz introduce un retardo de medio segundo entre una lectura y la siguiente. Está en la parte inferior izquierda del nuevo diagrama de bloques.

Este contador obliga a modificar la máquina de estados de ADC_CONTROL. Lo ideal es añadir un estado de espera **S4** tras terminar la comunicación y obtener las coordenadas. En S4 la máquina habilita el contador y permanece en ese estado hasta su fin de cuenta, de modo que no se hace otra comunicación hasta que pasa el medio segundo.

El diagrama de bloques muestra las entradas y salidas adicionales que necesita la máquina, y la figura muestra el diagrama de estados con el nuevo estado.

![[assets/Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Imagen065.png]]

Después, ajusta el módulo del contador para obtener el retardo más adecuado según la velocidad de transmisión.

next > [inicio](sdp/es/index)
