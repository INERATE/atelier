---
name: anime-js
description: Anime.js v4 — fast, tree-shakeable JS animation. Load for JS animation that Framer Motion doesn't cover well: multi-target timelines, SVG morph/line-draw, draggable with spring release, motion paths, scroll-scrub, staggered grids, and text splitting. Triggers on "anime.js"/"animejs", timeline, stagger, SVG morph, draw/drawable, motion path, draggable, splitText.
---

# Anime.js v4

Modular, tree-shakeable. Import only what you use. In Atelier, reach for it when
the effect is **timeline-, SVG-, or draggable-heavy**; for trigger-driven React
UI motion prefer Framer Motion (design-law §4), for continuous card schematics
prefer [[living-graphics]]. All motion still obeys the design-law motion system:
expo/spring physics, reduced-motion fallback, transform/opacity/canvas only.

## Install
`npm i animejs` · ESM `import { animate } from 'animejs'` · CDN `https://esm.sh/animejs`

## Core API (import from `animejs`)
- `animate(targets, params)` — CSS/transforms/vars, SVG attrs, JS objects, HTML attrs. Values: numeric, units, relative `+=`/`-=`/`*=`, color, `[from, to]`, or `(el,i,total)=>` functions. `ease:'outExpo'`, `createSpring({stiffness,damping,mass})`.
- `createTimeline({defaults})` → `.add(t, params, pos)` — position `'<'` (with prev), `'-=200'`, `'+=100'`, ms, or a label.
- `stagger(100, { from:'center', grid:[cols,rows] })` — for `delay`/values.
- `onScroll({ target, sync:true, enter, leave })` — pass as `autoplay` to scrub.
- SVG: `morphTo(path)`, `createDrawable('path')` + `{ draw:['0 0','0 1'] }`, `createMotionPath(path)`.
- `splitText(el,{chars,words,lines})` → `.addEffect()` for per-char reveals.
- `createDraggable(el,{ container, releaseEase:createSpring(...) })`.
- Utils: `$`, `get`/`set`, `remove`, `random`, `clamp`, `lerp`, `mapRange`.

## Patterns
```js
import { animate, createTimeline, stagger, createDrawable } from 'animejs';

animate('.item', { translateY:[16,0], opacity:[0,1],
  delay: stagger(70, { from:'center' }), duration:600, ease:'outExpo' });

createTimeline({ defaults:{ duration:500, ease:'outExpo' } })
  .add('.a',{ x:100 }).add('.b',{ x:100 }, '<').add('.c',{ x:100 }, '-=200');

animate(createDrawable('path'), { draw:['0 0','0 1'], duration:2000, ease:'inOutQuad' });
```

## React — always scope + revert
```jsx
useEffect(() => {
  const scope = createScope({ root: ref.current })
    .add(() => animate('.box', { rotate:360 }));
  return () => scope.revert();       // cleanup is mandatory
}, []);
```

Bundle: full ~24.5KB gzip; animation core ~10KB; add draggable/scroll only if used.
Docs: https://animejs.com/documentation · easing editor: https://animejs.com/easing-editor
