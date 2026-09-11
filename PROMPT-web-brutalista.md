# Volcano Fitness — Prompt web (dirección brutalista deportiva)

> Derivado de https://fit-and-you.webflow.io/ (template Webflow de Nata Stelmakh).
> Valores de color y tipografía extraídos del CSS real del sitio, no estimados a ojo.
> El acento naranja #FB5607 del original está mapeado al azul eléctrico de la marca Volcano.
> Pegar en Lovable, Bolt, v0 o Claude.

---

Construí el sitio de un gimnasio llamado "Volcano Fitness" en La Falda, Córdoba, Argentina,
usando React + Vite + TypeScript + Tailwind CSS + Framer Motion (motion/react) + lucide-react.
Todo el copy va en español rioplatense (voseo). Tono: directo, con energía, nada solemne.

## Sistema de diseño

### Colores
```css
:root {
  --bg:            #000000;  /* negro puro, fondo dominante */
  --surface:       #111111;  /* tarjetas y bloques */
  --surface-raised:#1B1B1B;  /* hover de tarjetas */
  --foreground:    #F8F8F8;  /* texto principal, blanco apagado */
  --muted:         #565656;  /* texto secundario */
  --border:        #222222;
  --accent:        #1E6BFF;  /* AZUL ELÉCTRICO — color del logo del volcán */
  --accent-soft:   rgba(30, 107, 255, 0.15);
  --gold:          #D9A441;  /* sol argentino de las remeras, uso MUY puntual */
  --invert-bg:     #FFFFFF;  /* fondo de la tarjeta destacada */
}
```
El azul es el único color saturado de la paleta. Nada de degradés: color plano siempre.

### Tipografía
- Import: `https://fonts.googleapis.com/css2?family=Antonio:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap`
- Titulares: **Antonio 700**, uppercase, `letter-spacing: -0.06em`, `line-height: 0.94`
  Escala del hero: `clamp(56px, 11vw, 141px)`. Los titulares son enormes a propósito:
  pegados al borde izquierdo, cortados por el viewport si hace falta.
- Cuerpo: **Inter 300–500**, `line-height: 1.6`
- Etiquetas: Inter 600, 10px, uppercase, `letter-spacing: 0.18em`

### Motivo gráfico: los corchetes
Es la firma visual del sitio. Los corchetes `[ ]` aparecen en todos lados:
- Botones: `UNITE [+]`, `VER MÁS [+]`
- Numeración de tarjetas: `[1]` `[2]` `[3]`
- Párrafos destacados abiertos y cerrados por un `[` y un `]` grandes, en azul, separados del texto
- Contador del preloader: `[ 0 ]` → `[ 100 ]`
Los corchetes siempre en Antonio 700, en azul, con peso visual propio.

## Secciones

### 0. Preloader
- Pantalla completa azul `#1E6BFF`
- Contador centrado `[ 0 ]` → `[ 100 ]` en Antonio 700, `clamp(80px, 14vw, 180px)`
- Los corchetes en blanco 40% de opacidad, el número en blanco pleno
- Al llegar a 100 la pantalla sube y descubre el hero (`y: 0 → -100%`, 0.8s, ease-in-out)

### 1. Navbar
- Flotante, centrada horizontalmente, a 24px del techo
- Cápsula (`border-radius: 999px`) `#111` con `backdrop-filter: blur(12px)`
- Izquierda, fuera de la cápsula: logo del volcán + "VOLCANO" en Antonio 700 uppercase
- Centro: Clases · Musculación · Planes · Caminatas · Contacto (Inter 600, 11px, uppercase)
- Derecha, fuera de la cápsula: "UNITE [+]" en azul
- Mobile: hamburguesa que abre overlay negro a pantalla completa con los links en Antonio 700 gigante

### 2. Hero
- Alto de viewport completo, fondo negro
- Foto de fondo del gimnasio a sangre con overlay
  `linear-gradient(to bottom, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.45) 60%, rgba(0,0,0,0.9) 100%)`
- Titular en dos líneas, alineado a la izquierda, pegado al borde:
  **"NO ES ENTRENAR."** en blanco
  **"ES VOLCANO."** en azul eléctrico
- Debajo, Inter 300: "Música fuerte, buenas vibras y entrenos que te hacen sudar pero también reír."
- CTA: "UNITE [+]" (azul pleno, texto negro) + "Ver planes" (fantasma, borde blanco 1px)

{/* Brief de foto: interior de gimnasio con paredes negras texturadas, arcos de luz LED cálida
detrás de los racks, máquinas negras, piso oscuro, fotografía comercial contrastada */}

### 3. Marquee
- Franja azul `#1E6BFF` de 72px, ancho completo, texto negro Antonio 700
- Desplazamiento horizontal infinito, 40s lineal, sin pausa
- Contenido repetido, separado por `·`:
  "ABIERTO 6 A 23" · "+20 CLASES POR SEMANA" · "CAMINATAS A LAS SIERRAS" · "MATECITOS ❤"

### 4. Nuestras clases
- Titular "NUESTRAS CLASES" en Antonio 700 gigante, pegado al borde izquierdo, sobre foto oscura
- A la derecha, párrafo entre corchetes azules grandes:
  `[` Entrená como quieras: solo, en grupo o en la sierra. Todos los profes te corrigen la técnica desde el primer día. `]`
