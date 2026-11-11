---
title: "Proyecto 2: Diseño de un controlador de vídeo"
draft: false
tags:
  - verilog
  - pantalla
  - memorias
---

prev > [[sdp/es/proyecto1-juego-luces|Proyecto 1: Diseño de un juego de luces]]

En este proyecto se diseña un **controlador de vídeo** para la pantalla táctil de la placa DE2-115. El sistema incluye un generador de sincronismo y la circuitería necesaria para representar imágenes y texto en la pantalla. Como ampliación opcional se puede añadir un controlador de teclado para mostrar en pantalla lo que se escribe.

## Objetivos

- Comprender el funcionamiento de un controlador de vídeo.
- Diseñar sistemas secuenciales complejos.
- Diseñar sistemas basados en memorias ROM.
- Crear e instanciar *IP cores*.
- Depurar circuitos con memorias en funcionamiento.

## Tareas a realizar

**Primera entrega:**

- Apartado 1: circuito y testbench.
- Apartado 2: circuito, testbench y prueba en placa.
- Apartado 3: circuito y testbench.
- Informe (solo apartados 1 a 3), con los resultados del *RTL Viewer*, el informe de *warnings* de análisis y síntesis y las imágenes generadas con el *Screen Simulator*.

**Segunda entrega:**

- Apartado 4: circuito y testbench.
- Apartado 5: circuito, testbench y prueba en placa, incluida la prueba del *Memory Content Editor* para cambiar el carácter mostrado. La versión final debe generar caracteres de 16 × 16.
- Apartado 6: circuito, testbench y prueba en placa, incluida la prueba del *Memory Content Editor* para cambiar el texto mostrado.
- Informe (solo apartados 4 a 6), con los resultados del *RTL Viewer*, el informe de *warnings* de análisis y síntesis y las imágenes generadas con el *Screen Simulator*.

## Introducción

### Visualización en una pantalla

En pintura, diseño gráfico, fotografía, imprenta y televisión, la teoría del color es un conjunto de reglas básicas sobre la mezcla de colores para conseguir el efecto deseado combinando luces o pigmentos. La luz blanca se puede producir combinando rojo, verde y azul, mientras que combinando pigmentos cian, magenta y amarillo se obtiene el negro.

Un sistema de color **aditivo** emite luz directamente desde una fuente de iluminación. La síntesis aditiva normalmente usa luz roja, verde y azul para producir el resto de colores: los tres primarios con la misma intensidad dan blanco, y variando la intensidad de cada uno se obtiene todo el espectro.

![[assets/control-pantalla/visualizacion-en-una-pantalla/2000px-additivecolor.png]]

El **modelo RGB** se basa en la síntesis aditiva: representa un color como suma de los tres colores primarios de luz, rojo, verde y azul (*Red, Green, Blue*). Todos los colores que se pueden crear mezclándolos forman el espectro de color; sin ninguna luz se percibe el negro. Los colores primarios de luz se aplican en monitores, televisores, proyectores y, en general, en los sistemas que combinan materiales que emiten en el rojo, el verde y el azul.

#### Representación de imágenes

Formalmente, una imagen es la distribución espacial de la luz irradiada en un plano: una función continua de dos variables, las coordenadas **x** e **y**, que da la intensidad de luz en cada punto. Para representarla digitalmente hay que discretizar coordenadas e intensidad: una imagen digital es aquella en la que ambas son finitas y discretas. Cada punto con coordenadas discretas es un **píxel**. Normalmente una imagen digital es una rejilla rectangular de **N** columnas y **M** filas: una imagen de **N × M píxeles**.

![[assets/control-pantalla/representacion-imagenes/imagen01.png]]

> [!note] Notación
> Matemáticamente una matriz se nombra como filas × columnas (aquí, **M × N**). En pantallas, sin embargo, siempre se indica primero la dimensión horizontal, es decir, las columnas; por eso decimos que la imagen es de **N × M** píxeles.

El primer píxel es el de la esquina superior izquierda, con coordenadas **(0, 0)**. Cada píxel contiene información de color en canales separados (subpíxeles) que representan las componentes primarias del modelo de color usado, sea RGB u otro.

La **profundidad de color**, en bits por píxel (bpp), es el número de bits que representan el color de un píxel. Con **n** bits, cada píxel puede tomar **2ⁿ** valores, es decir, **2ⁿ** colores. Como el byte es la unidad básica casi universal de almacenamiento, las profundidades suelen ser divisores o múltiplos de 8 (1, 2, 4, 8, 16, 24 y 32), salvo algunas como 10 o 15 que usan ciertos dispositivos gráficos.

#### Imagen en pantalla

Para mostrar una imagen en una pantalla hay que tener en cuenta sus características, sobre todo el tamaño del área de visualización y la profundidad de color. El tamaño que da el fabricante (primero el horizontal, en píxeles) se refiere al **área de visualización**: cuántos píxeles se ven.

