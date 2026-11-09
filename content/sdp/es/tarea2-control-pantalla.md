---
title: "Tarea 2: Control y visualización en una pantalla"
draft: false
tags:
  - verilog
  - pantalla
  - memorias
---

prev > [[sdp/es/tarea1-sistemas-secuenciales|Tarea 1 - Diseño de sistemas secuenciales]]

*Por Ricardo José Colom Palero*

En esta tarea se plantean las bases para el diseño de un **generador de sincronismo** que gestione la visualización en una pantalla. Antes de abordar los diseños propuestos, estudia la información de esta página.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/objetivos/objetivos.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

## Objetivos

El objetivo de la práctica es aprender las características y modos de funcionamiento de una pantalla, que es la aplicación en la que se centra el diseño. En primer lugar hay que desarrollar e implementar un elemento de control que genere las líneas de sincronismo necesarias para visualizar en una pantalla. Para abordar con éxito el diseño habrá que profundizar en los conceptos de Verilog HDL orientados al diseño de elementos de control. La **metodología de verificación funcional** de los diseños es muy importante en esta práctica. Como elementos complementarios a la visualización se abordarán el uso de memorias ROM y el funcionamiento de un teclado.

## Visualización en una pantalla

En pintura, diseño gráfico, fotografía, imprenta y televisión, la teoría del color es un conjunto de reglas básicas sobre la mezcla de colores para conseguir el efecto deseado combinando luces o pigmentos. La luz blanca se puede producir combinando rojo, verde y azul, mientras que combinando pigmentos cian, magenta y amarillo se obtiene el negro.

Un sistema de color **aditivo** implica que se emite luz directamente desde una fuente de iluminación. La síntesis aditiva normalmente usa luz roja, verde y azul para producir el resto de colores: combinando los tres primarios con la misma intensidad se obtiene blanco, y variando la intensidad de cada uno se obtiene todo el espectro.

![[assets/control-pantalla/visualizacion-en-una-pantalla/2000px-additivecolor.png]]

**RGB** es un modelo de color basado en la síntesis aditiva, que representa un color mediante la suma de los tres colores primarios de luz: rojo, verde y azul (*Red, Green, Blue*). Todos los colores que se pueden crear mezclando estas tres luces forman el espectro de color; cuando no hay ninguna luz se percibe el negro. Los colores primarios de luz se aplican en monitores, televisores, proyectores de vídeo y, en general, en todos los sistemas que combinan materiales que emiten en el rojo, el verde y el azul.

### Representación de imágenes

Formalmente, una imagen es la distribución espacial de la luz irradiada en un plano. Matemáticamente es una función continua de dos variables, las coordenadas **x** e **y** de un punto del plano, que representa la intensidad de luz en ese punto. Para representar una imagen digitalmente hay que discretizar las coordenadas y la intensidad: una imagen digital es aquella en la que los valores de coordenadas e intensidad son finitos y discretos. Cada punto del plano con coordenadas discretas se llama **píxel** (*picture element*). Así, una imagen digital es un conjunto de puntos que forman una rejilla rectangular de **N** columnas y **M** filas: una imagen de **N × M píxeles**.

![[assets/control-pantalla/representacion-imagenes/imagen01.png]]

> [!note] Notación
> Matemáticamente una matriz se nombra como filas × columnas (aquí, **M × N**). Sin embargo, en pantallas siempre se indica primero la dimensión horizontal, es decir, el número de columnas; por eso decimos que la imagen es de **N × M** píxeles.

Una imagen digital es, por tanto, una rejilla rectangular de N × M píxeles que se puede mostrar en un monitor, en papel o en otro dispositivo. El primer píxel es el de la esquina superior izquierda, que corresponde a la coordenada **(0, 0)**.

Cada píxel debe contener información de color, en canales separados o subpíxeles que representan las componentes primarias del color en el modelo usado, sea RGB u otro.

La **profundidad de color** o bits por píxel (bpp) es el número de bits necesarios para representar el color de un píxel. Con una profundidad de **n** bits cada píxel puede tomar **2ⁿ** valores, es decir, representar **2ⁿ** colores distintos. Como el byte de 8 bits es la unidad básica casi universal de almacenamiento, las profundidades suelen ser divisores o múltiplos de 8 (1, 2, 4, 8, 16, 24 y 32), salvo algunas como 10 o 15 que usan ciertos dispositivos gráficos.

### Imagen en pantalla

