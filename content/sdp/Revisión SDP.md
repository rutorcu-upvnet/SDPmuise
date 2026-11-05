---
title: Revisión de las prácticas de SDP (PoliformaT → Quartz)
draft: true
---

Informe de la migración de las Tareas 1–4 y las ayudas de Quartus/QAR de PoliformaT (DOC_34625_2026) a Markdown para Quartz. Generado el 5 de noviembre de 2026. Está marcado `draft: true` para que no se publique.

## Estructura generada

- `sdp/es/` y `sdp/en/`: una página por tarea (las subpáginas de PoliformaT pasan a ser secciones), más `index.md`, `Instalación de Quartus`/`Quartus installation` y `Crear QAR`/`Creating a QAR archive`.
- Navegación `prev >` / `next >` encadenada como en las prácticas de RISC-V.
- Las imágenes y ficheros se enlazan como `![[assets/<ruta dentro de "Contenido Lessons">]]`. Basta con copiar la carpeta **Recursos › Contenido Lessons** de PoliformaT a `content/assets/`.
- Las animaciones Tumult Hype se incrustan con `<iframe src="/static/animaciones/<ruta>">`. Hay que copiarlas (con su carpeta `*.hyperesources`) a `quartz/static/animaciones/` respetando la misma ruta.

## Pendiente antes de publicar

1. **Copiar recursos**: 127 imágenes/ficheros a `content/assets/` y 25 animaciones a `quartz/static/animaciones/` (lista al final).
2. **Rutas con «:»** (`Subtarea 1: Generación de las señales de sincronismo`, `Subtarea 1: Interface Serie...`, `Subtarea 2: Visualización...`): no son válidas en Windows y pueden dar problemas a Git/Quartz. Recomiendo renombrar esas carpetas (p. ej. quitar los dos puntos) y actualizar las rutas en los .md.
3. **Vídeos no exportables**: PoliformaT tiene 3 vídeos embebidos sin fichero accesible (uso del *In-System Memory Content Editor* en la Tarea 2, y dos de SignalTap en la Tarea 4). Están marcados con un comentario `<!-- PoliformaT: vídeo ... -->`; hay que subirlos o enlazarlos.
4. **Tests previos** (Tareas 1 y 4): el texto remite a un test de PoliformaT que no se puede enlazar desde una web pública. He dejado un aviso `[!warning] Test previo`.
5. **Enlaces de Intel** (Instalación de Quartus): los dos enlaces originales son elementos URL de PoliformaT que no pude resolver. He puesto el Intel FPGA Download Center; conviene comprobar el enlace directo a Quartus Lite 17.1.
6. **Dos «Tarea 3» visibles**: «Juego de luces mejorado con FSMs» (versión 2024, estilo *Proyecto*) y «Diseño de Máquinas de Estados Finitos» (motor paso a paso). He migrado las dos; decide cuál se publica.
7. **Screen Simulator**: se mantiene el enlace corto `https://is.gd/JtLbap`; conviene sustituirlo por la URL final.

## Correcciones técnicas

| Página | Original | Corregido / motivo |
| --- | --- | --- |
| T1 Estructura | «estructurada en cuatro subtareas» | Son **tres** subtareas. |
| T1 Subtarea 1 | `CLogB2` «con redondeo al entero más próximo» | **Redondeo hacia arriba** (techo). Con redondeo al más próximo, p. ej. N = 20 daría 4 bits y no cabe. |
| T1 Testbench | Código formateado en negrita párrafo a párrafo | Reescrito como bloque ```` ```verilog ```` (mismo código). |
| T1 Testbench | «alrededor de 20 ciclos» | Se para unos **24 ciclos** después de habilitar (`#(T*24)`), y se ven 0→19→0. |
| T1/T4 Menú | «Tools > Run Simulation Tools > Run RTL Simulation» | `Tools > Run Simulation Tool > RTL Simulation` (nombre real del menú en Quartus 17.1). |
| T2 | «2n» posibles valores / «2n por Y» | **2ⁿ** (se había perdido el superíndice). |
| T2 Direccionamiento X-Y | «potencia de 2 mayor que X» | **mayor o igual** (coincide con la versión inglesa). |
| T2 Verificación / Subtarea 2 | «cercano a los 23 ms» / «casi 23 ms» | 1056 × 525 × 40 ns = **22,18 ms**; cambiado a «unos 22 ms». |
| T2 ROM | «memorias... sincronías», «seña de reloj» | «síncronas», «señal de reloj». |
| T3 (motor) Subtarea 2 | «jugando con los diferentes botones y computadores» | «pulsadores e interruptores». |
| T4 Objetivos (EN) | «characteristics and operation modes of a **display screen**» | **touchscreen** (la ES habla de pantalla táctil). |
| T1 Verificación en placa (EN) | «the address (**Direction**)» | **direction**. |