Internamente, sin embargo, la pantalla tiene un área mucho mayor: alrededor de la zona visible hay zonas «negras» (en gris en la imagen) que sirven para estabilizar las señales de sincronismo. Se llaman ***Horizontal Back Porch*** y ***Horizontal Front Porch*** a la izquierda y a la derecha del área visible, y ***Vertical Back Porch*** y ***Vertical Front Porch*** encima y debajo.

![[assets/control-pantalla/visualizacion-en-pantalla/imagen02.png]]

Estas zonas no son simétricas: los *back porch* son mayores que los *front porch*, porque los sincronismos necesitan más tiempo de estabilización antes de visualizar. Un controlador de pantalla tiene que tener en cuenta estas zonas.

#### Funcionamiento de la visualización

Las pantallas suelen usar la misma técnica que los antiguos tubos de rayos catódicos (CRT), en los que un haz de electrones recorría una superficie fosforescente para «dibujar» la imagen. Gracias a la fosforescencia y a la persistencia del ojo, la imagen parecía estable aunque el haz se moviera continuamente; tardaba unos 20 ms en recorrer toda la pantalla y dibujar una imagen o **frame**.

En las pantallas planas no hay haz de electrones, pero la técnica es la misma: la pantalla se recorre con un punto llamado **dot clock**. Empieza en la esquina superior izquierda, fuera del área visible (en los *back porch*), y avanza un píxel a la derecha en cada flanco de reloj; se llama así porque el avance lo marca una señal de reloj que hay que dar a la pantalla. Al llegar al borde derecho, la señal de **sincronismo horizontal**, un pulso negativo en el último píxel de la fila, le indica que pase a la siguiente fila. Al llegar al último píxel de la última fila, la señal de **sincronismo vertical**, otro pulso negativo, le indica que vuelva a la primera fila y empiece un nuevo *frame*.

Es decir, el *dot clock* es un punto que se guía desde fuera con tres señales: un reloj que lo hace avanzar un píxel por flanco, un sincronismo horizontal que lo lleva al principio de la fila siguiente y un sincronismo vertical que lo devuelve al principio de la pantalla. Que tenga que volver rápidamente de derecha a izquierda, o de abajo arriba, justifica los márgenes (*porch*), sobre todo porque la técnica viene de los CRT, con un haz de control analógico.

En paralelo hay tres señales digitales, **R**, **G** y **B**, con la intensidad de cada color primario de cada píxel. Deben tener un valor válido cuando el *dot clock* está en el área visible, y ese valor es el color del píxel en el que se encuentra. Por eso RGB debe cambiar **síncronamente** con el *dot clock*, con la misma señal de reloj.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/funcionamiento-de-la-visualizacion/Pantalla_ver13.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

La animación emula el barrido: muestra cómo se mueve el *dot clock* y cómo se activan los pulsos de sincronismo. Va mucho más lenta de lo real (el barrido real dura unos 20 ms). El punto cambia de color al entrar en el área visible, para indicar que entonces cuentan las señales RGB, y en un momento dado toma un atajo hasta el final para no alargar la animación.

### Pantalla táctil LTM

![[assets/control-pantalla/pantalla-tactil-ltm/imagen042.png]]

La pantalla táctil LTM, de Terasic, está pensada para las placas del programa universitario de Altera, como la DE2-115 del laboratorio. Es una pantalla de 4,3 pulgadas, relación de aspecto 15:9 y resolución de **800 × 480 píxeles** de 24 bits (hasta 16 millones de colores). Tiene además un convertidor analógico-digital que captura el punto de contacto.

#### Estructura de la pantalla táctil LTM

![[assets/control-pantalla/estructura-pantalla-tactil-ltm/imagen043.png]]

La visualización y la captura del punto de contacto son totalmente independientes, así que en este proyecto solo se usa la visualización. La parte de visualización tiene una interfaz serie para ajustar resolución, color, etc., pero los valores por defecto sirven, así que no se usará: el proyecto se centra en las señales de datos RGB y de sincronismo.

#### Diagrama de temporización horizontal

La figura muestra los requisitos temporales básicos para visualizar cada fila.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen133.png]]

Un pulso activo a nivel bajo de duración **t_hpw** es el sincronismo horizontal (**HD**), que marca el final de una línea y el comienzo de la siguiente. Tras él, los datos RGB se ignoran durante el *horizontal back porch* (**t_hbp**). Después viene el tiempo de visualización (**t_hd**), en el que los datos se aplican a los píxeles de la fila y la habilitación de la pantalla (**DEN**) debe estar a nivel alto. Por último, durante el *horizontal front porch* (**t_hfp**) los datos vuelven a ignorarse, y llega un nuevo pulso de HD.

Todas las señales son síncronas con el reloj **NCLK** y cambian con su flanco de subida. La pantalla es un elemento pasivo y usa este reloj como referencia para los datos y los sincronismos.

![[assets/control-pantalla/diagrama-temporizacion-horizontal/imagen135.png]]