Para mostrar una imagen digital en una pantalla hay que tener en cuenta sus características, sobre todo las dimensiones del área de visualización y la profundidad de color. El tamaño de imagen que indica el fabricante (primero la dimensión horizontal y luego la vertical, en píxeles) se refiere al **área de visualización**, es decir, a cuántos píxeles se ven.

Sin embargo, internamente la pantalla tiene un área mucho mayor: alrededor de la zona visible hay unas zonas «**negras**» (en gris en la imagen) que amplían el área de trabajo de la electrónica de control. Estas zonas sirven para estabilizar las señales de sincronismo que marcan una correcta visualización y tienen nombres propios: *Horizontal Back Porch* y *Horizontal Front Porch* a la izquierda y a la derecha del área visible, y *Vertical Back Porch* y *Vertical Front Porch* encima y debajo.

![[assets/control-pantalla/visualizacion-en-pantalla/imagen02.png]]

Estas zonas no son simétricas: los *back porch* son mayores que los *front porch*, porque las señales de sincronismo necesitan más tiempo de estabilización antes de visualizar.

Por tanto, al diseñar un controlador de pantalla hay que tener en cuenta estas zonas «negras» alrededor del área de visualización.

### Funcionamiento de la visualización

Las pantallas suelen usar la misma técnica que los antiguos tubos de rayos catódicos (CRT): un haz de electrones recorría una superficie fosforescente para «dibujar» la imagen. Gracias a la fosforescencia y a la persistencia del ojo humano la imagen parecía estable, aunque el haz se movía continuamente. El haz tardaba unos 20 ms en recorrer toda la pantalla y dibujar una imagen o *frame*.

En las pantallas planas no hay haz de electrones y lo que se representa es una matriz de píxeles, pero la técnica es la misma: un barrido de la pantalla mediante un punto llamado ***dot clock***. El *dot clock* empieza en la esquina superior izquierda, fuera del área visible (en los *porch*), y avanza hacia la derecha un píxel en cada flanco de reloj; como el avance lo marca una señal de reloj que hay que proporcionar a la pantalla, se le llama *dot clock*. Cuando llega al borde derecho hay que indicarle que ha terminado la fila y debe ir al principio de la siguiente, lo que se hace con la señal de **sincronismo horizontal**: un pulso negativo cuando el *dot clock* está en el último píxel de la fila.

Cuando el *dot clock* llega al último píxel de la última fila hay que indicarle que ha recorrido toda la pantalla y debe volver a la primera fila. De ello se encarga la señal de **sincronismo vertical**: un pulso negativo que indica que empieza una nueva imagen o *frame*.

Es decir, el *dot clock* es un punto que se guía externamente para recorrer la pantalla con tres señales: un reloj que lo hace avanzar un píxel en cada flanco, un sincronismo horizontal que lo devuelve al principio de la fila siguiente y un sincronismo vertical que lo devuelve al principio de la pantalla.

Que el *dot clock* tenga que volver rápidamente de la derecha a la izquierda para empezar una fila, o de abajo arriba para una nueva imagen, justifica la existencia de los márgenes (*porch*) alrededor del área visible, sobre todo si se tiene en cuenta que la técnica procede de los CRT, donde el haz se controlaba analógicamente.

En paralelo hay tres señales digitales, **RGB**, que representan la intensidad de cada color primario de cada píxel. Deben tener un valor válido cuando el *dot clock* está dentro del área visible, y ese valor es el color del píxel en el que se encuentra. Por eso las señales RGB deben cambiar **síncronamente** con el movimiento del *dot clock*, es decir, con el mismo reloj que lo hace avanzar.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/funcionamiento-de-la-visualizacion/Pantalla_ver13.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

La animación emula el barrido de la pantalla: muestra cómo se mueve el *dot clock* y cómo se activan los pulsos de sincronismo horizontal y vertical. Por supuesto, va mucho más lenta de lo real para que se vea el punto, ya que para obtener una imagen estable el punto debe recorrer toda la pantalla en unos 20 ms.

Fíjate en dos detalles: el punto cambia de color al entrar en el área visible, para indicar que en ese momento las señales RGB son las protagonistas, y, para no alargar la animación, en un momento dado el punto toma un atajo hasta el final de la pantalla.

## Pantalla táctil LTM

![[assets/control-pantalla/pantalla-tactil-ltm/imagen042.png]]

En esta práctica se usa la pantalla táctil LTM fabricada por Terasic para las placas del programa universitario de Altera, como la DE2-115. Es una pantalla de 4,3 pulgadas con relación de aspecto 15:9 y resolución de **800 × 480 píxeles** de 24 bits, capaz de representar unos 16 millones de colores. Dispone también de un convertidor analógico-digital que captura el punto de contacto.