## Erratas y redacción (ES)

modernización → modelado · «avanzando en el aprendizaje y sus de la jerarquía» → «avanzando en el uso de la jerarquía» · «Como objetivos fundamental» → «El objetivo fundamental» · «En está practica» → «En esta práctica» · «consideré» → «considere» · «Testbech» → «testbench» · «hay emplear» → «hay que emplear» · «una utilizada que permite» → «una utilidad que permite» · FGPA → FPGA · «debanados» → «devanados» · «CLa Tabla» → «La tabla» · «leguaje» → «lenguaje» · «tacando» → «tocando» · «subtrarea» → «subtarea» · «trascripción» → «transcripción» · tildes en «máquina», «módulo», «único», etc. Además se ha aligerado la redacción (frases largas partidas, listas en vez de párrafos enumerativos).

## Versión inglesa

La versión EN de PoliformaT tenía muchas frases de traducción automática. Se ha reescrito manteniendo el contenido: *meter/accounts* → *counter/counts*, *flanks* → *edges*, *end of account* → *terminal count*, *module* → *modulus*, *a used tool* → *a utility*, *it will be called Quartus* → *Quartus will open*, *Testbech*, *lighing*, *memoria*, *an inverted is used* → *an inverter*, etc. Se usa ortografía británica de forma consistente.

## Añadidos (no estaban en PoliformaT)

Todos van en *callouts* para que sean fáciles de localizar o quitar:

- T1: pregunta «¿Has evaluado todos los casos posibles?» con lista de casos; pregunta plegada con el valor de `fin_cuenta` para 0,25 s (12 500 000, 24 bits). Avisos `[!warning]` para la entrega de capturas.
- T2: pregunta plegada con la duración del *frame* (22,18 ms); pregunta plegada con el reparto de los 13 bits de la ROM de caracteres; *tip* sobre RGB565 (**suposición**: comprobar el formato de `imagen_rgb16_xy.hex`); *tip* sobre marcar *Allow In-System Memory Content Editor* al crear la ROM.
- T3 (luces): pregunta plegada sobre por qué `counter_variable` usa `>=`; *tip* sobre sobrescribir el parámetro del divisor en el testbench.
- T3 (motor): tabla de elementos del emulador (antes lista).
- T4: *tip* sobre *Storage Qualifier* de SignalTap.

## Eliminado

- T3 (motor): «Entre sus principales aplicaciones destacan como motor de frecuencia variable, motor de corriente continua sin escobillas, servomotores...». Es técnicamente confuso (un paso a paso no es una aplicación de un motor brushless). Si quieres conservarlo, conviene reformularlo.

## Dudas para el profesor

- T1 Subtarea 1: no se especifica cuándo se activa **TC** contando hacia abajo (¿en 0?). Convendría indicarlo.
- T1 Subtarea 2: la especificación del registro no dice el sentido de desplazamiento.
- T3 (luces) Apartado 1: se pide una máquina **Medvedev** (salidas = bits de estado) con 14 estados y 8 LEDs. Si la secuencia repite patrones de LEDs en la ida y la vuelta, no puede ser Medvedev pura (dos estados con la misma salida serían el mismo estado). Revisar según `Imagen06.png`.
- T2 Subtarea 1: la versión EN dice que RST_n es asíncrono y la ES no lo especifica.
- T4: «el parámetro del módulo del contador deberá ajustarse... en función de la velocidad de transmisión»: el retardo de 0,5 s no depende de la velocidad de transmisión; quizá se refiere a ajustarlo de forma empírica.

## Lista de animaciones (para `quartz/static/animaciones/`)