La tabla da los valores para 800 × 480 píxeles. El fabricante indica que la frecuencia óptima de reloj es **33,2 MHz**, aunque admite hasta **40 MHz**. Con **25 MHz** también se visualiza correctamente, y es el valor que se usará en el proyecto.

#### Diagrama de temporización vertical

La figura muestra los requisitos temporales para cada *frame*. El sincronismo vertical es similar al horizontal, pero su pulso indica que ha terminado un refresco completo de la pantalla y empieza el siguiente, y los datos son ahora el conjunto de todas las filas.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen134.png]]

Un pulso activo a nivel bajo de duración **t_vpw** es el sincronismo vertical (**VD**). Tras él, los datos se ignoran durante el *vertical back porch* (**t_vbp**). Después viene el tiempo de visualización (**t_vd**), en el que los datos se aplican solo dentro del área visible que marcan las señales horizontales; durante este tiempo **DEN** está a nivel bajo en los *back porch* y *front porch* horizontales. Por último, durante el *vertical front porch* (**t_vfp**) los datos se ignoran y llega un nuevo pulso de VD.

Las señales de este diagrama cambian al cambiar de línea, porque corresponden al movimiento vertical del puntero; por eso es **HD** quien marca sus cambios.

![[assets/control-pantalla/diagrama-temporizacion-vertical/imagen136.png]]

Los valores de la tabla se expresan en unidades de una línea horizontal (**H**): por ejemplo, el *vertical back porch* vale 35 líneas.

## Estructura del proyecto

El proyecto tiene seis apartados obligatorios:

1. Señales de sincronismo.
2. Barras de colores en pantalla.
3. Imagen en blanco y negro en pantalla.
4. Imagen en color en pantalla.
5. Caracteres en pantalla.
6. Texto en pantalla.

> [!note] Apartados opcionales
> Los apartados 7 y 8 son ampliaciones opcionales. Este curso no son obligatorios ni cuentan para la nota; se incluyen para quien quiera desarrollar una aplicación completa.

## Apartado 1: Señales de sincronismo

![[assets/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/imagen051.png]]

Primero se diseña el bloque que genera las señales de datos y sincronismo, que permitirá representar imágenes. La configuración inicial de la pantalla ya permite visualizar a 800 × 480 píxeles, así que **no hace falta diseñar la interfaz serie**: solo sería necesaria para cambiar la resolución u otros parámetros.

Diseña el módulo que genera los sincronismos. Como se ve en la figura, tendrá:

- **Entradas:** reloj **CLK** y reset asíncrono activo a nivel bajo **RST_n**.
- **Salidas:** sincronismo horizontal (**HD**) y vertical (**VD**), reset global de la pantalla (**GREST**), reloj hacia la pantalla (**NCLK**), habilitación de la visualización (**DEN**), que indica cuándo son válidos los datos RGB, y dos buses, **Fila** y **Columna**, con las coordenadas del píxel que se representa en cada momento.

### Representación con cuentas

El controlador genera los sincronismos horizontal y vertical y el reloj que guían el barrido del *dot clock*. Según los diagramas temporales del fabricante, para visualizar una imagen de 800 × 480 píxeles hay que gestionar un barrido de **1056 × 525 puntos**. La figura muestra las coordenadas de los extremos y del área visible.

![[assets/control-pantalla/representacion-con-cuentas/imagen05.png]]

El área visible va de la coordenada **(216, 35)** a la **(1015, 514)**; entre ellas están los 800 × 480 píxeles. En esos rangos están activas las señales **HDEN** y **VDEN**, que indican que se está en el área de visualización.

### Estructura propuesta del diseño

Como propuesta orientativa se sugiere el diagrama de bloques siguiente.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/propuesta-estructura-diseno/diagrama_bloques_ver20/Diagrama_bloques_ver20.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

- Arriba a la izquierda, un gestor de reloj (un **PLL**) genera a partir del oscilador de 50 MHz el reloj de **25 MHz** (**NCLK**) que necesita la pantalla. El resto del diseño funciona con este reloj.
- En el centro, un contador de **módulo 1056** (**HCOUNT**) cuenta los píxeles horizontales, es decir, la columna. Se incrementa en cada flanco de subida de NCLK y vuelve a cero tras 1055. Su fin de cuenta **TC**, activo cuando la cuenta vale 1055, sirve para generar el sincronismo horizontal.
- Abajo, un contador de **módulo 525** (**VCOUNT**) cuenta las filas. Se incrementa cada vez que HCOUNT llega al fin de cuenta, y su **TC** sirve para generar el sincronismo vertical.
- A la derecha, en amarillo, el bloque que genera **DEN** a partir de la fila y la columna: debe estar activa en el área visible, de **(216, 35)** a **(1015, 514)**.
- Por último, dos inversores dan a **HD** y **VD** la polaridad adecuada a partir de los fines de cuenta de HCOUNT y VCOUNT.

> [!question]- ¿Cuánto dura un *frame* con un reloj de 25 MHz?
>> [!todo] 1056 × 525 ciclos × 40 ns = 22,18 ms, unas 45 imágenes por segundo.