### Estructura de la pantalla táctil LTM

![[assets/control-pantalla/estructura-pantalla-tactil-ltm/imagen043.png]]

En esta pantalla, la visualización y la captura del punto de contacto son totalmente independientes, lo que permite usar solo la visualización, como se hará en esta práctica. La parte de visualización tiene además una interfaz serie para ajustar la configuración (resolución, ajustes de color...), pero se puede visualizar con los valores por defecto, así que no se usará. La práctica se centra en las señales de datos RGB y de sincronismo.

### Diagrama de temporización horizontal

La figura muestra los requisitos temporales básicos para visualizar cada fila de la pantalla.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen133.png]]

Un pulso activo a nivel bajo de duración determinada (**thpw**) es la señal de sincronismo horizontal (**HD**), que indica el final de una línea y el comienzo de la siguiente. Tras el pulso, los datos RGB todavía no son válidos durante el *back porch* horizontal (**thbp**). Después viene el tiempo de visualización (**thd**), en el que los datos se aplican a los píxeles recorriendo la fila; durante este tiempo la señal de habilitación de la pantalla (**DEN**) debe estar a nivel alto. Por último está el *front porch* horizontal (**thfp**), en el que los datos vuelven a no ser válidos, tras el cual llega un nuevo pulso de sincronismo horizontal.

Todas las señales son síncronas con un reloj llamado **NCLK** y cambian con su flanco de subida. La pantalla es un elemento pasivo: el reloj le sirve de referencia para marcar el ritmo de los datos RGB y de las señales de sincronismo.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen135.png]]

La tabla muestra los valores de la temporización horizontal para 800 × 480 píxeles. El fabricante indica que la frecuencia de reloj óptima es **33,2 MHz**, aunque se pueden usar otras hasta un máximo de **40 MHz**. En particular, con **25 MHz** también se consigue una visualización correcta.

### Diagrama de temporización vertical

La figura muestra los requisitos temporales básicos para cada *frame* o imagen. El sincronismo vertical (**VD**) es similar al horizontal, salvo que un pulso de VD indica que ha terminado un *frame* (un refresco completo de la pantalla) y empieza el siguiente; además, los datos son ahora el conjunto de todas las filas del *frame*.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen134.png]]

Un pulso activo a nivel bajo de duración determinada (**tvpw**) es la señal de sincronismo vertical (**VD**), que indica el final de un *frame* y el comienzo del siguiente. Tras el pulso, los datos RGB no son válidos durante el *back porch* vertical (**tvbp**). Después viene el tiempo de visualización (**tvd**), en el que los datos se aplican a los píxeles, pero solo dentro del área visible que marcan las señales horizontales; durante este tiempo **DEN** va cambiando y está desactivada (a nivel bajo) durante el *back porch* y el *front porch* horizontales. Por último está el *front porch* vertical (**tvfp**), con datos no válidos, tras el cual llega un nuevo pulso de VD.

Las señales de este diagrama cambian al cambiar de línea, porque corresponden al movimiento vertical del puntero: el sincronismo horizontal (**HD**) es el que marca sus cambios.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen136.png]]

La tabla muestra los valores de la temporización vertical para 800 × 480 píxeles. Se expresan tomando como unidad el tiempo de una línea horizontal (**H**): por ejemplo, el *back porch* vertical vale 35 líneas.

## Estructura de la tarea

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/estructura-de-la-tarea/indice.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

La práctica consiste en diseñar un sistema de control y visualización en una pantalla. Se ha elegido una pantalla táctil, que permite obtener las coordenadas del punto tocado, pero en esta práctica solo se trabaja la visualización.

La práctica se divide en **siete subtareas**. La primera es el diseño del generador de sincronismo; a partir de ahí la complejidad aumenta (colores, barras, imágenes, caracteres) hasta escribir en pantalla los caracteres de un teclado PS/2 conectado a la placa.

## Subtarea 1: Generación de las señales de sincronismo

![[assets/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/imagen051.png]]

Primero se diseña el bloque que genera las señales de datos y sincronismo de la pantalla, que permitirá representar imágenes. La configuración inicial de la pantalla ya permite visualizar con una resolución de 800 × 480 píxeles, así que **no hace falta diseñar la interfaz serie**: solo se necesita para cambiar la resolución u otros parámetros.

Diseña el módulo que genera las señales de sincronismo. Como se ve en la figura, tendrá:

- **Entradas:** reloj **CLK** y reset activo a nivel bajo **RST_n**.
- **Salidas:** sincronismo horizontal (**HD**) y vertical (**VD**), reset global de la pantalla (**GREST**), reloj hacia la pantalla (**NCLK**), habilitación de la visualización (**DEN**), que indica cuándo son válidos los datos RGB, y dos buses, **Fila** y **Columna**, con las coordenadas del píxel que se está representando en cada momento.

### Representación con cuentas

El controlador consiste básicamente en generar los sincronismos horizontal y vertical y el reloj que guían el barrido del *dot clock*. Para ello hay que tener en cuenta los diagramas temporales del fabricante, de los que se deduce que para visualizar una imagen de 800 × 480 píxeles hay que gestionar un barrido de **1056 × 525 puntos**. La figura muestra las coordenadas de los extremos del barrido y las posiciones del área visible.

![[assets/control-pantalla/representacion-con-cuentas/imagen05.png]]

El área visible empieza en la coordenada **(216, 35)** y termina en la **(1015, 514)**; entre ellas están los 800 × 480 píxeles. En estos rangos están activas las señales **HDEN** y **VDEN**, que indican que se está en el área de visualización.

### Propuesta de estructura del diseño

Como propuesta orientativa se puede usar el diagrama de bloques de la imagen.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/propuesta-estructura-diseno/Diagrama_bloques_ver20.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

- Arriba a la izquierda hay un gestor de reloj o **PLL**, que genera a partir del oscilador externo de 50 MHz el reloj de **25 MHz** que necesita la pantalla (**NCLK**). El resto del diseño debe funcionar con este reloj de 25 MHz.
- En el centro está el contador de **módulo 1056** (**HCOUNT**), que cuenta los píxeles horizontales, es decir, la columna. Se incrementa en cada flanco de subida del reloj de 25 MHz y, al llegar a 1055, vuelve a cero. Su salida de fin de cuenta **TC** se activa cuando la cuenta vale 1055 y se usa también para generar el sincronismo horizontal.
- Debajo está el contador de **módulo 525** (**VCOUNT**), que cuenta las filas. Se incrementa cada vez que HCOUNT llega al fin de cuenta. Su **TC** se usa para generar el sincronismo vertical.
- A la derecha, en amarillo, está el generador de **DEN**, que a partir de la fila y la columna de HCOUNT y VCOUNT activa DEN en el área visible, de **(216, 35)** a **(1015, 514)**.
- Por último, dos inversores obtienen **HD** y **VD** a partir de los fines de cuenta de HCOUNT y VCOUNT.

> [!question]- ¿Cuánto dura un *frame* con un reloj de 25 MHz?
>> [!todo] 1056 × 525 ciclos × 40 ns = 22,18 ms, unas 45 imágenes por segundo.

### Uso del IP Catalog para crear un PLL

Aunque el fabricante fija NCLK en 33,2 MHz, la pantalla acepta frecuencias de hasta 40 MHz, y es perfectamente válido usar 25 MHz, como en VGA. Lo más adecuado es que **todo el diseño** funcione con un reloj de 25 MHz en lugar de los 50 MHz del oscilador de la placa.

> [!question] ¿Cómo se obtienen 25 MHz a partir del oscilador de 50 MHz manteniendo un diseño síncrono correcto?
> Con uno de los **PLL** internos de la FPGA, que generan un reloj de distinta frecuencia y fase a partir de otro.

Los PLL internos se generan y configuran con la herramienta **IP Catalog** de Quartus (antes *MegaWizard Plug-In Manager*), una biblioteca de bloques hardware y funciones sintetizables. Entre ellas está **ALTPLL**, que crea un módulo con los parámetros adecuados para usar los PLL de la FPGA. En sus ventanas de configuración se fijan las características del PLL, y la herramienta genera los archivos necesarios, entre ellos una plantilla para instanciarlo en el diseño.

La animación **Cómo crear un PLL** muestra paso a paso qué parámetros y opciones hay que fijar para obtener un reloj de 25 MHz a partir de uno de 50 MHz. El punto de partida es el proyecto de Quartus en el que se hace el diseño.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/ip_pll_ver11/IP_PLL_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Al generar el PLL, el IP Catalog crea en el directorio del proyecto varios archivos, entre ellos **pll_ltm_inst.v**, con un ejemplo de cómo instanciarlo:

```verilog
pll_ltm pll_ltm_inst (
  .inclk0 ( inclk0_sig ),
  .c0     ( c0_sig )
);
```

### Verificación del diseño

![[assets/control-pantalla/verificacion-del-diseno/imagen061.png]]