- Debajo, lista de clases. Cada fila ocupa el ancho completo:
  - Etiqueta chica arriba (SALA · GRUPALES · AIRE LIBRE)
  - Nombre en Antonio 700 `clamp(40px, 6vw, 96px)`
  - Grilla de tres datos a la derecha: OBJETIVO / DURACIÓN / PLAN
  - `border-bottom: 1px solid var(--border)`
  - Hover: el fondo de la fila pasa a `--surface-raised`, el nombre se tiñe de azul,
    aparece una miniatura de la clase siguiendo al cursor
- Clases:
  - MUSCULACIÓN — Ganar fuerza — Libre — Todos
  - FUNCIONAL — Estar más ágil — 45 min — Full
  - SPINNING — Quemar — 45 min — Full
  - LOCALIZADA — Tonificar — 50 min — Full
  - ENTRADA EN CALOR — Moverte mejor — 30 min — Todos
  - **CAMINATAS A LAS SIERRAS** — Despejarte — 2 hs — Full *(destacada: es lo que nos hace distintos)*

### 5. Tu rutina  ← sección propia, no la tiene ninguna competencia
- Fondo `--surface`, borde superior azul de 3px
- Etiqueta: "SOLO PARA SOCIOS"
- Titular Antonio 700: "TU RUTINA, SIEMPRE A MANO"
- Inter 300: "Entrá con tu usuario y mirá la rutina que te armó tu profe: ejercicios, series, repeticiones y el peso de la última vez. Sin anotar nada en papel."
- Mockup de la pantalla de rutina: lista de ejercicios con series × repeticiones,
  checkbox por serie completada, y el peso anterior en gris al lado del campo de hoy
- CTA: "ENTRAR A MI RUTINA [+]"

### 6. Planes
- Titular "PLANES" centrado, Antonio 700, `clamp(60px, 12vw, 160px)`
- 4 tarjetas en fila (2×2 en tablet, 1 columna en mobile). Cada tarjeta:
  - Fondo `--surface`, sin border-radius
  - **Triángulo azul en la esquina superior derecha** (`clip-path: polygon(100% 0, 0 0, 100% 100%)`, 56px)
  - Número entre corchetes arriba a la izquierda: `[1]`
  - Nombre del plan en Antonio 700
  - Lista de beneficios con `+` azul adelante, en Inter 300
  - Precio en Antonio 700 abajo
  - Botón "QUIERO ESTE [+]"
  - Hover: borde azul de 1px + `box-shadow: 0 0 24px var(--accent-soft)`
- Planes (⚠️ precios a confirmar con el gimnasio):
  - `[1]` LIBRE — Sala de musculación · Horario completo — {{precio}}/mes
  - `[2]` FULL — Sala + todas las clases grupales — {{precio}}/mes — **destacada: fondo blanco, texto negro, triángulo azul igual**
  - `[3]` FULL + CAMINATAS — Todo lo anterior + salidas a las sierras — {{precio}}/mes
  - `[4]` PERSONALIZADO — Todo + rutina y seguimiento uno a uno — {{precio}}/mes

### 7. Dónde estamos
- Mapa oscuro (estilo dark) a media pantalla, pin azul
- Al lado, bloque de datos en Inter:
  {{dirección}}, La Falda, Córdoba · {{teléfono}} · {{horarios}} · Instagram @volcano_fitnesslafalda
- Botón "CÓMO LLEGAR [+]"

### 8. CTA final
- Alto de viewport completo, fondo negro
- Titular en tres líneas, Antonio 700 `clamp(56px, 11vw, 141px)`:
  "PRIMERA" / "CLASE" / "GRATIS." ← la última línea en azul
- Inter 300: "Vení, probá y después charlamos."
- "UNITE [+]" en azul pleno

### 9. Footer
- Negro, wordmark "VOLCANO" gigante en Antonio 700 cortado por el borde inferior
- Links: Clases · Planes · Caminatas · Contacto
- Instagram · TikTok (@volcano.fitness)
- "© 2026 Volcano Fitness · La Falda, Córdoba"

## Animaciones
- Preloader: contador que sube y cortina que se va hacia arriba
- Hero: las dos líneas del titular entran escalonadas (`y: 60 → 0`, 0.7s, delay 0.12s entre líneas)
- Titulares de sección: entran desde la izquierda al hacer scroll
- Marquee: loop infinito sin pausa
- Filas de clases: fade-up escalonado, miniatura que sigue al cursor en hover
- Todos los hover: 0.15s ease
- Respetar `prefers-reduced-motion`

## Responsive
- Desktop: titulares a sangre por la izquierda, planes en fila de 4
- Tablet: planes 2×2, titulares al 70%
- Mobile: una columna, nav hamburguesa con overlay negro, hero a 85vh,
  las filas de clases pierden la grilla de datos y muestran solo nombre + duración

## Datos que faltan (reemplazar los {{ }} antes de publicar)
dirección · teléfono · horarios reales · precios de cada plan · nombres de los profes · fotos propias del gimnasio