### Uso del *IP Catalog* para generar un PLL

Aunque el fabricante fija NCLK en 33,2 MHz, la pantalla acepta hasta 40 MHz y en particular 25 MHz, como una pantalla VGA. Lo más adecuado es que **todo el diseño** funcione a 25 MHz en lugar de con los 50 MHz del oscilador de la placa.

> [!question] ¿Cómo se obtienen 25 MHz a partir del oscilador de 50 MHz manteniendo un diseño síncrono correcto?
> Con uno de los **PLL** internos de la FPGA, que generan un reloj de distinta frecuencia y fase a partir de otro.

Los PLL internos se generan y configuran con la herramienta **IP Catalog** de Quartus, una biblioteca de bloques hardware y funciones sintetizables que se pueden incorporar a los diseños. Uno de ellos es **ALTPLL**, que crea un módulo con los parámetros adecuados para usar los PLL de la FPGA. En sus ventanas de configuración se fijan las características del PLL, y la herramienta genera los archivos necesarios, entre ellos una plantilla para instanciarlo.

La animación **Cómo crear un PLL** muestra cómo generarlo y qué opciones fijar para obtener 25 MHz a partir de 50 MHz. El punto de partida es el proyecto de Quartus del diseño.

> [!warning] Atención a las casillas
> Fíjate en qué opciones quedan marcadas al final. En particular, ***Create an 'areset' input to asynchronously reset the PLL*** y ***Create 'locked' output*** deben quedar **sin marcar**.

Si eliges mal los parámetros de un bloque IP como ALTPLL, o quieres cambiarlos, puedes volver a sus ventanas de configuración buscándolo en la subventana *Project Navigator* de Quartus (arriba a la izquierda), en *IP Components* o, si ya has compilado, en *Hierarchy*.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/ip_pll_ver11/IP_PLL_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Al generar el PLL, el IP Catalog crea varios archivos en el directorio del proyecto, entre ellos **pll_ltm_inst.v**, con un ejemplo de instanciación:

```verilog
pll_ltm pll_ltm_inst (
  .inclk0 ( inclk0_sig ),
  .c0     ( c0_sig )
);
```

### Verificación del diseño

Escribe un testbench en Verilog que verifique el módulo **LCD_SYNC**: que los contadores funcionan y que los sincronismos horizontal y vertical se generan correctamente. Como mínimo hay que recorrer la pantalla una vez, unos **22 ms** de tiempo simulado; una simulación así tarda unos 3 minutos.

> [!warning] No uses un tiempo fijo para terminar la simulación
> Usa condiciones basadas en las señales que genera el módulo (HD, VD, Fila, Columna...).

Después comprueba en el visor de ondas, con el zoom (lupas), que los contadores y los sincronismos funcionan, como en estas figuras:

**Simulación de una fila:**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_1.png]]

**Fin de la simulación de una fila (detalle):**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_2.png]]

**Simulación de un recorrido completo de la pantalla:**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_3.png]]

**Fin del recorrido completo (detalle):**

![[assets/control-pantalla/verificacion-del-diseno/p2verif_4.png]]

### Aceleración de la simulación

Como habrás comprobado, este diseño tarda muchísimo en simularse. Se debe al PLL, cuyo modelo de simulación a bajo nivel es muy complejo. Una vez seguros de que el bloque con el PLL funciona, podemos sustituir el PLL por un modelo de alto nivel que acelere la simulación, pero **solo al simular**: para la síntesis y la prueba en placa queremos el PLL real.

Para ello se usan **directivas de compilación**, que permiten al compilador «ver» o «ignorar» bloques de código. La directiva `` `ifdef `` seguida de una etiqueta indica que el código siguiente solo se tiene en cuenta si la etiqueta está definida; `` `else `` da la alternativa y `` `endif `` cierra el bloque:

```verilog
`ifdef ETIQUETA
  // Bloque de código 1: se usa si ETIQUETA está definida
`else
  // Bloque de código 2: se usa si no lo está
`endif
```

Las etiquetas se definen también con una directiva: `` `define ETIQUETA ``.

Usaremos la etiqueta **`MODEL_TECH`**, que ModelSim define automáticamente al simular pero Quartus no al compilar. Como el PLL divide la frecuencia exactamente por 2, se puede emular con un contador módulo 2, es decir, un flip-flop que cambia de estado en cada ciclo. Sustituye la instancia del PLL en **LCD_SYNC** por:

```verilog
`ifdef MODEL_TECH

// Modelo de alto nivel del PLL mediante un flip-flop
reg nclk_sim;
assign NCLK = nclk_sim;

always @(posedge CLK or negedge RST_n)
  if (~RST_n)
    nclk_sim <= 0;
  else
    nclk_sim <= ~nclk_sim;

`else

// Instancia del PLL real
// (sustituye estas líneas por las que hayas usado para instanciar tu PLL)
pll_ltm pll_ltm_inst (
  .inclk0(CLK),
  .c0(NCLK)
);

`endif
```

