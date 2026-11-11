---
title: "Proyecto 4: Diseño de un interfaz para pantalla táctil"
draft: false
tags:
  - verilog
  - comunicacion-serie
  - signaltap
---

prev > [[sdp/es/proyecto3-luces-fsm|Proyecto 3: Diseño de un juego de luces mejorado]]

En este proyecto se retoma la pantalla táctil de la placa DE2-115 y se implementa la **detección de la posición de toque**. Para ello se diseña un interfaz de comunicación serie con el convertidor analógico-digital externo que lee dicha posición. Se termina con una verificación física del diseño mediante el analizador lógico integrado **SignalTap**, para comprobar que el convertidor se comporta según lo previsto.

## Objetivos

- Comprender el funcionamiento de un interfaz serie.
- Diseñar interfaces de comunicación.
- Diseñar sistemas basados en *controlpath* y *datapath*.
- Realizar *testbenches* basados en modelos funcionales.
- Verificar circuitos en funcionamiento usando SignalTap.

## Tareas a realizar

- **Apartado 1:** circuito (ADC_CONTROL), verificación con el *testbench* proporcionado y modificación del *testbench* con los casos extra solicitados.
- **Apartado 2:** circuito con la decodificación a 7 segmentos, prueba en placa y pruebas con SignalTap (captura de un punto y captura de varios puntos).
- **Apartado 3:** circuito, verificación con el *testbench* proporcionado y prueba en placa.
- **Informe del proyecto**, incluyendo los resultados del *RTL Viewer* y del *State Machine Viewer*, el informe de *warnings* de análisis/síntesis y el test comentado.

## Introducción

### Lectura de la posición de contacto

![[assets/diseno-de-una-comunicacion-serie/pantalla-tactil-ltm/imagen042.png]]

Se utiliza la misma pantalla táctil que en el [[sdp/es/proyecto2-controlador-video|Proyecto 2]]. En ella, la visualización y la captura del punto de contacto son totalmente independientes, lo que permite usar solo la captura sin visualizar nada en la pantalla, como se hace en este proyecto.

![[assets/diseno-de-una-comunicacion-serie/estructura-pantalla-tactil-ltm/imagen043.png]]

La captura del punto de contacto corre a cargo de un convertidor analógico-digital (**ADC**) conectado a la pantalla, el **AD7843** de Analog Devices, de **12 bits**. El ADC obtiene las coordenadas X e Y del punto tocado, cada una con 12 bits, y dispone de un interfaz serie a través del cual se leen sus valores.

![[assets/diseno-de-una-comunicacion-serie/caracteristicas-_touch_/imagen044.png]]

La conexión con la pantalla incluye dos interfaces serie: uno para la pantalla (visualización) y otro para el ADC (punto de contacto). Ambos llegan a la FPGA a través de un conector de expansión de 40 pines y, por la limitación de pines, comparten algunas señales: el mismo reloj (**ADC_DCLK**) y la misma habilitación (**SCEN**). Para que la comunicación con un dispositivo no interfiera con la del otro, la habilitación del ADC pasa por un inversor: cuando la pantalla LCD está habilitada (SCEN a nivel bajo) el ADC está deshabilitado, y viceversa.

Además de estas dos líneas compartidas, el interfaz serie del ADC tiene:

- **ADC_DIN**, línea de entrada de datos para enviar al ADC comandos de gestión y control;
- **ADC_DOUT**, línea de salida de datos por la que el ADC envía en serie los 12 bits de cada coordenada;
- **ADC_BUSY**, que el ADC usa para indicar que está ocupado;
- **ADC_PENIRQ_n**, petición de interrupción que el ADC genera cuando se toca la pantalla.

### Diagrama de temporización

![[assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen047.png]]

La figura muestra el diagrama de temporización del protocolo de comunicación con el ADC para obtener la coordenada X o la Y. La FPGA inicia la comunicación como **maestro** y el ADC actúa como **esclavo**. La FPGA genera la selección **SCEN**, la señal **ADC_DIN** con el comando que solicita la coordenada y la señal **ADC_DCLK**, que fija la velocidad de la comunicación y sincroniza los bits de ADC_DIN y ADC_DOUT. El resto de señales (ADC_DOUT, ADC_PENIRQ_n y ADC_BUSY) las genera el ADC y las lee la FPGA.

![[assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen053.png]]

Aunque la FPGA controla la comunicación, necesita saber cuándo iniciarla: cuando se toca la pantalla. El ADC lo indica con **ADC_PENIRQ_n**, que normalmente está a nivel alto y pasa a nivel bajo al tocar la pantalla con el dedo o un lápiz. La FPGA debe monitorizar esta señal e iniciar la comunicación serie cuando pase a 0.

