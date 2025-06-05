# Trabajo Práctico – Procesamiento de Lenguaje Natural

## Análisis de Interacciones en Contact Centers con Speech Analytics y Tokenización

### Objetivo
Implementar un sistema que procese las interacciones que son comunes en un contact center, y que, utilizando técnicas de tokenización, identifique las palabras, evaluando la calidad de la comunicación y el seguimiento del protocolo de atención al cliente.

## Descripción del Trabajo Práctico

### 1. Preprocesamiento

#### 1.1 Entrada de datos (audio a texto)
Convertir una entrada de audio en transcripciones de conversaciones entre el agente y el cliente.

**Ejemplo de una conversación:**
```
Agente: Hola, bienvenido al servicio de Atención al Cliente. ¿Con quién tengo el gusto de hablar?
Cliente: Buenas, mi nombre es Juan Arias, quiero hacer una consulta acerca de mi factura.
...
```

#### 1.2 Sobre la recopilación de Datos de Audio
- Recolecta o utiliza un conjunto de datos de llamadas de centros de contacto enfocadas en asistencia técnica. Estas llamadas deben involucrar conversaciones entre un cliente y un agente.
- Los formatos de audio pueden obtenerse de conjuntos de datos públicos (como el conjunto de datos de Call Center AI de IBM) o simulando conversaciones con voces sintéticas o reales entre personas anónimas.
- Las llamadas deben cubrir varios casos de sentimiento (resolución positiva, sin resolver/neutro o negativo/con muchas quejas).

#### 1.3 Conversión de Voz a Texto
Utiliza un motor de reconocimiento de voz para transcribir las grabaciones de audio en texto. Las opciones incluyen:
1. Google Speech-to-Text API
2. DeepSpeech
3. Amazon Transcribe
4. Otro de tu preferencia. Buscar en la tienda de aplicaciones de uso frecuente.

> **Nota:** Asegúrate de que el sistema de reconocimiento de voz sea lo robusto para manejar el típico ruido de los centros de contacto.

### 2. Tokenización
Implementa un tokenizador para segmentar la transcripción en palabras. La misión principal del tokenizador es poder dividir un ejemplo de entrada en palabras o lexemas y catalogarlas según un criterio o patrón.

Esta parte puede ser diseñada utilizando estructuras como autómatas finitos y aplicando los conceptos del análisis léxico. 

> **Observación:** Es muy probable que muchas de las técnicas vistas no puedan aplicarse sino que deberán utilizarse el background conceptual que ellas aportan para definir un curso de acción.

**Ejemplo:**
```
Lexemas detectados: ["Hola", "bienvenido", "a", "Atención", "al", "Cliente", ...]
```

Cada uno de ellos son identificados como un token de acuerdo a patrones definidos.

#### 2.1 Detección de lexemas
Se tiene que contar con una base de datos (tabla de símbolos) con palabras válidas en español y que sirva para contrastar con un lexema que se identifica en la entrada. Si la palabra no se encuentra dentro de la base de datos se deberá:

- Desplegar la palabra candidata a lexema
- Preguntar si la misma es un lexema válido y a que token pertenece y la puntuación como resultado del análisis de sentimiento
- Si no es un lexema válido, probablemente se trate de un error de entrada por lo que se debe sugerir lexemas que podrían reemplazar a la palabra encontrada basándose en las técnicas de:
  - Distancia mínima de edición usando la distancia de Levensthein
  - Distancia Hamming usando vacío para igual longitud de palabras

### 3. Fase de Análisis – Speech Analytics

#### 3.1 Análisis de Sentimiento
Carga una tabla de símbolos que asigna una puntuación a cada palabra dependiendo de si es positiva o negativa.

**Ejemplo de tabla de símbolos (palabras con ponderación):**

| Lexema    | Ponderación |
|-----------|-------------|
| bueno     | +1          |
| amable    | +2          |
| problema  | -1          |
| mal       | -2          |
| excelente | +3          |
| fatal     | -3          |

**Cálculo:**
Por cada palabra en la conversación, suma o resta la ponderación para determinar si la interacción es mayormente positiva o negativa.

