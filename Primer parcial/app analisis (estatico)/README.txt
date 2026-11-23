ANALISIS ESTRATEGICO 360 - Instrucciones
==========================================

Requisitos:
- Python 3.8 o superior (Tkinter viene incluido de forma estandar).

Como ejecutar:
1) Abre una terminal en la carpeta donde guardaste "analisis_estrategico.py"
2) Ejecuta:  python analisis_estrategico.py
   (en algunos sistemas es: python3 analisis_estrategico.py)

Flujo de la aplicacion:
1. Pantalla de inicio: escribe el nombre de tus 6 datos y reparte
   exactamente 50 puntos de importancia entre ellos (usando los deslizadores).
2. Panel principal: 6 botones -> Actualizar datos, FODA, 6 Sombreros,
   Ishikawa, Pareto y CATWOE. Todos se generan automaticamente con tus datos.
3. En toda pantalla hay:
   - Boton "Regresar" (esquina superior izquierda)
   - Espacio para tu logo (esquina superior derecha, circulo punteado)
   - Boton "Creador" (esquina inferior derecha) con informacion sobre ti.

Personalizacion:
- Para poner tu logo real: reemplaza el circulo punteado de la funcion
  add_logo() por una imagen con tkinter (PhotoImage).
- Para editar la seccion "Acerca del creador": modifica el texto dentro
  de la clase AboutScreen.