La comunicación empieza activando SCEN y generando ADC_DCLK y ADC_DIN según el diagrama. Por ADC_DIN se envía un **comando de control** que solicita la coordenada X o la Y; la tabla siguiente muestra los bits de cada comando. Tras recibirlo, el ADC realiza la conversión y transmite en serie por **ADC_DOUT** los 12 bits de la coordenada, sincronizados con ADC_DCLK. Como cada coordenada requiere un comando distinto, el proceso se repite dos veces: una para X y otra para Y.

![[assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen055.png]]

ADC_DIN debe permanecer a nivel bajo cuando no se transmite un comando.

> [!warning] ADC_DCLK no es un reloj
> A pesar de su nombre, ADC_DCLK no es propiamente una señal de reloj: en reposo está a nivel bajo y solo oscila durante la comunicación, marcando la velocidad y la sincronización de los bits. Cada secuencia de transmisión-recepción de una coordenada dura **24 periodos** de ADC_DCLK. El ADC admite periodos entre **0,5 μs y 0,1 ms**, es decir, velocidades entre **10 kbps y 2 Mbps**.

![[assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen054.png]]

## Apartado 1: Diseño del interfaz serie

![[assets/diseno-de-una-comunicacion-serie/subtarea-1-interface-serie-del-convertidor-adc/imagen045.png]]

En el primer apartado se diseña el interfaz de comunicación serie con el ADC para obtener las coordenadas X e Y del punto de contacto, ajustándose a la temporización del AD7843. El bloque tendrá una entrada de reloj para el oscilador de **50 MHz**, un reset asíncrono activo a nivel bajo, las señales de comunicación con el ADC y dos buses de salida de **12 bits**, uno por coordenada.

Aunque el reloj es de 50 MHz, la velocidad de la comunicación debe estar entre 10 kbps y 2 Mbps. Se propone como referencia **70 kbps**.

Para facilitar el diseño y su verificación se proporciona un proyecto de Quartus archivado, [[assets/diseno-de-una-comunicacion-serie/plantilla_proyecto_4.qar|Plantilla_Proyecto_4.qar]], que incluye una plantilla del módulo **ADC_CONTROL.v** con los puertos ya definidos, que debes completar o sustituir por tu diseño. El proyecto contiene también los ficheros de verificación y está totalmente configurado, así que se recomienda partir de él en lugar de crear el circuito desde cero.

### Sugerencia: contador de semiciclos

![[assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen048.png]]

Se sugiere utilizar un contador que lleve la cuenta de los **semiperiodos** de ADC_DCLK necesarios para completar la secuencia de transmisión-recepción. La secuencia de cada coordenada dura 24 periodos, es decir, **48 semiperiodos**, por lo que haría falta un contador de **módulo 48**. La figura añade esta cuenta al cronograma: su valor sirve para generar ADC_DCLK y ADC_DIN y para capturar los bits recibidos por ADC_DOUT.

![[assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen056.png]]

ADC_DCLK cambia de valor en cada semiperiodo. ADC_DIN debe cambiar en el momento adecuado, coincidiendo con los **flancos de bajada** de ADC_DCLK, como muestra la figura. Por ejemplo, el bit A0 se pone en ADC_DIN justo en el cambio de la cuenta 5 a la 6 y se mantiene durante las cuentas 6 y 7.

![[assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen057.png]]

Los bits que envía el ADC por ADC_DOUT deben capturarse en el **punto medio** de cada bit, donde la línea es más estable. Por ejemplo, el bit 9 se captura en el cambio de la cuenta 22 a la 23, el bit 8 entre las cuentas 24 y 25, etc. Estas capturas coinciden con los flancos de subida de ADC_DCLK, pero la referencia para hacerlas no es ese flanco sino la **cuenta del contador**, igual que para las demás señales.

### Sugerencia: concatenación de las lecturas

![[assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen058.png]]

Para obtener X e Y hacen falta dos secuencias de transmisión-recepción consecutivas. Sin embargo, el cronograma muestra tiempos de espera del ADC dentro de cada secuencia, así que se puede acelerar el proceso combinando ambas en una sola que aproveche esas esperas para solicitar ya el siguiente dato.

![[assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen059.png]]

En la secuencia concatenada de la figura, la solicitud de la coordenada Y empieza a enviarse mientras todavía se recibe la X; es posible porque las líneas de transmisión y recepción son independientes. La secuencia conjunta dura solo **80 semiperiodos**, en lugar de los 48 + 48 = 96 de dos comunicaciones por separado.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/Temporizacion_Tactil01.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