> **Resultado esperado:** El método simple de cálculo permite establecer que si la puntuación acumulada es positiva, la conversación fue mayormente positiva. Si es negativa, fue una mala interacción.

#### 3.2 Verificación del Protocolo de Atención
Implementa una verificación basada en la detección de ciertas palabras claves para asegurarse de que el agente sigue el protocolo de atención. El protocolo debe incluir:

- **Fase de saludo:** Detectar si el agente realiza una bienvenida (ejemplo: "Hola", "Buen día" son lexemas que pueden pertenecer a un token saludo inicial).
- **Identificación del cliente:** Verificar si el agente pide la identificación del cliente (ejemplo: "¿Con quién tengo el gusto de hablar?").
- **No usar palabras rudas o prohibidas:** Verificar el agente de atención al cliente que no se use palabras rudas, como "inútil", "tonto" y otras son lexemas que pueden pertenecer a la categoría o token palabras no permitidas.
- **Despedida amable:** Comprobar que el agente cierre la conversación de manera cortés (ejemplo: "Gracias por su tiempo", "Que tenga un buen día").

#### 3.3 Implementación con Tokenización
En este paso, utiliza la tokenización como estrategia para recorrer las palabras y asegurarte de que el protocolo se cumple.

**Ejemplo de protocolo seguido:**
```
"Hola, bienvenido a Atención al Cliente..." -> Es una fase de saludo OK
"¿Con quién tengo el gusto?" -> Es un pedido de identificación del cliente OK
...
```

### 4. Resultados y Reporte

#### 4.1 Detección de Sentimiento
Mostrar un reporte indicando si la conversación fue positiva, neutral o negativa, en base a las palabras identificadas y la ponderación final.

**Ejemplo de output:**
```
Sentimiento general: Positivo (+5)
Palabras positivas: 6
Palabra más positiva: amable, +2
Palabras negativas: 2
Palabra más negativa: mal, -2
```

#### 4.2 Verificación del Protocolo de Atención
Indicar si el agente siguió el protocolo y, en caso de no hacerlo, mostrar en que falló u omitió.

**Ejemplo de output:**
```
Fase de saludo: OK
Identificación del cliente: OK
Uso de palabras rudas: Ninguna detectada
Despedida amable: Faltante
```

## Términos y condiciones

### Entregables:
a. Un documento en PDF donde:
1. se describa el trabajo práctico, las decisiones adoptadas, mejoras y todo lo que contribuya a definir el alcance y estrategias aplicadas.
2. El código fuente.
3. El resultado para un caso de ejemplo.
4. Cualquier observación sobre el funcionamiento o situaciones no resueltas o no contempladas.

b. La defensa del trabajo práctico es presencial y no puede recuperarse. Es requisito para rendir el examen final. En caso de ausencia no se aceptará la entrega en forma electrónica sin defensa.

Al finalizar el trabajo, se comprenderá el impacto que se tiene en utilizar el 
analizador léxico como herramienta de procesamiento de lenguajes naturales. 
En forma simétrica y comparando, se podrán generar corolarios en la convenicia 
de utilización del analizador léxico o sintáctico como protagonista de una 
estrategia de procesamiento de lenguaje y el rol de un tokenizador para el 
análisis de la entrada de datos. 

## Evaluación
El proceso de evaluación tendrá en cuenta:
a. Una parte práctica, que se basa en la defensa del trabajo práctico, donde se presentará sus funcionalidades y ejemplos con cadenas para procesar. Se evaluará su eficiencia y su correcto funcionamiento y validaciones. La interface es opcional.
b. Una parte teórica, donde se evalúa el contenido del documento PDF base del trabajo práctico y el algoritmo obtenido.

## Observaciones
a. El trabajo práctico no es recuperable.
b. Fecha de entrega: la entrega se desarrollará en la semana entre el segundo parcial y el inicio de los exámenes finales. Cada alumno dispondrá de hasta un máximo de 15 minutos para la defensa del TP.
c. El trabajo práctico se debe realizar en forma individual o en grupo de hasta dos personas. 