Una vez descrito el módulo **LCD_SYNC**, hay que verificar mediante simulación que los contadores funcionan y que los sincronismos horizontal y vertical se generan según las especificaciones. Como mínimo hay que recorrer la pantalla una vez, lo que supone unos **22 ms** de simulación.

Escribe un testbench en Verilog HDL que, mediante ***tasks***, use los valores de Fila y Columna y/o las señales de sincronismo para detener la simulación. Primero puedes detenerla tras recorrer la primera fila y después simular el recorrido completo de la pantalla.

> [!warning] No uses el tiempo para detener la simulación
> La simulación debe detenerse por el estado del diseño (fila, columna, sincronismos), no tras un retardo fijo.

Después comprueba el funcionamiento en el visor de ondas, usando el zoom (lupas) para verificar los contadores y los sincronismos.

**Simulación de una fila:**

![[assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.05.17-1.png]]

**Detalle del final de la simulación de una fila:**

![[assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.05.48-1.png]]

**Simulación de un recorrido completo de la pantalla:**

![[assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.16.01.png]]

**Detalle del final del recorrido completo:**

![[assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.17.47.png]]

## Subtarea 2: Barras de colores en la pantalla

![[assets/control-pantalla/subtarea-3/imagen140.png]]

Una vez diseñado el módulo **LCD_SYNC**, hay que comprobarlo en la placa DE2-115. Para ello solo hace falta usar LCD_SYNC y asignar valores a las señales de color (RGB) para que en la pantalla se vean las barras de colores de la imagen superior. La figura muestra el esquema de bloques. Como todas las barras tienen la misma anchura, el valor de RGB depende **solo de la columna** que genera LCD_SYNC.

![[assets/control-pantalla/subtarea-3/imagen163.png]]

Una vez diseñado el módulo **BARRAS_LCD**, verifica su funcionamiento con una simulación RTL en ModelSim. Comprobar el resultado en el visor de ondas puede ser muy laborioso, pero se dispone de una herramienta web que emula la pantalla y genera la imagen a partir de un fichero de texto y de los parámetros de la pantalla. Ese fichero es el resultado de una simulación en ModelSim y contiene en cada línea el tiempo de simulación y los valores de **HD, VD, DEN, R, G y B** en ese instante.

Este es un ejemplo de las primeras líneas del fichero para RGB de 24 bits (8 bits por color). El tiempo está en picosegundos, aunque también se pueden usar nanosegundos.

![[assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.11.png]]

Para obtener el fichero hay que simular el diseño en ModelSim con un testbench, como en las sesiones anteriores, al que se añaden los bloques procedurales siguientes (adaptados a tu diseño). Así se genera el fichero `vga.txt` con los resultados en el formato adecuado. La simulación debe durar lo suficiente para un *frame* completo, unos **22 ms**.

![[assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.33.png]]

Para comprobar el resultado usa el emulador de pantalla [Screen Simulator](https://is.gd/JtLbap), también enlazado en la barra lateral de PoliformaT. Selecciona el fichero `vga.txt`, pulsa **Iniciar** y obtendrás la imagen resultante:

![[assets/control-pantalla/subtarea-3/captura-de-pantalla-2022-09-21-a-las-12.12.26.png]]

Cuando la simulación sea correcta, prueba el diseño en la placa DE2-115 con la siguiente asignación de pines:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.56.png]]

## Subtarea 3: Visualización de una imagen en la pantalla

![[assets/control-pantalla/subtarea-3/imagen164b.png]]

En esta subtarea se visualiza una imagen almacenada en una **memoria ROM** interna de la Cyclone IV. Partiendo del módulo LCD_SYNC hay que realizar el diseño del diagrama de bloques:

![[assets/control-pantalla/subtarea-3/imagen165.png]]

Se añade una memoria que contiene la imagen. Cada posición guarda el color de un píxel, así que hay que direccionar la memoria secuencialmente, igual que se recorre la pantalla.

El bloque **Direccionamiento** genera las direcciones de memoria a partir de la fila y la columna de **LCD_SYNC**. Su funcionamiento depende del modo de direccionamiento con que se haya almacenado la imagen:

- **Direccionamiento continuo.** Los píxeles se guardan consecutivamente, empezando por el de la esquina superior izquierda en la dirección 0 y siguiendo el barrido hacia la derecha hasta completar la fila, para continuar con la siguiente. Para una imagen de **X × Y** píxeles hace falta un bus de direcciones de **k** bits y una memoria de al menos **X × Y** posiciones. Este modo optimiza la memoria, pero complica el direccionamiento, porque Fila y Columna incluyen las zonas de *porch* mientras que en memoria solo está la imagen visible.
- **Direccionamiento X-Y.** Los píxeles de cada fila se guardan consecutivamente, pero cada fila empieza en una dirección múltiplo de una potencia de dos: la primera en la 0 y la segunda en **2ⁿ**, la menor potencia de 2 **mayor o igual** que **X**. Por ejemplo, para una imagen de 400 × 240 la primera fila empieza en la dirección 0, la segunda en la 512, la tercera en la 1024, etc. Quedan huecos sin usar entre filas, pero la dirección se obtiene simplemente **concatenando** Y y X. La memoria necesaria es de unas **2ⁿ × Y** posiciones. Igual que antes, para obtener la dirección a partir de Fila y Columna hay que descontar el *back porch*.

![[assets/control-pantalla/subtarea-3/imagen167.png]]

Otro aspecto es la **codificación del color**. Como muestra la imagen, hay muchas opciones: desde blanco y negro con 1 bit o escala de grises de 8 bits hasta RGB de 30 bits. Cada píxel en memoria puede ocupar de 1 a 30 bits y hay que recodificarlo al formato RGB de 24 bits de la pantalla; de ahí el módulo **Datos a RGB**. Para recodificar:

- Si sobran bits, elimina los de **menor peso**.
- Si faltan bits, coloca los disponibles en la parte **alta** y replícalos en la parte baja, de mayor a menor peso, hasta completar.
- Para pasar de escala de grises a color, pon el mismo valor en los tres colores.

![[assets/control-pantalla/subtarea-3/imagen166.png]]

Realiza el diseño para visualizar una **imagen de 400 × 240 píxeles en RGB de 16 bits con direccionamiento X-Y**, almacenada en el fichero [[assets/control-pantalla/subtarea-3/imagen_rgb16_xy.hex|imagen_rgb16_xy.hex]]. La pantalla muestra **800 × 480 píxeles en RGB de 24 bits**, así que además de recodificar el color, el bloque de direccionamiento debe **replicar los píxeles** para duplicar el tamaño de la imagen.

> [!tip] RGB de 16 bits
> El formato habitual es RGB565: 5 bits de rojo, 6 de verde y 5 de azul. Aplica las reglas de recodificación anteriores a cada componente.

Verifica el diseño mediante simulación con ModelSim y el emulador de pantalla de la subtarea anterior, y después pruébalo en la placa DE2-115.

### Cómo crear una memoria ROM

La memoria será un bloque interno de la FPGA, que se crea con el **IP Catalog** de Quartus (antes *MegaWizard Plug-In Manager*). Su compilador de memorias genera memorias de varios tipos, entre ellas la ROM que se necesita aquí.

La ROM guardará la imagen y hay que inicializarla con el fichero suministrado, que puede ser HEX (datos en hexadecimal) o MIF (*Memory Initialization File*) y debe estar en la carpeta del proyecto.

La animación **Generación de una memoria ROM** muestra cómo generar la ROM y qué opciones fijar. El punto de partida es el proyecto de Quartus.

> [!danger] Atención
> La anchura de datos y el tamaño de memoria que aparecen en la animación **no son los de esta aplicación**; son solo orientativos. Elige los valores adecuados según las características de la imagen suministrada.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-3/ip_rom_img_ver11/IP_ROM_Img_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Al generar la ROM se crean varios archivos en el directorio del proyecto, entre ellos **ROM_image_inst.v**, con un ejemplo de instanciación:

```verilog
ROM_image ROM_image_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

## Subtarea 4: Visualización de caracteres en pantalla

![[assets/control-pantalla/subtarea-4/imagen139.png]]

El objetivo es mostrar caracteres, en concreto llenar toda la pantalla con caracteres iguales o distintos. Se ha elegido esta representación porque es mucho más fácil de implementar y de comprobar: no importa la posición en pantalla, solo hay que generar las señales RGB.

Como la pantalla se refresca constantemente, hace falta una memoria que guarde los caracteres (por ejemplo 0, A, B...). Se diseñará un módulo que lea de memoria cada carácter y actúe sobre las señales RGB según la Fila y la Columna de LCD_SYNC para mostrarlo.

La memoria será interna de la FPGA (*on-chip*) y se crea con el **IP Catalog** de Quartus, como en la subtarea anterior.

Una **ROM** es un conjunto de celdas con datos de un tamaño determinado almacenados previamente. Para leer un dato basta con indicar la dirección de la celda y la memoria entrega su contenido. Tiene, por tanto, un bus de direcciones, cuyo tamaño depende del número de celdas, y un bus de datos. Las memorias internas de la FPGA son **síncronas**, así que necesitan una señal de reloj.

![[assets/control-pantalla/subtarea-4/imagen160b.png]]

La memoria guarda los caracteres, de **8 × 8 píxeles**, con un bit por píxel que indica si está encendido o apagado. Su contenido se inicializa con un fichero MIF o Intel-HEX que fija el valor de cada celda, y que puede escribirse en binario, hexadecimal, decimal u octal. La imagen muestra la estructura del MIF de esta subtarea: una memoria de **8192 celdas de 1 bit**, con direcciones en decimal y datos en binario para que se entienda mejor.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/MIF_File.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

El fichero [[assets/control-pantalla/subtarea-4/char_rom-1.mif|char_rom-1.mif]] es un ejemplo de cómo es un MIF con la definición de los caracteres.

> [!warning] No uses este MIF para crear la memoria
> Da error al simular. Usa en su lugar el fichero HEX del apartado *Uso del IP Catalog para crear una ROM*.

> [!question]- ¿Cómo se reparten los 13 bits de dirección de la ROM de caracteres?
>> [!todo] 8192 = 2¹³ celdas = 128 caracteres × 8 filas × 8 columnas: 7 bits para el código del carácter, 3 para la fila y 3 para la columna dentro del carácter.

### Propuesta de estructura del diseño

Con lo explicado se puede usar como propuesta el diagrama de bloques de la imagen, con tres bloques: **LCD_SYNC**, **SELEC_COLOR** y **CHAR_ROM**.

![[assets/control-pantalla/subtarea-4/imagen147c.png]]

- **LCD_SYNC** es el bloque de la subtarea 1, que genera los sincronismos.
- **SELEC_COLOR** genera las señales RGB: es un multiplexor que elige entre el color de fondo (*background*) y el de los caracteres (*foreground*), según una señal de **CHAR_ROM** que indica si el píxel es fondo o carácter.

![[assets/control-pantalla/subtarea-4/imagen149.png]]

- **CHAR_ROM** está formado por la ROM y un bloque de **Direccionamiento**, conectados como en el diagrama inferior. El direccionamiento funciona como en la subtarea anterior: genera la dirección a partir de Fila y Columna. En la parte alta del bus de direcciones se concatena la posición del carácter en la memoria, que coincide con su código ASCII. La memoria entrega así 1 bit, el del píxel de esa fila y columna del carácter: 0 para fondo y 1 para carácter.

![[assets/control-pantalla/subtarea-4/imagen148b.png]]

La siguiente animación interactiva ilustra el funcionamiento conjunto de CHAR_ROM y SELEC_COLOR:

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/Funcionamiento_Char_ROM_ver30.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

### Uso del IP Catalog para crear una ROM

La memoria guarda caracteres de 8 × 8 píxeles y se inicializa con el fichero HEX suministrado, [[assets/control-pantalla/subtarea-4/char_rom.hex|char_rom.hex]], que define una memoria de **8192 celdas de 1 bit**.

La animación **Generación de una memoria ROM** muestra qué parámetros, opciones y ajustes fijar para instanciar la memoria de este diseño. El punto de partida es el proyecto de Quartus.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/ip_rom_char_ver11/IP_ROM_Char_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Al generar la ROM se crea, entre otros, el archivo **ROM_char_inst.v**, con un ejemplo de instanciación:

```verilog
ROM_char ROM_char_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

### Mejora visual del diseño

Al probar el diseño en la placa se ve que las letras son muy pequeñas: caben **100 × 60 caracteres**, demasiados para una pantalla tan pequeña.

Una mejora es **aumentar el tamaño** de los caracteres replicando sus píxeles en horizontal y en vertical. Es una modificación sencilla que solo requiere cambiar dos líneas del bloque de **Direccionamiento**.

Haz las modificaciones necesarias para que los caracteres tengan el doble de tamaño, **16 × 16 píxeles**, y se vean mejor.

## Subtarea 5: Una frase en la pantalla

Se quieren mostrar los nombres de los componentes del grupo de prácticas en una línea más o menos centrada. Se puede partir del diseño anterior, con la diferencia de que el carácter a mostrar ya no es fijo, sino que depende de la posición en pantalla, controlada de nuevo por los contadores de fila y columna.