- `Control Pantalla/Estructura de la Tarea/indice.html`
- `Control Pantalla/Funcionamiento de la Visualizacion/Pantalla_ver13.html`
- `Control Pantalla/Objetivos/objetivos.html`
- `Control Pantalla/Propuesta Estructura Diseño/Diagrama_bloques_ver20.html`
- `Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/IP_PLL_ver11/IP_PLL_ver11.html`
- `Control Pantalla/Subtarea 3/IP_ROM_Img_ver11/IP_ROM_Img_ver11.html`
- `Control Pantalla/Subtarea 4/Funcionamiento_Char_ROM_ver30.html`
- `Control Pantalla/Subtarea 4/IP_ROM_Char_ver11/IP_ROM_Char_ver11.html`
- `Control Pantalla/Subtarea 4/MIF_File.html`
- `Disenyo FSM/Estructura_Tarea/indice.html`
- `Disenyo FSM/Objetivos/objetivos.html`
- `Disenyo FSM/SubTarea3/Diagrama_Bloques/Diagrama_bloques.html`
- `Disenyo FSM/SubTarea3/Pasos/Pasos.html`
- `Diseño de una Comunicación Serie/Estructura de la Tarea/indice.html`
- `Diseño de una Comunicación Serie/Objetivos/objetivos.html`
- `Diseño de una Comunicación Serie/Propuesta estructura diseño/Diagrama_bloques_bi/Diagrama_bloques_bi.html`
- `Diseño de una Comunicación Serie/Sugerencia, concatenación/Temporizacion_Tactil01.html`
- `Diseño de una Comunicación Serie/Verificación del Diseño/Diagrama_verificacion_bi/Diagrama_verificacion_bi.html`
- `Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Diagrama_bloques_mejora_bi/Diagrama_bloques_mejora_bi.html`
- `Secuenciales/Estrutura_Tarea/Estructura_Tarea.html`
- `Secuenciales/Objetivos/Objetivos.html`
- `Secuenciales/Verificación con Verilog HDL/ModelSim_desacoplo.html`
- `Secuenciales/Verificación con Verilog HDL/ModelSim_general.html`
- `Secuenciales/Verificación con Verilog HDL/ModelSim_restart.html`
- `Secuenciales/Verificación con Verilog HDL/ModelSim_tiempo.html`
## Lista de recursos (para `content/assets/`)

- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 13.13.13.png`
- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.31.png`
- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.56.png`
- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.31.png`
- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.53.png`
- `Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.32.44.png`
- `Control Pantalla/Diagrama Temporización Horizontal/Imagen133.png`
- `Control Pantalla/Diagrama Temporización Horizontal/Imagen135.png`
- `Control Pantalla/Diagrama Temporización Vertical/Imagen134.png`
- `Control Pantalla/Diagrama Temporización Vertical/Imagen136.png`
- `Control Pantalla/Estructura Pantalla Tactil LTM/Imagen043.png`
- `Control Pantalla/Pantalla Tactil LTM/Imagen042.png`
- `Control Pantalla/Realizar la Simulacion/Imagen116.png`
- `Control Pantalla/Representacion Imagenes/Imagen01.png`
- `Control Pantalla/Representación con Cuentas/Imagen05.png`
- `Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/Imagen051.png`
- `Control Pantalla/Subtarea 3/Captura de Pantalla 2022-09-21 a las 12.12.26.png`
- `Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.11.png`
- `Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.33.png`
- `Control Pantalla/Subtarea 3/Imagen140.png`
- `Control Pantalla/Subtarea 3/Imagen163.png`
- `Control Pantalla/Subtarea 3/Imagen164b.png`
- `Control Pantalla/Subtarea 3/Imagen165.png`
- `Control Pantalla/Subtarea 3/Imagen166.png`
- `Control Pantalla/Subtarea 3/Imagen167.png`
- `Control Pantalla/Subtarea 3/imagen_rgb16_xy.hex`
- `Control Pantalla/Subtarea 4/Imagen139.png`
- `Control Pantalla/Subtarea 4/Imagen147c.png`
- `Control Pantalla/Subtarea 4/Imagen148b.png`
- `Control Pantalla/Subtarea 4/Imagen149.png`
- `Control Pantalla/Subtarea 4/Imagen160b.png`
- `Control Pantalla/Subtarea 4/char_rom-1.mif`
- `Control Pantalla/Subtarea 4/char_rom.hex`
- `Control Pantalla/Subtarea 5/Imagen142b.png`
- `Control Pantalla/Subtarea 5/Imagen173.png`
- `Control Pantalla/Subtarea 5/text_rom_ejemplo.mif`
- `Control Pantalla/Subtarea 6/Imagen174.png`
- `Control Pantalla/Subtarea 7/Imagen145_rotate.png`
- `Control Pantalla/Subtarea 7/Imagen146.png`
- `Control Pantalla/Subtarea 7/visualiza.qar`
- `Control Pantalla/Subtarea_Opcional.png`
- `Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.17-1.png`
- `Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.48-1.png`
- `Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.16.01.png`
- `Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.17.47.png`
- `Control Pantalla/Verificación del Diseño/Imagen061.png`
- `Control Pantalla/Visualizacion en Pantalla/Imagen02.png`
- `Control Pantalla/Visualizacion en una Pantalla/2000px-AdditiveColor.png`
- `Disenyo FSM/2024/Proy3_Ap1.png`
- `Disenyo FSM/2024/Proy3_Ap2.png`
- `Disenyo FSM/2024/Proy3_Ap3.png`
- `Disenyo FSM/2024/cronograma_mealy.png`
- `Disenyo FSM/Control_Motor_PP/18866.jpg`
- `Disenyo FSM/Control_Motor_PP/Dibujos_bobinado01.png`
- `Disenyo FSM/Control_Motor_PP/Dibujos_bobinado02.png`
- `Disenyo FSM/Control_Motor_PP/Dibujos_bobinado03.png`
- `Disenyo FSM/Control_Motor_PP/Dibujos_bobinado04.png`
- `Disenyo FSM/Control_Motor_PP/Dibujos_bobinado06.png`
- `Disenyo FSM/Control_Motor_PP/stepper_motor_inside.jpg`
- `Disenyo FSM/Estructura_Tarea/Estado_FSM_Motor.png`
- `Disenyo FSM/Estructura_Tarea/Imagen01.png`
- `Disenyo FSM/Estructura_Tarea/Imagen02.png`
- `Disenyo FSM/Estructura_Tarea/Imagen07.png`
- `Disenyo FSM/Estructura_Tarea/Imagen08.png`
- `Disenyo FSM/Estructura_Tarea/Imagen09.png`
- `Disenyo FSM/Estructura_Tarea/Imagen11.png`
- `Disenyo FSM/Estructura_Tarea/Imagen12.png`
- `Disenyo FSM/Estructura_Tarea/Imagen14.png`
- `Disenyo FSM/Estructura_Tarea/Imagen15.png`
- `Disenyo FSM/Estructura_Tarea/motor_alumno.qar`
- `Diseño de una Comunicación Serie/Características _Touch_/Imagen044.png`
- `Diseño de una Comunicación Serie/Comprobación/Imagen033.png`
- `Diseño de una Comunicación Serie/Comprobación/Imagen034.png`
- `Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen047.png`
- `Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen053.png`
- `Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen054.png`
- `Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen055.png`
- `Diseño de una Comunicación Serie/Estructura Pantalla Táctil LTM/Imagen043.png`
- `Diseño de una Comunicación Serie/Pantalla Táctil LTM/Imagen042.png`
- `Diseño de una Comunicación Serie/Procedimiento/Imagen035.png`
- `Diseño de una Comunicación Serie/Procedimiento/Imagen036.png`
- `Diseño de una Comunicación Serie/Propuesta FSM/Imagen060.png`
- `Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_a.jpg`
- `Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_b.jpg`
- `Diseño de una Comunicación Serie/SignalTap/datos02.jpg`
- `Diseño de una Comunicación Serie/Subtarea 1: Interface Serie del Convertidor ADC/Imagen045.png`
- `Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen046.png`
- `Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen052.png`
- `Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Touch_alumno.qar`
- `Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen058.png`
- `Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen059.png`
- `Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen048.png`
- `Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen056.png`
- `Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen057.png`
- `Diseño de una Comunicación Serie/Verificación del Diseño/Imagen061.png`
- `Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Imagen065.png`
- `Generar QAR/Imagen009.jpg`
- `Generar QAR/Imagen011.jpg`
- `Generar QAR/Imagen012.jpg`
- `Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.30.48.png`
- `Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.40.05.png`
- `Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.41.16.png`
- `Instalar Quartus/Captura de Pantalla 2022-09-15 a las 16.23.00.png`
- `Secuenciales/Estrutura_Tarea/Captura de pantalla 2019-12-16 a las 17.18.47.png`
- `Secuenciales/Estrutura_Tarea/Captura de pantalla 2019-12-17 a las 10.14.49.png`
- `Secuenciales/Estrutura_Tarea/Captura de pantalla 2020-03-04 a las 10.12.34.png`
- `Secuenciales/Estrutura_Tarea/Imagen02.png`
- `Secuenciales/Estrutura_Tarea/Imagen04.png`
- `Secuenciales/Estrutura_Tarea/Imagen05.png`
- `Secuenciales/Estrutura_Tarea/Imagen06.png`
- `Secuenciales/Estrutura_Tarea/Imagen08.png`
- `Secuenciales/Estrutura_Tarea/MathFun.vh`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-09-17 a las 11.53.02.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-09-17 a las 11.53.11.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 15.28.34.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 15.33.02.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 16.39.47.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 16.45.40.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 17.09.20.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 17.30.43.png`
- `Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2019-12-16 a las 17.25.53.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+26-ene.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+1.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+2.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+3.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+4.png`
- `Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+5.png`