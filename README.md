# Proyecto de TFG: Estudio de LLM's aplicados a control de drones autónomos

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Motivación](#motivación)
3. [Idea del Proyecto](#idea-del-proyecto)
4. [Fases del Proyecto](#fases-del-proyecto)
5. [Diagrama de Componentes](#diagrama-de-componentes)
6. [Funcionamiento del Sistema](#funcionamiento-del-sistema)
7. [Referencias](#referencias)

## Introducción

Con esta idea para el TFG planteo un sistema para que un LLM controle un dron mediante texto con el fin de que realice 
tareas complejas, como encontrar tarjetas en un edificio simulado o seguir objetivos en movimiento.

## Motivación

Quería hacer un TFG sobre Inteligencia Artificial para llevar al límite todo lo que he aprendido en estos años sobre 
machine learning y programación.

La idea de este proyecto se basa en el paper 
"[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://voyager.minedojo.org/)", en el que se 
estudia cómo un LLM aprende a jugar a Minecraft sin ayuda externa, más allá de la definición de objetivos. 
En el caso de Voyager se usan tres elementos:
1. Un Currículum Automático que gestiona los logros y los objetivos del agente.
2. Un Mecanismo de Prompting Iterativo que interactúa con el LLM y le permite definir posibles nuevas habilidades y recibir información del entorno.
3. Una Biblioteca de Habilidades que permite reutilizar conocimiento anterior del agente en forma de habilidades programadas.

![Componentes de Voyager](docs/images/Voyager_Components.png)

## Idea del Proyecto

La idea principal es entrenar un LLM a pilotar un dron dentro de una simulación para realizar tareas complejas como 
seguir un objetivo en movimiento o encontrar objetos escondidos dentro de la simulación.

Para este caso he pensado en una estructura un poco distinta a la propuesta para Voyager (ver [Motivación](#motivación)), 
se basa en tres componentes (contando el LLM):
1. Un Currículum Automático, que contiene las posibles tareas del dron, establece distintos circuitos (para evitar el olvido catastrófico) y evalúa el trabajo del agente.
2. Una Interfaz de Vuelo, que contiene una serie de acciones que puede realizar el LLM para controlar el dron, como despegar, aterrizar, rotar, etc.
3. Un LLM que será un modelo open source que pueda entrenarse para este problema específico.

![Componentes Drone TFG](docs/images/Drone_Components.png)

## Fases del Proyecto

Soy consciente de que puede ser complicado llevar a cabo un proyecto así por mi cuenta, pero considero que la creación 
de la Interfaz de Vuelo podría ser un reto suficiente.

##### Fases
1. Desarrollar la Interfaz de Vuelo.
2. Desarrollar el Currículum Automático.
3. Entrenar el LLM.


Para la Interfaz de Vuelo usaré una red neuronal que aprenda a realizar las acciones complejas asociadas a sus funciones. 
Para las imágenes de la cámara, usaré un modelo ya entrenado para detectar objetos y su distancia relativa, 
logrando una interfaz de texto para el LLM.

Posteriormente, el currículum se programará con todas las pruebas y 
la forma en que encadenará las acciones. 

Finalmente, se buscará una forma de entrenar el modelo con vuelos realizados 
por una persona mediante una interfaz para el piloto.

## Funcionamiento del Sistema
### Diagrama de Componentes

![Component Diagram](docs/images/component_diagram.png)

Este diagrama muestra cómo se puede entrenar la Interfaz de Vuelo de manera descentralizada mediante aprendizaje 
reforzado, utilizando algoritmos como PPO o A3C, o incluso un algoritmo evolutivo como NEAT.


### Nodo Central

- Coordina los nodos trabajadores y recoge los resultados de cada entrenamiento para obtener el mejor modelo después de varias iteraciones.
- Contiene un módulo de gestión del entrenamiento distribuido, un módulo de gestión de información con servicios como MongoDB y Prometheus, y un módulo de comunicación con los nodos trabajadores.

### Nodos Trabajadores

- Comunicación con el nodo central.
- Gestión del entrenamiento a nivel local, permitiendo ejecutar varias simulaciones simultáneamente.
- Gestión de modelos recibidos del nodo central.
- Definición de pruebas para el entrenamiento individual.
- Comunicación con el simulador Webots para controlar la simulación y el dron.

### Nodo Extra

- Puede estar en el mismo equipo que el nodo central o en un servicio cloud.
- Persistencia de modelos a medio entrenar, modelos entrenados y metadatos del entrenamiento con MongoDB.
- Servicio de monitorización con Grafana y Prometheus para seguir el progreso del entrenamiento.

### Flujo de Datos

Explica el flujo de datos a través del sistema, desde la entrada hasta la salida final.

### Tecnologías Utilizadas

- **Programas y Software Externo**
  - Webots: Para la simulación del dron en un entorno 3D.
  - MongoDB: Para la persistencia de los modelos.
  - Prometheus: Para la recogida de los datos de entrenamiento.
  - Grafana: Para la monitorización del entrenamiento. 

- **Lenguajes de Programación**
  - Python
  - Java?

- **Librerías**
  - Ray: Para el entrenamiento distribuido y la comunicación entre nodos.
  - Tensorflow: Para la creación de modelos de Deep Learning.
  - NEAT Python: Para aplicar un algoritmo evolutivo al Deep Learning.
  - Pymongo: Para comunicarnos con la base de datos MongoDB.
  - Prometheus_client: Para comunicarnos con Prometheus para los datos de monitorización. 

## Referencias

- Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., & Anandkumar, A. (2023). 
 Voyager: An Open-Ended Embodied Agent with Large Language Models. *arXiv preprint arXiv:2305.16291*. 
Disponible en: [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)

## Contacto

- **Email:** j.esteban.rincon.m@gmail.com
- **University Email:** juanesteban.rincon@alumnos.upm.es
- **GitHub:** [Esk1z0](https://github.com/Esk1z0)