Una sugerencia importante es guardar la frase en **otra ROM**, cuyo contenido serán las direcciones de los caracteres en CHAR_ROM y que se direcciona con la fila y la columna. El éxito del ejercicio depende de un direccionamiento correcto y de generar bien el fichero MIF de inicialización.

![[assets/control-pantalla/subtarea-5/imagen142b.png]]

La mejor opción es implementar una **memoria de pantalla** para el texto: la misma idea que en la visualización de una imagen, pero con caracteres en lugar de píxeles. Al diseño anterior se añade una memoria que da el carácter a mostrar en cada instante. El diagrama muestra una propuesta:

![[assets/control-pantalla/subtarea-5/imagen173.png]]

Se parte de la versión con caracteres de 16 × 16 píxeles, así que en pantalla caben **50 × 30 caracteres**. Hay que añadir una memoria (en verde en el diagrama) con capacidad para todos ellos, en la que cada posición contiene el carácter a mostrar. Para simplificar se usa **direccionamiento X-Y**, obtenido de Columna y Fila por el bloque de Direccionamiento. La posición de un carácter viene dada por una coordenada horizontal entre 0 y 49 y una vertical entre 0 y 29.

Con direccionamiento X-Y la memoria de texto debe tener **1920 palabras de 7 bits** (64 × 30). Es una ROM con el mensaje, así que hay que crear un fichero de inicialización **MIF** con los códigos de los caracteres en sus posiciones. Como la memoria se recorre continuamente, **todas las posiciones** deben inicializarse con el código del espacio en blanco, que aquí es el 0 o el 0x20.

El fichero [[assets/control-pantalla/subtarea-5/text_rom_ejemplo.mif|text_rom_ejemplo.mif]] es un ejemplo de MIF para la memoria de texto con los nombres de dos alumnos en dos líneas. Puedes usarlo como punto de partida.

Una vez verificado el diseño en la placa, se puede modificar el texto en tiempo real con la herramienta de Quartus ***In-System Memory Content Editor***, que permite acceder a la ROM y cambiar su contenido con el diseño en marcha.

<!-- PoliformaT: vídeo de uso del In-System Memory Content Editor (no exportado) -->

> [!tip] Habilita el acceso en la ROM
> Para que el *In-System Memory Content Editor* vea la memoria, al crearla en el IP Catalog marca la opción *Allow In-System Memory Content Editor to capture and update content independently of the system clock* y dale un identificador.

> [!warning] Entrega
> Usa esta herramienta para modificar la memoria de texto con el diseño en marcha y comprueba que el texto se actualiza en la pantalla. Incluye capturas y/o fotos de la prueba en la memoria del trabajo.

## Subtarea 6: Imagen y texto en la pantalla

Se trata de unir la visualización de una imagen (subtarea 3) con la escritura de texto (subtarea anterior) encima de ella. En la figura se ha escrito «Palau de les Arts» sobre la imagen.

![[assets/control-pantalla/subtarea-6/imagen174.png]]

## Subtarea 7: Escribir desde el teclado y visualizar en pantalla

![[assets/control-pantalla/subtarea_opcional.png]]

Tras controlar la visualización y representar caracteres en posiciones determinadas, se quiere implementar un módulo que muestre en pantalla las teclas pulsadas en un **teclado PS/2** conectado a la placa DE2-115:

![[assets/control-pantalla/subtarea-7/imagen145_rotate.png]]

Para no tener que diseñar el control del teclado, los profesores proporcionan una versión de ese bloque: [[assets/control-pantalla/subtarea-7/visualiza.qar|visualiza.qar]]. El módulo entrega el código de la tecla pulsada, el ***scan code***, que es único y estándar para todos los teclados.

El *scan code* debe transformarse en un código que actúe sobre la ROM de caracteres para seleccionar el carácter correspondiente. Hay que diseñar el módulo que hace esta decodificación:

![[assets/control-pantalla/subtarea-7/imagen146.png]]

Por ejemplo, al pulsar la tecla «A» el *scan code* es **0x1C**. El módulo debe traducirlo al código de la letra A en el MIF de CHAR_ROM, es decir, a la dirección **0x41**.

Se puede partir del diseño de la subtarea 5, cambiando la ROM de texto por una **RAM de doble puerto**: un puerto de lectura que funciona igual que antes y otro de escritura donde se escriben los caracteres del teclado.

El teclado se conecta a la FPGA mediante dos señales de una comunicación serie: una de datos y otra de reloj para capturarlos. La tabla muestra su asignación de pines:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.31.png]]

next > [[sdp/es/tarea3-luces-fsm|Tarea 3 - Juego de luces mejorado con FSM]]