Así ModelSim solo «ve» el flip-flop y Quartus solo «ve» el PLL. Recompila y simula: el diseño compilado en Quartus sigue teniendo un PLL, pero la simulación tarda apenas unos segundos y da los mismos resultados.

## Apartado 2: Barras de colores en pantalla

![[assets/control-pantalla/subtarea-3/imagen140.png]]

Una vez diseñado **LCD_SYNC**, hay que comprobarlo en la placa. Basta con usar LCD_SYNC y asignar valores a las señales RGB para que se vean las barras de colores de la imagen. La figura muestra el esquema de bloques. Como todas las barras tienen la misma anchura y todas las filas son iguales, el valor de RGB depende **solo de la columna**.

![[assets/control-pantalla/subtarea-3/imagen163.png]]

### Verificación lógica

Una vez diseñado **BARRAS_LCD**, verifícalo con una simulación RTL en ModelSim. Comprobarlo en el visor de ondas es engorroso, pero hay una herramienta web que emula la pantalla y genera la imagen a partir de un fichero de texto. Ese fichero sale de una simulación en ModelSim y contiene en cada línea el tiempo de simulación y los valores de **HD**, **VD**, **DEN**, **R**, **G** y **B**, en ese orden.

Este es un ejemplo de las primeras líneas del fichero para RGB de 24 bits (8 por color). El tiempo está en picosegundos, aunque también puede ir en nanosegundos.

![[assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.11.png]]

Para generar el fichero `vga.txt`, añade a tu testbench estos bloques, adaptados a tu diseño. Como en el apartado anterior, la simulación debe cubrir un *frame* completo (unos 22 ms).

```verilog
integer fd;
event cierraFichero;
reg abierto;

initial
begin
  // Inserta aquí tu simulación (todos los casos de test)
  // ...
  $display("Fin de la simulacion");
  -> cierraFichero;
  #10;
  $stop;
end

initial
begin
  fd = $fopen("vga.txt","w");
  abierto = 1;
  @(cierraFichero);
  disable guardaFichero;
  abierto = 0;
  $display("Cerrando fichero");
  $fclose(fd);
end

initial
forever
begin : guardaFichero
  @(posedge NCLK);
  if (abierto) $fwrite(fd,"%0t ps: %b %b %b %b %b %b\n",$time,HD,VD,DEN,R,G,B);
end
```

Para comprobar el resultado usa el emulador de pantalla (**Screen Simulator**), en la barra lateral de PoliformaT. Selecciona el fichero `vga.txt`, que normalmente está en la subcarpeta **simulation/modelsim** del proyecto, y pulsa **Submit**: obtendrás la imagen resultante.

![[assets/control-pantalla/subtarea-3/screenshot.png]]

### Verificación física

Cuando la simulación sea correcta, prueba el diseño en la placa con la siguiente asignación de pines:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.56.png]]

## Apartado 3: Imagen en blanco y negro en pantalla

![[assets/control-pantalla/subtarea-3/imagen164d_2027.png]]

El objetivo es mostrar una imagen almacenada en una **memoria ROM** interna de la FPGA. Partiendo de LCD_SYNC hay que realizar el diseño del diagrama de bloques:

![[assets/control-pantalla/subtarea-3/imagen165bn.png]]

### Memoria de imagen

Se añade un bloque de memoria que contiene la imagen; cada posición guarda la información de color de un píxel. La memoria será interna de la FPGA (*on-chip*) y se crea con el **IP Catalog** de Quartus; más abajo hay una guía. Aquí se necesita una ROM.

Una **ROM** es un conjunto de celdas con datos almacenados previamente. Para leer un dato basta con indicar la dirección de la celda. Tiene, por tanto, un bus de direcciones de entrada, cuyo tamaño depende del número de celdas, y un bus de datos de salida. Las memorias internas de la FPGA son **síncronas**, así que necesitan reloj.

### Direccionamiento

Como cada posición corresponde a un píxel, la memoria se lee en el mismo orden en que se recorre la pantalla. El bloque **Direccionamiento** genera las direcciones a partir de la fila y la columna de LCD_SYNC, y su funcionamiento depende de cómo esté almacenada la imagen:

- **Direccionamiento continuo.** Los píxeles se guardan seguidos, empezando por el de la esquina superior izquierda en la dirección 0. Para una imagen de **X × Y** píxeles, la fila *r* empieza en la dirección *r* × X. Hace falta un bus de **k** bits y una memoria de al menos X × Y posiciones. Optimiza la memoria, pero complica el direccionamiento, porque Fila y Columna incluyen los *porch* y la memoria solo tiene la imagen visible.
- **Direccionamiento X-Y.** Los píxeles de cada fila se guardan seguidos, pero cada fila ocupa **2ⁿ** posiciones, la menor potencia de 2 **mayor o igual** que X. La fila *r* empieza en la dirección *r* × 2ⁿ. Por ejemplo, para 800 × 480 píxeles la segunda fila empieza en la 1024 y la tercera en la 2048. Quedan huecos sin usar, pero la dirección se obtiene simplemente **concatenando** Y y X. La memoria necesaria es de unas 2ⁿ × Y posiciones. Igual que antes, hay que descontar el *back porch*.

