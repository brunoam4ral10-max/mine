# Minecraft · Item Viewer 3D

Dois ambientes 3D em **HTML + CSS + JavaScript (Three.js)**, ambos 100% autossuficientes:

| Página | O que é |
|---|---|
| **`index.html`** | Item viewer da espada: sprite vanilla 16×16 reconstruída **voxel a voxel**, com 6 materiais, vista explodida e órbita livre. |
| **`casa.html`** | Casa de fazenda em estilo Minecraft **totalmente 3D e procedural**, com navegação cinematográfica por scroll, ciclo dia/noite e hotspots interativos. |

As páginas são ligadas entre si (ícone ⌂ no topo do viewer / link «voltar» na casa).

## Como usar

Abra **`index.html`** ou **`casa.html`** diretamente no navegador (duplo clique). Não precisa de
servidor, build, npm ou internet: Three.js, a fonte pixelada, as texturas e os modelos estão
embutidos/gerados por código em cada arquivo.

> Para uma prévia ao vivo, rode `python3 -m http.server 8080` nesta pasta e acesse
> `http://localhost:8080`.

## Controles

| Ação | Entrada |
|---|---|
| Girar livremente (todos os ângulos) | Arrastar com o mouse / toque |
| Aproximar e afastar | Scroll do mouse / pinça no touch |
| Redefinir a câmera | Duplo clique, botão `REDEFINIR` ou `R` |
| Trocar de material | Botões na barra inferior ou teclas `1`–`6` |
| Auto-rotação (retoma após 2,2 s de inatividade) | `AUTO-ROTAÇÃO` / `A` |
| Vista explodida (mostra os 84 blocos) | `VOXELS` / `V` |
| Partículas, glints e halo de luz | `BRILHO` / `B` |
| Tela cheia | Ícone no topo / `F` |
| Girar pelo teclado | Setas |

## Materiais

Madeira, Pedra, Ferro, Ouro, Diamante e Netherita — com os atributos reais do **Java Edition
1.20.x** (dano, velocidade de ataque, durabilidade e encantabilidade). A silhueta é idêntica nos
seis arquivos, então a troca de textura é instantânea, sem reconstruir a geometria.

## Detalhes técnicos

- **Geometria**: um único `BufferGeometry` com 84 voxels, faces internas eliminadas e
  *vertex colors* para sombreamento nas laterais; ~2.000 vértices no total.
- **Relevo**: a profundidade de cada bloco vem da luminância do pixel (a guarda e o cabo são
  mais espessos), criando um leve 3D em relevo sem perder o desenho original.
- **Textura**: `CanvasTexture` 16×16 gerada em runtime, `NearestFilter`, sem mipmaps, UVs com
  pequeno *inset* para evitar sangramento entre pixels.
- **Cena**: luz ambiente + hemisférica + direcional principal com `PCFSoftShadowMap`, luz de
  contorno e ponto de preenchimento coloridos pelo material, `ACESFilmicToneMapping`.
- **Cinematografia**: fundo escuro com gradiente, grade, vinheta e grão; poço de luz e sombra
  projetada no piso; poeira e glints aditivos; flutuação senoidal; intro em que os voxels se
  montam sozinhos.
- **Performance**: `setPixelRatio` limitado a 2, pausa em aba oculta, `requestAnimationFrame`
  com delta limitado, sem pós-processamento e sem dependências externas em runtime.
- **Responsivo**: a distância da câmera é recalculada pelo aspecto da tela; HUD reorganizado
  para celulares, com suporte a gestos de pinça.

## A casa 3D (`casa.html`)

Inspirada em [woanminecraftfolio.com](https://www.woanminecraftfolio.com/) e em construções
cottagecore do Minecraft. **Nenhum modelo `.glb`/`.obj` é carregado**: o mundo é gerado por
código a partir de ~12.000 blocos.

- Frontão empenado escalonado de tijolos de pedra com reboco claro, janela no sótão, chaminé de
  tijolos e telhado de tábuas escuras; paredes de reboco com vigas de carvalho escuro.
- Varanda com pérgula, videiras penduradas, jardineiras, placa *WELCOME*, vasos de rosas,
  floreiras sob as janelas, escadas e caminho de cascalho.
- Jardim com canteiros murados (flores e trigo), postes de lanterna, *sea lantern* luminosa,
  hortas em terraços ao fundo, árvores, nuvens e montanhas.
- **5 pontos de vista** com câmera interpolada (scroll, teclas `1–5` ou marcadores laterais),
  órbita livre por arraste, zoom por pinça/`+`/`−`, auto-rotação após 4 s de inatividade.
- **Ciclo dia · entardecer · noite** (`T`): céu, névoa, luzes, estrelas e halos mudam juntos.
- **5 hotspots** projetados do 3D para o HTML abrem fichas sobre cada parte da casa.
- Som ambiente procedural via WebAudio (`S`), modal de ajuda (`?`), tela de carregamento e HUD responsivo.

Tecnicamente: um **atlas de 32 texturas pixel art 16×16** desenhado em `<canvas>`, um único
`BufferGeometry` com faces internas eliminadas (1 draw call), vegetação em planos cruzados com
`alphaTest`, sombras `PCFSoft`, luzes de ponto reais nas lanternas e `ACESFilmicToneMapping`.

## Estrutura

```
index.html                  ← item viewer da espada (autossuficiente)
casa.html                   ← casa 3D procedural (autossuficiente)
README.md
build.py                    ← gera index.html
build_house.py              ← gera casa.html
src/template.html           ← HTML + CSS + JS do viewer
src/house-template.html     ← HTML + CSS + JS da casa
vendor/three.min.js         ← Three.js r128 (MIT)
assets/textures/*.png       ← 6 texturas vanilla 16×16
assets/press-start-2p-latin.woff2
preview.png / casa-preview.png
```

Para alterar algo, edite o template correspondente e rode:

```bash
python3 build.py            # gera index.html (requer Pillow)
python3 build_house.py      # gera casa.html
```

## Créditos

Texturas de item © Mojang Studios / Microsoft (Minecraft Java 1.20.4), usadas aqui como
referência visual de pixel art. Three.js r128 (MIT). Fonte *Press Start 2P* (SIL OFL 1.1).