De nuevo, la tabla con los comandos que hay que enviar al ADC para leer las coordenadas X e Y:

![[assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen055.png]]

> [!question]- Con un reloj de 50 MHz y 70 kbps como referencia, ¿qué módulo debe tener el divisor ADC_DCLK_CNT?
>> [!todo] A 70 kbps cada bit (un periodo de ADC_DCLK) dura unos 14,3 μs, y cada semiperiodo unos 7,14 μs, es decir, unos 357 ciclos de 50 MHz. El valor exacto depende de cómo se genere ADC_DCLK en tu diseño; cualquier valor que deje la velocidad entre 10 kbps y 2 Mbps es válido.

### Estructura propuesta del diseño

A partir de la propuesta de concatenar las dos secuencias, se plantea el diagrama de bloques siguiente como orientación. Se trata de un **diseño síncrono**: todos los bloques comparten el reloj de 50 MHz y el reset asíncrono.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/diseno-de-una-comunicacion-serie/propuesta-estructura-diseno/diagrama_bloques_2024/Diagrama_bloques_bi_sin_half.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

El esquema tiene los siguientes bloques:

- A la izquierda, un contador de módulo **ADC_DCLK_CNT** (definido como parámetro) que actúa como divisor de frecuencia y fija la velocidad de transmisión entre 10 kbps y 2 Mbps, por ejemplo 70 kbps. Puede usarse el contador del [[sdp/es/proyecto1-juego-luces|Proyecto 1]].
- En el centro, un contador de **módulo 80** que sirve de referencia para los 80 semiperiodos de la secuencia de lectura de ambas coordenadas. De nuevo, sirve nuestro viejo contador de confianza.
- Abajo, en amarillo, el bloque que genera **ADC_DCLK**, a partir de la cuenta de semiperiodos y/o la señal TC del primer contador.
- A la derecha, el bloque que genera **ADC_DIN** en función de la cuenta de semiperiodos.
- Justo debajo, el bloque que **captura los bits de ADC_DOUT**, que usa la cuenta de semiperiodos y, como habilitación, el fin de cuenta del primer contador.
- Arriba, una **máquina de estados** que controla todo el diseño generando las habilitaciones necesarias. Es la que inicia la comunicación a partir de **ADC_PENIRQ_n** y genera la selección **SCEN**.

En esta propuesta la línea **ADC_BUSY no se utiliza**.

### Propuesta de máquina de estados

La máquina de estados que gestiona el protocolo no es única; puede diseñarse de varias maneras. Aquí se propone una, representada de dos formas equivalentes (diagrama ASM y diagrama de estados):

![[assets/diseno-de-una-comunicacion-serie/propuesta-fsm/imagen060.png]]

Es una máquina de cuatro estados:

- **S0**: estado inicial tras el reset. Es transitorio y sirve para inicializar las señales.
- **S1**: espera a que se toque la pantalla, es decir, se mantiene mientras ADC_PENIRQ_n vale 1. Cuando pasa a 0, se pasa a S2.
- **S2**: inicia el protocolo activando las habilitaciones (contadores y selección del convertidor). Se mantiene hasta completar la lectura de X e Y, que marcan los 80 semiperiodos contados por el contador de módulo 80.
- **S3**: estado de transición que termina la comunicación y lo indica con la señal **Fin_Trans**.

### Verificación funcional

![[assets/diseno-de-una-comunicacion-serie/verificacion-del-diseno/imagen061.png]]

Una vez descrito el interfaz en Verilog, hay que verificarlo funcionalmente mediante simulación. Generar a bajo nivel o con un editor de estímulos las señales del convertidor no es sencillo, así que conviene plantear el test a un nivel de abstracción mayor: se usa un **modelo funcional** de la pantalla táctil que emula la comunicación del ADC, descrito en el fichero **EMULE_ADC.vo**, y un *testbench* en Verilog que lo utiliza, simulado en ModelSim.

#### Estructura del testbench

El entorno de verificación del proyecto de Quartus tiene la estructura de la figura. El fichero de nivel superior, **tb_Touch_Control.v**, es una descripción estructural que instancia y conecta el resto de bloques:

- **ADC_CONTROL.v**: el diseño realizado, objeto de la verificación.
- **EMULE_ADC.vo**: emulador (modelo funcional) de la pantalla, que simula el comportamiento del ADC.
- **MFB.v**: modelo funcional de bus, que genera las señales básicas (reloj y reset) y proporciona el interfaz para simular una comunicación y comprobar si es correcta.