![[assets/control-pantalla/subtarea-3/imagen167.png]]

En este vídeo se explican los dos modos de direccionamiento y cómo calcular la dirección de un punto a partir de sus coordenadas:

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/direccionamiento-xy.mp4"></video>

### Generación del color

Por las limitaciones de memoria de la FPGA, la imagen tiene muy poca resolución de color: **1 bit por píxel**, blanco (1) o negro (0). La pantalla usa RGB de 24 bits, así que el bloque **Datos a RGB** convierte el color: genera el RGB del blanco o del negro según la memoria dé 1 o 0. Si quieres, puedes usar otros dos colores cualesquiera.

### Tarea a realizar

Realiza el diseño para mostrar una **imagen de 800 × 480 píxeles con direccionamiento X-Y y 1 bit de color**, almacenada en el fichero [[assets/control-pantalla/subtarea-3/imagen2027bn.hex|imagen2027bn.hex]].

> [!warning] Advertencias
> - Copia el fichero de inicialización (el HEX) a la carpeta del proyecto de Quartus **antes** de generar la ROM.
> - Los ficheros de inicialización de memoria no siempre se guardan por defecto en el QAR. Consulta [[sdp/es/crear-qar|Ayuda: creación de QAR]] para añadirlos a mano (**Advanced... > Add...**).

Después verifica el diseño con ModelSim y el emulador de pantalla del apartado anterior, y pruébalo en la placa.

### Cómo generar una memoria ROM

El **IP Catalog** de Quartus incluye un generador de bloques de memoria interna de varios tamaños y tipos, entre ellos la ROM de este diseño. La ROM se inicializa con los datos de la imagen mediante un fichero HEX o MIF (*Memory Initialization File*) que debe estar en la carpeta del proyecto.

La animación **Generación de una memoria ROM** muestra cómo crearla y qué opciones fijar. El punto de partida es el proyecto de Quartus.

> [!danger] Atención
> 1. La anchura de datos y el tamaño de memoria de la animación **no son los de esta aplicación**; son solo orientativos. Elige los valores según las características de la imagen.
> 2. Fíjate en qué opciones quedan marcadas al final. En particular, ***'q' output port*** debe quedar **sin marcar**.
> 3. Copia el fichero de inicialización a la carpeta del proyecto **antes** de generar la ROM.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-3/ip_rom_img_ver11/IP_ROM_Img_ver11.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

Al generar la ROM se crea, entre otros, el archivo **ROM_image_inst.v**, con un ejemplo de instanciación:

```verilog
ROM_image ROM_image_inst (
  .address ( address_sig ),
  .clock   ( clock_sig ),
  .q       ( q_sig )
);
```

## Apartado 4: Imagen en color en pantalla

![[assets/control-pantalla/subtarea-3/imagen164e_2027.png]]

El objetivo es mostrar una imagen en color. La memoria de la FPGA no da para una imagen de 800 × 480 con suficientes bits por píxel, así que se usa una imagen de **400 × 240** que sí cabe, y hay que adaptar el diseño anterior para **replicar los píxeles** y duplicar su tamaño.

![[assets/control-pantalla/subtarea-3/imagen165.png]]

El diagrama de bloques es el mismo, pero los tres bloques inferiores cambian:

- La **Memoria** tiene otros parámetros (ancho de palabra y número de palabras) y otro fichero de inicialización, con la imagen en color.
- El **Direccionamiento** debe duplicar cada píxel en horizontal y en vertical, haciendo que cada par de filas y columnas consecutivas acceda a la misma posición de memoria.
- **Datos a RGB** debe convertir la codificación del color, como se explica a continuación.

### Formato de color

Siempre que se trabaja con imágenes hay que tener en cuenta la codificación del color. Como muestra la figura, hay muchas opciones, desde 1 bit (blanco y negro) o 8 bits (escala de grises) hasta RGB de 30 bits. Cada píxel en memoria puede ocupar entre 1 y 30 bits y hay que recodificarlo al RGB de 24 bits de la pantalla. Para ello:

- Si sobran bits, elimina los de **menor peso**.
- Si faltan bits, coloca los disponibles en las posiciones de **mayor peso** y replícalos en las siguientes, de mayor a menor, hasta completar.
- Para pasar de escala de grises a color, pon el mismo valor en los tres colores.

![[assets/control-pantalla/subtarea-3/imagen166.png]]

### Tarea a realizar

Realiza el diseño para mostrar una **imagen de 400 × 240 píxeles con direccionamiento X-Y en RGB de 24 bits**, almacenada en el fichero [[assets/control-pantalla/subtarea-3/imagen2027color.hex|imagen2027color.hex]]. La pantalla muestra **800 × 480 píxeles en RGB de 24 bits**, así que el bloque de direccionamiento debe **replicar los píxeles para duplicar el tamaño de la imagen**.

