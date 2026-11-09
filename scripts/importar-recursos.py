#!/usr/bin/env python3
"""Copia los recursos de PoliformaT al repo con nombres ASCII.

Uso:  python3 scripts/importar-recursos.py "/ruta/a/Contenido Lessons"

La carpeta es la que se descarga de PoliformaT > Recursos > Contenido Lessons.
Los nombres se comparan sin distinguir mayúsculas ni la forma Unicode de las
tildes (macOS las guarda descompuestas), así que no hace falta renombrar nada.
"""
import os, sys, shutil, unicodedata

ASSETS = {
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 13.13.13.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.31.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.56.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.56.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.31.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.31.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.53.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.53.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.32.44.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.32.44.png",
 "Control Pantalla/Diagrama Temporización Horizontal/Imagen133.png": "assets/control-pantalla/diagrama-temporizacion-horizontal/imagen133.png",
 "Control Pantalla/Diagrama Temporización Horizontal/Imagen135.png": "assets/control-pantalla/diagrama-temporizacion-horizontal/imagen135.png",
 "Control Pantalla/Diagrama Temporización Vertical/Imagen134.png": "assets/control-pantalla/diagrama-temporizacion-vertical/imagen134.png",
 "Control Pantalla/Diagrama Temporización Vertical/Imagen136.png": "assets/control-pantalla/diagrama-temporizacion-vertical/imagen136.png",
 "Control Pantalla/Estructura Pantalla Tactil LTM/Imagen043.png": "assets/control-pantalla/estructura-pantalla-tactil-ltm/imagen043.png",
 "Control Pantalla/Pantalla Tactil LTM/Imagen042.png": "assets/control-pantalla/pantalla-tactil-ltm/imagen042.png",
 "Control Pantalla/Realizar la Simulacion/Imagen116.png": "assets/control-pantalla/realizar-la-simulacion/imagen116.png",
 "Control Pantalla/Representacion Imagenes/Imagen01.png": "assets/control-pantalla/representacion-imagenes/imagen01.png",
 "Control Pantalla/Representación con Cuentas/Imagen05.png": "assets/control-pantalla/representacion-con-cuentas/imagen05.png",
 "Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/Imagen051.png": "assets/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/imagen051.png",
 "Control Pantalla/Subtarea 3/Captura de Pantalla 2022-09-21 a las 12.12.26.png": "assets/control-pantalla/subtarea-3/captura-de-pantalla-2022-09-21-a-las-12.12.26.png",
 "Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.11.png": "assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.11.png",
 "Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.33.png": "assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.33.png",
 "Control Pantalla/Subtarea 3/Imagen140.png": "assets/control-pantalla/subtarea-3/imagen140.png",
 "Control Pantalla/Subtarea 3/Imagen163.png": "assets/control-pantalla/subtarea-3/imagen163.png",
 "Control Pantalla/Subtarea 3/Imagen164b.png": "assets/control-pantalla/subtarea-3/imagen164b.png",
 "Control Pantalla/Subtarea 3/Imagen165.png": "assets/control-pantalla/subtarea-3/imagen165.png",
 "Control Pantalla/Subtarea 3/Imagen166.png": "assets/control-pantalla/subtarea-3/imagen166.png",
 "Control Pantalla/Subtarea 3/Imagen167.png": "assets/control-pantalla/subtarea-3/imagen167.png",
 "Control Pantalla/Subtarea 3/imagen_rgb16_xy.hex": "assets/control-pantalla/subtarea-3/imagen_rgb16_xy.hex",
 "Control Pantalla/Subtarea 4/Imagen139.png": "assets/control-pantalla/subtarea-4/imagen139.png",
 "Control Pantalla/Subtarea 4/Imagen147c.png": "assets/control-pantalla/subtarea-4/imagen147c.png",
 "Control Pantalla/Subtarea 4/Imagen148b.png": "assets/control-pantalla/subtarea-4/imagen148b.png",
 "Control Pantalla/Subtarea 4/Imagen149.png": "assets/control-pantalla/subtarea-4/imagen149.png",
 "Control Pantalla/Subtarea 4/Imagen160b.png": "assets/control-pantalla/subtarea-4/imagen160b.png",
 "Control Pantalla/Subtarea 4/char_rom-1.mif": "assets/control-pantalla/subtarea-4/char_rom-1.mif",
 "Control Pantalla/Subtarea 4/char_rom.hex": "assets/control-pantalla/subtarea-4/char_rom.hex",
 "Control Pantalla/Subtarea 5/Imagen142b.png": "assets/control-pantalla/subtarea-5/imagen142b.png",
 "Control Pantalla/Subtarea 5/Imagen173.png": "assets/control-pantalla/subtarea-5/imagen173.png",
 "Control Pantalla/Subtarea 5/text_rom_ejemplo.mif": "assets/control-pantalla/subtarea-5/text_rom_ejemplo.mif",
 "Control Pantalla/Subtarea 6/Imagen174.png": "assets/control-pantalla/subtarea-6/imagen174.png",
 "Control Pantalla/Subtarea 7/Imagen145_rotate.png": "assets/control-pantalla/subtarea-7/imagen145_rotate.png",
 "Control Pantalla/Subtarea 7/Imagen146.png": "assets/control-pantalla/subtarea-7/imagen146.png",
 "Control Pantalla/Subtarea 7/visualiza.qar": "assets/control-pantalla/subtarea-7/visualiza.qar",
 "Control Pantalla/Subtarea_Opcional.png": "assets/control-pantalla/subtarea_opcional.png",
 "Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.17-1.png": "assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.05.17-1.png",
 "Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.05.48-1.png": "assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.05.48-1.png",
 "Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.16.01.png": "assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.16.01.png",
 "Control Pantalla/Verificación del Diseño/Captura de pantalla 2018-12-12 a las 17.17.47.png": "assets/control-pantalla/verificacion-del-diseno/captura-de-pantalla-2018-12-12-a-las-17.17.47.png",
 "Control Pantalla/Verificación del Diseño/Imagen061.png": "assets/control-pantalla/verificacion-del-diseno/imagen061.png",
 "Control Pantalla/Visualizacion en Pantalla/Imagen02.png": "assets/control-pantalla/visualizacion-en-pantalla/imagen02.png",
 "Control Pantalla/Visualizacion en una Pantalla/2000px-AdditiveColor.png": "assets/control-pantalla/visualizacion-en-una-pantalla/2000px-additivecolor.png",
 "Disenyo FSM/2024/Proy3_Ap1.png": "assets/disenyo-fsm/2024/proy3_ap1.png",
 "Disenyo FSM/2024/Proy3_Ap2.png": "assets/disenyo-fsm/2024/proy3_ap2.png",
 "Disenyo FSM/2024/Proy3_Ap3.png": "assets/disenyo-fsm/2024/proy3_ap3.png",
 "Disenyo FSM/2024/cronograma_mealy.png": "assets/disenyo-fsm/2024/cronograma_mealy.png",
 "Disenyo FSM/Control_Motor_PP/18866.jpg": "assets/disenyo-fsm/control_motor_pp/18866.jpg",
 "Disenyo FSM/Control_Motor_PP/Dibujos_bobinado01.png": "assets/disenyo-fsm/control_motor_pp/dibujos_bobinado01.png",
 "Disenyo FSM/Control_Motor_PP/Dibujos_bobinado02.png": "assets/disenyo-fsm/control_motor_pp/dibujos_bobinado02.png",
 "Disenyo FSM/Control_Motor_PP/Dibujos_bobinado03.png": "assets/disenyo-fsm/control_motor_pp/dibujos_bobinado03.png",
 "Disenyo FSM/Control_Motor_PP/Dibujos_bobinado04.png": "assets/disenyo-fsm/control_motor_pp/dibujos_bobinado04.png",
 "Disenyo FSM/Control_Motor_PP/Dibujos_bobinado06.png": "assets/disenyo-fsm/control_motor_pp/dibujos_bobinado06.png",
 "Disenyo FSM/Control_Motor_PP/stepper_motor_inside.jpg": "assets/disenyo-fsm/control_motor_pp/stepper_motor_inside.jpg",
 "Disenyo FSM/Estructura_Tarea/Estado_FSM_Motor.png": "assets/disenyo-fsm/estructura_tarea/estado_fsm_motor.png",
 "Disenyo FSM/Estructura_Tarea/Imagen01.png": "assets/disenyo-fsm/estructura_tarea/imagen01.png",
 "Disenyo FSM/Estructura_Tarea/Imagen02.png": "assets/disenyo-fsm/estructura_tarea/imagen02.png",
 "Disenyo FSM/Estructura_Tarea/Imagen07.png": "assets/disenyo-fsm/estructura_tarea/imagen07.png",
 "Disenyo FSM/Estructura_Tarea/Imagen08.png": "assets/disenyo-fsm/estructura_tarea/imagen08.png",
 "Disenyo FSM/Estructura_Tarea/Imagen09.png": "assets/disenyo-fsm/estructura_tarea/imagen09.png",
 "Disenyo FSM/Estructura_Tarea/Imagen11.png": "assets/disenyo-fsm/estructura_tarea/imagen11.png",
 "Disenyo FSM/Estructura_Tarea/Imagen12.png": "assets/disenyo-fsm/estructura_tarea/imagen12.png",
 "Disenyo FSM/Estructura_Tarea/Imagen14.png": "assets/disenyo-fsm/estructura_tarea/imagen14.png",
 "Disenyo FSM/Estructura_Tarea/Imagen15.png": "assets/disenyo-fsm/estructura_tarea/imagen15.png",
 "Disenyo FSM/Estructura_Tarea/motor_alumno.qar": "assets/disenyo-fsm/estructura_tarea/motor_alumno.qar",
 "Diseño de una Comunicación Serie/Características _Touch_/Imagen044.png": "assets/diseno-de-una-comunicacion-serie/caracteristicas-_touch_/imagen044.png",
 "Diseño de una Comunicación Serie/Comprobación/Imagen033.png": "assets/diseno-de-una-comunicacion-serie/comprobacion/imagen033.png",
 "Diseño de una Comunicación Serie/Comprobación/Imagen034.png": "assets/diseno-de-una-comunicacion-serie/comprobacion/imagen034.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen047.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen047.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen053.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen053.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen054.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen054.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen055.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen055.png",
 "Diseño de una Comunicación Serie/Estructura Pantalla Táctil LTM/Imagen043.png": "assets/diseno-de-una-comunicacion-serie/estructura-pantalla-tactil-ltm/imagen043.png",
 "Diseño de una Comunicación Serie/Pantalla Táctil LTM/Imagen042.png": "assets/diseno-de-una-comunicacion-serie/pantalla-tactil-ltm/imagen042.png",
 "Diseño de una Comunicación Serie/Procedimiento/Imagen035.png": "assets/diseno-de-una-comunicacion-serie/procedimiento/imagen035.png",
 "Diseño de una Comunicación Serie/Procedimiento/Imagen036.png": "assets/diseno-de-una-comunicacion-serie/procedimiento/imagen036.png",
 "Diseño de una Comunicación Serie/Propuesta FSM/Imagen060.png": "assets/diseno-de-una-comunicacion-serie/propuesta-fsm/imagen060.png",
 "Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_a.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_a.jpg",
 "Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_b.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_b.jpg",
 "Diseño de una Comunicación Serie/SignalTap/datos02.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/datos02.jpg",
 "Diseño de una Comunicación Serie/Subtarea 1: Interface Serie del Convertidor ADC/Imagen045.png": "assets/diseno-de-una-comunicacion-serie/subtarea-1-interface-serie-del-convertidor-adc/imagen045.png",
 "Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen046.png": "assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen046.png",
 "Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen052.png": "assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen052.png",
 "Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Touch_alumno.qar": "assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/touch_alumno.qar",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen058.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen058.png",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen059.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen059.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen048.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen048.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen056.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen056.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen057.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen057.png",
 "Diseño de una Comunicación Serie/Verificación del Diseño/Imagen061.png": "assets/diseno-de-una-comunicacion-serie/verificacion-del-diseno/imagen061.png",
 "Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Imagen065.png": "assets/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/imagen065.png",
 "Generar QAR/Imagen009.jpg": "assets/generar-qar/imagen009.jpg",
 "Generar QAR/Imagen011.jpg": "assets/generar-qar/imagen011.jpg",
 "Generar QAR/Imagen012.jpg": "assets/generar-qar/imagen012.jpg",
 "Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.30.48.png": "assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.30.48.png",
 "Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.40.05.png": "assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.40.05.png",
 "Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.41.16.png": "assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-15.41.16.png",
 "Instalar Quartus/Captura de Pantalla 2022-09-15 a las 16.23.00.png": "assets/instalar-quartus/captura-de-pantalla-2022-09-15-a-las-16.23.00.png",
 "Secuenciales/Estrutura_Tarea/Captura de pantalla 2019-12-16 a las 17.18.47.png": "assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-16-a-las-17.18.47.png",
 "Secuenciales/Estrutura_Tarea/Captura de pantalla 2019-12-17 a las 10.14.49.png": "assets/secuenciales/estrutura_tarea/captura-de-pantalla-2019-12-17-a-las-10.14.49.png",
 "Secuenciales/Estrutura_Tarea/Captura de pantalla 2020-03-04 a las 10.12.34.png": "assets/secuenciales/estrutura_tarea/captura-de-pantalla-2020-03-04-a-las-10.12.34.png",
 "Secuenciales/Estrutura_Tarea/Imagen02.png": "assets/secuenciales/estrutura_tarea/imagen02.png",
 "Secuenciales/Estrutura_Tarea/Imagen04.png": "assets/secuenciales/estrutura_tarea/imagen04.png",
 "Secuenciales/Estrutura_Tarea/Imagen05.png": "assets/secuenciales/estrutura_tarea/imagen05.png",
 "Secuenciales/Estrutura_Tarea/Imagen06.png": "assets/secuenciales/estrutura_tarea/imagen06.png",
 "Secuenciales/Estrutura_Tarea/Imagen08.png": "assets/secuenciales/estrutura_tarea/imagen08.png",
 "Secuenciales/Estrutura_Tarea/MathFun.vh": "assets/secuenciales/estrutura_tarea/mathfun.vh",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-09-17 a las 11.53.02.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.02.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-09-17 a las 11.53.11.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-09-17-a-las-11.53.11.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 15.28.34.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.28.34.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 15.33.02.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-15.33.02.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 16.39.47.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.39.47.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 16.45.40.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-16.45.40.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 17.09.20.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.09.20.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 17.30.43.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2019-12-16 a las 17.25.53.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2019-12-16-a-las-17.25.53.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+26-ene.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-26-ene.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+1.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+2.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-2.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+3.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-3.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+4.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-4.png",
 "Secuenciales/Verificación con Verilog HDL/Captura+ST1-3+5.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5.png"
}
ANIMS = {
 "Control Pantalla/Estructura de la Tarea/indice.html": "quartz/static/animaciones/control-pantalla/estructura-de-la-tarea/indice.html",
 "Control Pantalla/Funcionamiento de la Visualizacion/Pantalla_ver13.html": "quartz/static/animaciones/control-pantalla/funcionamiento-de-la-visualizacion/Pantalla_ver13.html",
 "Control Pantalla/Objetivos/objetivos.html": "quartz/static/animaciones/control-pantalla/objetivos/objetivos.html",
 "Control Pantalla/Propuesta Estructura Diseño/Diagrama_bloques_ver20.html": "quartz/static/animaciones/control-pantalla/propuesta-estructura-diseno/Diagrama_bloques_ver20.html",
 "Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/IP_PLL_ver11/IP_PLL_ver11.html": "quartz/static/animaciones/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/ip_pll_ver11/IP_PLL_ver11.html",
 "Control Pantalla/Subtarea 3/IP_ROM_Img_ver11/IP_ROM_Img_ver11.html": "quartz/static/animaciones/control-pantalla/subtarea-3/ip_rom_img_ver11/IP_ROM_Img_ver11.html",
 "Control Pantalla/Subtarea 4/Funcionamiento_Char_ROM_ver30.html": "quartz/static/animaciones/control-pantalla/subtarea-4/Funcionamiento_Char_ROM_ver30.html",
 "Control Pantalla/Subtarea 4/IP_ROM_Char_ver11/IP_ROM_Char_ver11.html": "quartz/static/animaciones/control-pantalla/subtarea-4/ip_rom_char_ver11/IP_ROM_Char_ver11.html",
 "Control Pantalla/Subtarea 4/MIF_File.html": "quartz/static/animaciones/control-pantalla/subtarea-4/MIF_File.html",
 "Disenyo FSM/Estructura_Tarea/indice.html": "quartz/static/animaciones/disenyo-fsm/estructura_tarea/indice.html",
 "Disenyo FSM/Objetivos/objetivos.html": "quartz/static/animaciones/disenyo-fsm/objetivos/objetivos.html",
 "Disenyo FSM/SubTarea3/Diagrama_Bloques/Diagrama_bloques.html": "quartz/static/animaciones/disenyo-fsm/subtarea3/diagrama_bloques/Diagrama_bloques.html",
 "Disenyo FSM/SubTarea3/Pasos/Pasos.html": "quartz/static/animaciones/disenyo-fsm/subtarea3/pasos/Pasos.html",
 "Diseño de una Comunicación Serie/Estructura de la Tarea/indice.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/estructura-de-la-tarea/indice.html",
 "Diseño de una Comunicación Serie/Objetivos/objetivos.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/objetivos/objetivos.html",
 "Diseño de una Comunicación Serie/Propuesta estructura diseño/Diagrama_bloques_bi/Diagrama_bloques_bi.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/propuesta-estructura-diseno/diagrama_bloques_bi/Diagrama_bloques_bi.html",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Temporizacion_Tactil01.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/Temporizacion_Tactil01.html",
 "Diseño de una Comunicación Serie/Verificación del Diseño/Diagrama_verificacion_bi/Diagrama_verificacion_bi.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-del-diseno/diagrama_verificacion_bi/Diagrama_verificacion_bi.html",
 "Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Diagrama_bloques_mejora_bi/Diagrama_bloques_mejora_bi.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/diagrama_bloques_mejora_bi/Diagrama_bloques_mejora_bi.html",
 "Secuenciales/Estrutura_Tarea/Estructura_Tarea.html": "quartz/static/animaciones/secuenciales/estrutura_tarea/Estructura_Tarea.html",
 "Secuenciales/Objetivos/Objetivos.html": "quartz/static/animaciones/secuenciales/objetivos/Objetivos.html",
 "Secuenciales/Verificación con Verilog HDL/ModelSim_desacoplo.html": "quartz/static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_desacoplo.html",
 "Secuenciales/Verificación con Verilog HDL/ModelSim_general.html": "quartz/static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_general.html",
 "Secuenciales/Verificación con Verilog HDL/ModelSim_restart.html": "quartz/static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_restart.html",
 "Secuenciales/Verificación con Verilog HDL/ModelSim_tiempo.html": "quartz/static/animaciones/secuenciales/verificacion-con-verilog-hdl/ModelSim_tiempo.html"
}

def key(p):
    return unicodedata.normalize("NFC", p).replace("\\", "/").lower()

def main(src):
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index = {}
    for root, _, files in os.walk(src):
        for f in files:
            full = os.path.join(root, f)
            index[key(os.path.relpath(full, src))] = full
    missing = []
    for orig, dst in ASSETS.items():
        f = index.get(key(orig))
        if not f:
            missing.append(orig); continue
        out = os.path.join(repo, "content", dst)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(f, out)
    for orig, dst in ANIMS.items():
        f = index.get(key(orig))
        if not f:
            missing.append(orig); continue
        out = os.path.join(repo, dst)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(f, out)
        # carpeta de recursos de Tumult Hype (Nombre.hyperesources)
        res = os.path.splitext(f)[0] + ".hyperesources"
        if os.path.isdir(res):
            shutil.copytree(res, os.path.splitext(out)[0] + ".hyperesources", dirs_exist_ok=True)
        else:
            missing.append(os.path.splitext(orig)[0] + ".hyperesources/")
    print(f"Copiados {len(ASSETS)+len(ANIMS)-len(missing)} de {len(ASSETS)+len(ANIMS)}.")
    if missing:
        print("No encontrados:")
        for m in missing: print("  -", m)

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