Como es habitual, tb_Touch_Control no tiene entradas ni salidas.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-del-diseno/diagrama_verificacion_bi/Diagrama_verificacion_bi.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

El MFB genera el reloj y el reset. Además, implementa una *task* que simula que se ha tocado la pantalla: proporciona unas coordenadas X e Y al emulador y activa la señal **NEW_COORD** para que inicie la emulación. El emulador pone entonces a nivel bajo ADC_PENIRQ_n, y ADC_CONTROL debe responder iniciando la comunicación, en la que recibirá las coordenadas que el MFB suministró al emulador. Cuando ADC_CONTROL obtiene X e Y, el MFB las compara con las originales y escribe en la consola de ModelSim si la verificación es correcta o no.

#### Comprobación del diseño

![[assets/diseno-de-una-comunicacion-serie/comprobacion/captura_11_may_2024.png]]

Al lanzar la simulación en ModelSim se emula la recepción de un par de coordenadas fijadas en el código del *testbench*. Si se reciben correctamente, en la consola aparece el mensaje **"Verificación del DUV correcta"**.

![[assets/diseno-de-una-comunicacion-serie/comprobacion/imagen034.png]]

Si no aparece, hay algún problema en el diseño. Por ejemplo:

- **La simulación no comienza** porque ModelSim ha detectado en ADC_CONTROL un error que Quartus ha dejado pasar. Hay que corregirlo en Quartus y volver a lanzar la simulación.
- **La simulación comienza pero no termina nunca.** ADC_CONTROL no funciona bien, normalmente porque la comunicación no termina: sus señales no vuelven a los valores de reposo.
- **La simulación termina con el mensaje "Error de Transmisión".** Las coordenadas recibidas no coinciden con las enviadas, así que ADC_CONTROL tiene algún error.

#### Modificación del testbench

Cuando ADC_CONTROL supere la simulación inicial, hay que ampliar la verificación modificando **tb_Touch_Control.v** para incluir dos casos nuevos:

1. **CASO 2**: tres comunicaciones consecutivas con tres datos distintos, sin activar el reset entre ellas. Los valores de las coordenadas pueden fijarse en el código. Añade este caso a partir de la línea 96 del fichero, bajo el comentario `CASO 2`, tomando como referencia las líneas del `CASO 1` pero **sin usar `MFB.reset`**.
2. **CASO 3**: otras tres comunicaciones consecutivas, ahora con coordenadas **aleatorias** en lugar de fijas. Añádelo bajo el comentario `CASO 3`. Se recomienda usar la función `$random` y la estructura `repeat`.

Cuando la verificación sea correcta, se puede pasar a la verificación física.

## Apartado 2: Verificación física

![[assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen052.png]]

El segundo apartado consiste en probar ADC_CONTROL en la placa DE2-115 con la pantalla táctil. Se obtienen las coordenadas X e Y del punto de toque y se muestran en los **displays de 7 segmentos** en hexadecimal, con 12 bits por coordenada. La figura muestra los valores extremos de las coordenadas en cada esquina.

![[assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen046.png]]

Hay que añadir al proyecto un bloque que convierta el valor binario de las coordenadas en las señales de los displays. Para ello, diseña un **decodificador de 7 segmentos** para un único dígito hexadecimal y crea un **nuevo nivel superior** que instancie ADC_CONTROL junto con varias copias del decodificador, hasta traducir todos los bits de las dos coordenadas.

> [!question]- ¿Cuántas copias del decodificador hacen falta?
>> [!todo] Seis: cada coordenada tiene 12 bits, es decir, 3 dígitos hexadecimales, y hay dos coordenadas.

También hay que asignar los pines para conectar con la pantalla y con los displays:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.53.png]]

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.32.44.png]]

Una vez comprobada la comunicación serie, termina la verificación comprobando que los valores de los displays corresponden aproximadamente con los esperados según el punto de toque.

> [!note] Las esquinas no se alcanzan
> Es prácticamente imposible ver en el display las coordenadas `12'h000` o `12'hFFF`: la superficie de toque es muy pequeña en comparación con la resolución táctil de la pantalla y, además, el marco de metacrilato limita el acceso a los bordes. No te preocupes si no alcanzas los valores extremos teóricos indicados por el fabricante.

### Verificación con SignalTap

Con la placa configurada, lo primero que se suele hacer es tocar la pantalla y comprobar que los displays muestran las coordenadas. Funcione o no, lo correcto es comprobar la comunicación serie **visualizando las señales con un analizador lógico**.