Después verifica el diseño con ModelSim y el emulador de pantalla, y pruébalo en la placa.

## Apartado 5: Caracteres en pantalla

![[assets/control-pantalla/subtarea-4/imagen139.png]]

El objetivo es mostrar caracteres, en concreto llenar la pantalla con copias de un mismo carácter (por ejemplo A, B, C...). Como la pantalla se refresca constantemente, hace falta una memoria con la imagen de los caracteres. Se diseñará un módulo que lea de esa memoria la imagen del carácter según la Fila y la Columna de LCD_SYNC y actúe sobre las señales RGB para mostrarlo.

### Memoria de caracteres

Se usa otra ROM interna. Guarda las imágenes de todos los caracteres, de **8 × 8 píxeles** y 1 bit por píxel, que indica si el píxel se enciende. Cada carácter se identifica por su código ASCII de 7 bits ([tabla ASCII](https://www.asciitable.com/)), así que es una memoria de **8192 celdas de 1 bit** (128 caracteres × 8 × 8 píxeles).

![[assets/control-pantalla/subtarea-4/imagen160b.png]]

El fichero de inicialización contiene la imagen de cada carácter. La animación muestra la estructura de un fichero MIF con esas imágenes: direcciones en decimal y datos en binario, para que se entienda mejor.

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/mif_file/MIF_File.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

El fichero [[assets/control-pantalla/subtarea-4/char_rom.mif|char_rom.mif]] es un ejemplo de MIF con la definición de los caracteres; sirve para ver cómo es cada uno.

> [!warning] No uses el MIF para inicializar la memoria
> Da error al simular. Usa el fichero HEX: [[assets/control-pantalla/subtarea-4/char_rom-1.hex|char_rom-1.hex]]. Crea la ROM igual que en el apartado anterior, con los parámetros de este caso (tamaño, anchura y fichero), y **ponle otro nombre** para no sobrescribir la del apartado 3.

> [!question]- ¿Cómo se reparten los 13 bits de dirección de la ROM de caracteres?
>> [!todo] 8192 = 2¹³ celdas = 128 caracteres × 8 filas × 8 columnas: 7 bits para el código ASCII, 3 para la fila y 3 para la columna dentro del carácter.

### Estructura propuesta del diseño

Se propone el diagrama de bloques de la imagen, con tres bloques: **LCD_SYNC**, **SELEC_COLOR** y **CHAR_ROM**.

![[assets/control-pantalla/subtarea-4/imagen147c.png]]

- **LCD_SYNC** es el bloque del apartado 1.
- **SELEC_COLOR** genera las señales RGB: es un multiplexor que elige entre el color de fondo (*background*) y el de los caracteres (*foreground*) según una señal de **CHAR_ROM** que indica si el píxel es fondo o carácter.

![[assets/control-pantalla/subtarea-4/imagen149.png]]

- **CHAR_ROM** está formado por la ROM y un bloque de **Direccionamiento**, conectados como en el diagrama inferior. El direccionamiento genera la dirección a partir de Fila y Columna, y en la parte alta del bus se concatena la posición del carácter en memoria, que coincide con su código ASCII. La memoria entrega 1 bit: 0 para fondo y 1 para carácter.

![[assets/control-pantalla/subtarea-4/imagen148b.png]]

De momento, conecta un valor constante a la entrada **Caracter** de CHAR_ROM, por ejemplo `7'h30` (el número 0). Al final del apartado se cambiará para poder modificar el carácter desde Quartus.

Esta animación interactiva ilustra cómo funcionan juntos CHAR_ROM y SELEC_COLOR:

<iframe src="https://rutorcu-upvnet.github.io/SDPmuise/static/animaciones/control-pantalla/subtarea-4/funcionamiento_char_rom_ver30/Funcionamiento_Char_ROM_ver30.html" width="720" height="400" style="border:0;max-width:100%"></iframe>

### Mejora visual del diseño

Al probarlo en la placa se ve que las letras son muy pequeñas: caben **100 × 60 caracteres**, demasiados para una pantalla tan pequeña. Se pueden agrandar replicando los píxeles en horizontal y en vertical, cambiando solo el bloque de **Direccionamiento**.

Modifica el diseño para que los caracteres midan el doble, **16 × 16 píxeles**. Si aún se ven pequeños, modifícalo de nuevo para que midan **32 × 32**.

### Verificación física con el editor de contenidos de memoria

Una vez verificado en la placa, se puede cambiar el carácter en tiempo real con la herramienta de Quartus ***In-System Memory Content Editor***, que permite modificar memorias y constantes del diseño en funcionamiento si se han configurado para ello. Para ello sustituye el valor constante de la entrada **Caracter** de CHAR_ROM por un bloque **LPM_CONSTANT** del **IP Catalog**.

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/memory-content-editor-1.mp4"></video>

> [!warning] Entrega
> Usa esta herramienta para cambiar la constante de carácter con el diseño en marcha y comprueba que la pantalla se actualiza. Incluye capturas o fotos de la prueba en el informe.

## Apartado 6: Texto en pantalla

El objetivo es mostrar un texto en el centro de la pantalla; como ejemplo, los nombres de los miembros del grupo de prácticas.

![[assets/control-pantalla/subtarea-5/imagen142b.png]]

### Estructura propuesta del diseño

Se parte del diseño del apartado anterior, pero el carácter a mostrar ya no es fijo: depende de la posición en pantalla. Lo más sencillo es guardar el texto en otra ROM direccionada con Fila y Columna; el éxito del diseño depende de un direccionamiento correcto y de generar bien su fichero de inicialización.

Se propone una **memoria de pantalla** para el texto: la misma idea que para la imagen, pero con caracteres en lugar de píxeles. El diagrama muestra una propuesta:

![[assets/control-pantalla/subtarea-5/imagen173_mod.jpg]]

Se parte de la versión con caracteres de 16 × 16, así que caben **50 × 30 caracteres**. Hay que añadir una memoria (en verde) en la que cada posición contiene el carácter a mostrar. Para simplificar se usa **direccionamiento X-Y**: la posición horizontal va de 0 a 49 y la vertical de 0 a 29.

Con direccionamiento X-Y la memoria de texto tiene **1920 palabras de 7 bits** (64 × 30). Es una ROM con el texto, así que hay que crear un fichero de inicialización **MIF** con los códigos de los caracteres en sus posiciones. Como la memoria se recorre continuamente, **todas las posiciones** deben inicializarse con el código del espacio en blanco, `0` o `7'h20`.

El fichero [[assets/control-pantalla/subtarea-5/text_rom_ejemplo.mif|text_rom_ejemplo.mif]] es un ejemplo con los nombres de dos alumnos en dos líneas; puedes usarlo como punto de partida.

> [!note] Registro de retardo
> En el diagrama se ha añadido un registro para los bits inferiores de Fila y Columna, que los retrasa un ciclo de reloj. Hace falta porque la ROM de texto, a la que se accede a la vez, es síncrona y tiene un ciclo de retardo. Sin él, los campos de la dirección de la memoria de caracteres estarían desincronizados y los píxeles del borde izquierdo de cada carácter se verían mal (¡compruébalo quitando el registro!).

### Verificación física con el editor de contenidos de memoria

Una vez verificado en la placa, usa el ***In-System Memory Content Editor*** para modificar el contenido de la ROM de texto en tiempo real.

<video controls preload="metadata" style="max-width:100%" src="https://rutorcu-upvnet.github.io/SDPmuise/static/videos/memory-content-editor-2.mp4"></video>

> [!warning] Entrega
> Modifica la memoria de texto con el diseño en marcha y comprueba que el texto se actualiza en la pantalla. Incluye capturas o fotos de la prueba en el informe.

## Apartado 7 (opcional): Combinación de imagen y texto

![[assets/control-pantalla/subtarea_opcional.png]]

Se trata de unir la visualización de una imagen (apartados 3 y 4) con el texto del apartado 6 superpuesto. En la figura se ha escrito el nombre de la asignatura sobre la imagen.

**Combina los diseños anteriores para que los nombres de los miembros del grupo aparezcan sobre la imagen.** Puedes usar la imagen en color (apartado 4) o la de blanco y negro (apartado 3).

![[assets/control-pantalla/subtarea-3/imagen164f_2027.png]]

## Apartado 8 (opcional): Consola con escritura desde teclado

![[assets/control-pantalla/subtarea_opcional.png]]

Para terminar, se implementa un módulo que muestra en pantalla las teclas pulsadas en un **teclado PS/2** conectado a la placa:

![[assets/control-pantalla/subtarea-7/imagen145_rotate.png]]

No hace falta diseñar el control del teclado: los profesores proporcionan uno en [[assets/control-pantalla/subtarea-7/keyboard_demo.qar|keyboard_demo.qar]]. El módulo entrega el código de la tecla pulsada, el ***scan code***, que es único y estándar para todos los teclados.

Cada *scan code* debe traducirse al código ASCII del carácter que se quiere mostrar, que luego se usa para obtener su imagen. Hay que diseñar el módulo que hace esta decodificación:

![[assets/control-pantalla/subtarea-7/imagen146b.png]]

Por ejemplo, la tecla «A» tiene el *scan code* `8'h1C`, que debe traducirse al código ASCII `7'h41`, la posición de la «A» en la ROM de caracteres.

Se puede partir del diseño del apartado 6, cambiando la ROM de texto por una **RAM de doble puerto**: un puerto de lectura que funciona igual que antes y otro de escritura para los caracteres que llegan del teclado.

El teclado se conecta a la FPGA con dos señales generadas por el teclado sobre las que se implementa el protocolo serie PS/2: una de datos y otra de reloj para capturarlos. La tabla muestra su asignación de pines:

![[assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.31.png]]

next > [[sdp/es/proyecto3-luces-fsm|Proyecto 3: Diseño de un juego de luces mejorado]]
