# Proyecto EaFc25

¡Bienvenido al proyecto EaFc25! Aquí podrás sumergirte en un juego de simulación futbolística, donde podrás abrir sobres, gestionar tu club, formar una plantilla y enfrentarte a otros equipos.

La aplicación está diseñada con una interfaz gráfica de usuario (GUI) que facilita la interacción con el juego a través de ventanas y botones, brindando una experiencia más visual y dinámica. Todo se maneja de forma intuitiva mediante menús y pantallas donde podrás gestionar cada aspecto de tu equipo.

## Ejecutar el Proyecto

Comienza ejecutando el archivo `main.py`. Una vez en marcha, aparecerá un menú con distintas opciones para explorar las funcionalidades del juego.

## Opciones del Menú

Al ejecutar el proyecto, se abrirá una ventana principal con un menú interactivo. Las opciones del menú son:

- Abrir Sobres
- Ver Club
- Hacer Plantilla
- Ver Plantilla
- Jugar Partido
- Salir

A continuación, te explicamos cada una de estas opciones y sus funcionalidades dentro de la interfaz gráfica.

### 1. Abrir Sobres
En esta ventana podrás abrir diferentes tipos de sobres, cada uno con su probabilidad de contener jugadores con distintas medias. Los jugadores obtenidos se añadirán automáticamente a tu club.

#### Tipos de sobres:
- **Sobre de Bronce**: Jugadores con hasta 64 de media.
- **Sobre de Plata**: Jugadores con una media entre 65 y 74.
- **Sobre de Oro**: Jugadores con una media superior a 75.
- **Sobre de Oro Promocional**: Jugadores con una media a partir de 86.

La ventana te mostrará las probabilidades de cada sobre y te permitirá abrirlos con solo hacer clic en los botones correspondientes.

### 2. Ver Club
Aquí podrás ver todos los jugadores que tienes en tu club, con sus respectivos atributos. Los jugadores se mostrarán ordenados de mayor a menor media, para facilitarte la gestión de tus recursos. Esta funcionalidad está completamente integrada en la interfaz, permitiéndote interactuar de forma visual con la lista de jugadores.

### 3. Hacer Plantilla
En esta ventana podrás construir tu plantilla ideal. A través de un sistema visual de selección podrás:

- Colocar jugadores en cada una de las posiciones disponibles.
- Ver el progreso de la plantilla en tiempo real, con una vista gráfica de los jugadores seleccionados y sus medias.
- Guardar la plantilla una vez completada, para verla posteriormente en la siguiente opción.

La interfaz te permitirá gestionar de manera fácil y rápida los jugadores que asignas a las distintas posiciones del campo.

### 4. Ver Plantilla
Visualiza la plantilla que creaste en la sección anterior. Aquí podrás revisar las decisiones tomadas y modificar los jugadores o las posiciones si es necesario, todo dentro de un entorno gráfico amigable que facilita la visualización de tu equipo.

### 5. Jugar Partido
Prepárate para enfrentarte en un partido. Necesitarás una plantilla completa para jugar, y podrás elegir entre distintos niveles de dificultad para tu rival.

#### Handicap
Como en el clásico EaFc25 (anteriormente conocido como FIFA), hemos añadido un sistema de handicap. Esto significa que, aunque tengas un equipo mucho mejor o peor que tu rival, siempre habrá una posibilidad de ganar o perder, manteniendo la experiencia emocionante y realista.

Una vez seleccionada la dificultad desde la interfaz, el juego determinará el resultado en función de tus decisiones y la calidad de tu plantilla. El resultado del partido se muestra en la misma ventana, proporcionando feedback inmediato y claro.

### 6. Salir
Termina tu sesión de juego. Al hacer clic en esta opción, la aplicación se cerrará y finalizarás tu sesión.

## Tecnologías Utilizadas

Este proyecto ha sido desarrollado utilizando Python con la librería `customtkinter` para la creación de las ventanas y la interfaz gráfica de usuario (GUI). Además, se utilizan bibliotecas como `pandas` para gestionar los datos de los jugadores y simular el juego de forma eficiente.

## Instrucciones para Ejecutar el Proyecto

### Requisitos:
- Python 3.x
- Librerías: `customtkinter`, `pandas`

### Instalación:
Para instalar las dependencias, usa el siguiente comando:

```bash
pip install customtkinter pandas

### Ejecución:
Ejecuta el programa llamado interfaces_main.py
