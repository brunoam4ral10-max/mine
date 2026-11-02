# Minecraft · Item Viewer 3D

Viewer interativo de espadas do Minecraft construído com **HTML + CSS + JavaScript (Three.js)**.
A sprite vanilla 16×16 é reconstruída **voxel a voxel** em uma malha 3D real — cada pixel opaco
vira um bloco com relevo, faces laterais sombreadas e textura *nearest-neighbor*.

## Como usar

Abra **`index.html`** diretamente no navegador (duplo clique). Não precisa de servidor, build,
npm ou internet: Three.js, a fonte pixelada e as 6 texturas estão embutidos no próprio arquivo.

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

## Estrutura

```
index.html                  ← arquivo final, autossuficiente (entregável)
README.md
build.py                    ← gera index.html a partir do template
src/template.html           ← HTML + CSS + JS legíveis (edite aqui)
vendor/three.min.js         ← Three.js r128 (MIT)
assets/textures/*.png       ← 6 texturas vanilla 16×16
assets/press-start-2p-latin.woff2
```

Para alterar o viewer, edite `src/template.html` e rode:

```bash
python3 build.py       # requer Pillow: pip install pillow
```

## Créditos

Texturas de item © Mojang Studios / Microsoft (Minecraft Java 1.20.4), usadas aqui como
referência visual de pixel art. Three.js r128 (MIT). Fonte *Press Start 2P* (SIL OFL 1.1).