Quartus incluye un analizador lógico, **SignalTap**, que se integra con el diseño y permite ver las señales internas de la FPGA. Este vídeo muestra un ejemplo de uso para capturar señales:

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/signaltap-1.mp4"></video>

En este caso, la condición de disparo puede ser el **flanco de bajada de ADC_PENIRQ_n** o que el **contador de semiperiodos tome un valor concreto**, por ejemplo 5. Ambas permiten obtener una captura como esta:

![[assets/diseno-de-una-comunicacion-serie/signaltap/datos02.jpg]]

Además de las señales de entrada y salida se ha capturado el contador de semiperiodos que secuencia la comunicación.

> [!warning] Entregable
> Realiza una captura similar que demuestre el correcto funcionamiento del diseño e inclúyela en el informe. Arriba a la izquierda aparecen la fecha y la hora de uso de SignalTap, que deben coincidir con los ficheros del proyecto de Quartus entregado.

#### Captura de varios puntos

En el ejemplo anterior solo se ve un punto de toque. Capturar varios exigiría mucha memoria para almacenar la secuencia. Sin embargo, durante cada bit se toman muchas muestras, cuando con un par bastaría para saber qué dato se ha recibido. El siguiente vídeo muestra cómo configurar SignalTap para que solo almacene parte de las muestras; así se pueden capturar cientos de puntos de toque con la misma memoria.

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/signaltap-2.mp4"></video>

La imagen muestra una captura con esas condiciones, detenida tras solo 7 toques para no alargar la adquisición:

![[assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_a.jpg]]

Al ampliar la imagen se ve que se almacena solo una muestra por cada cuenta del contador de semiperiodos, de modo que cada cuenta parece durar un único ciclo de reloj. En realidad, simplemente no se guarda (ni se representa) toda la información capturada.

![[assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_b.jpg]]

## Apartado 3: Mejora del diseño

Durante la prueba en placa puede observarse que, al mantener el dedo sobre la pantalla, las coordenadas mostradas son estables y aproximadamente correctas, y al arrastrarlo cambian de forma coherente. Sin embargo, **al dejar de tocar** la pantalla el último valor mostrado cambia a una coordenada que no tiene nada que ver con la última posición (a veces solo cambia una de las dos). Esto ocurre porque, mientras se toca, el ADC lee la posición de forma continua y, al soltar, aún hace una última lectura en la que el dedo ya no toca la pantalla, con lo que el valor resistivo varía y la coordenada leída es incorrecta.

Este inconveniente se puede corregir ajustando dos aspectos:

1. **La velocidad de la comunicación**, que puede estar entre 10 kbps y 2 Mbps. En la plantilla la fija el parámetro **ADC_DCLK_CNT**, inicialmente a unos 70 kbps. Cambiándolo se puede reducir el efecto, aunque puede no bastar.
2. **Una pausa entre dos adquisiciones consecutivas**, para que el ADC no haga conversiones continuas. Al tocar la pantalla se realiza una comunicación y no se hace otra hasta que pase al menos cierto tiempo (por ejemplo, medio segundo), aunque el dedo siga en la pantalla. Así se hacen menos lecturas y se evitan las erróneas, a cambio de modificar ligeramente el diseño para añadir un elemento que genere esa espera.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/diagrama_bloques_2024/Diagrama_bloques_mejora_bi_sin_half.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Para reducir el número de lecturas se propone añadir un contador de **módulo 25 000 000**, que introduce un retardo de **medio segundo** entre una lectura y la siguiente; aparece abajo a la izquierda del nuevo diagrama de bloques.

Este contador obliga a modificar la máquina de estados de ADC_CONTROL. Una forma sencilla es añadir un estado de espera **S4** tras completar la comunicación y obtener las coordenadas. En S4 la máquina habilita el contador de módulo 25 000 000 y permanece en ese estado hasta que llega al fin de cuenta. Así no se inicia otra comunicación, ni por tanto otra captura, hasta que transcurre el medio segundo.

El diagrama de bloques muestra las nuevas entradas y salidas de la máquina, y la figura siguiente el diagrama de estados tras añadir el nuevo estado:

![[assets/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/imagen065.png]]

> [!tip] Ajuste del retardo
> El módulo del contador puede ajustarse a posteriori para elegir el retardo más adecuado según la velocidad de transmisión.

Verifica el diseño mejorado con el *testbench* proporcionado y pruébalo en la placa.

> [!question]- ¿Por qué 25 000 000 ciclos equivalen a medio segundo?
>> [!todo] Con un reloj de 50 MHz cada ciclo dura 20 ns, y 25 000 000 × 20 ns = 0,5 s.

next > [[sdp/es/index|Volver al índice]]
