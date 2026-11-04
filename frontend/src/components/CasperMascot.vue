<template>
  <Teleport to="body">
    <div v-show="enabled" class="casperMascotLayer" data-casper-mascot aria-hidden="true">
      <div ref="body" class="casperActor" data-casper-flight><CasperFigure part="body" /></div>
      <div ref="accessories" class="casperActor" data-casper-props><CasperFigure part="accessories" /></div>
    </div>
  </Teleport>
</template>

<script setup>
import { nextTick, onMounted, onBeforeUnmount, ref, watch } from 'vue';
import CasperFigure from './CasperFigure.vue';
import { casperTimeline, CASPER_DURATION } from '../lib/casperTimeline';

const props = defineProps({ active: Boolean });
const body = ref(null), accessories = ref(null), enabled = ref(false);
const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
let animations = [], resizeObserver, appObserver, bodyObserver, geometryFrame, generation = 0;

function geometry() {
  const anchor = document.querySelector('.siteBrandBar [data-casper-home-anchor]');
  if (!anchor) return null;
  const rect = anchor.getBoundingClientRect();
  const heading = document.querySelector('[data-home-intro="heading"]');
  const receive = document.querySelector('label[for="get-input"]');
  return casperTimeline({
    home: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
    width: window.innerWidth, height: window.innerHeight,
    headingTop: heading?.getBoundingClientRect().top ?? window.innerHeight * .35,
    receiveTop: receive?.getBoundingClientRect().top ?? window.innerHeight * .65,
  });
}

function updateGeometry() {
  geometryFrame = undefined;
  if (!animations.length) return;
  const frames = geometry();
  if (!frames) return;
  animations[0].effect.setKeyframes(frames.body);
  animations[1].effect.setKeyframes(frames.accessories);
}
function queueGeometry() {
  if (animations.length && geometryFrame == null) geometryFrame = requestAnimationFrame(updateGeometry);
}
function syncPlayback() {
  const paused = document.hidden || document.body.classList.contains('overlay-open');
  for (const animation of animations) {
    if (paused && animation.playState !== 'paused') animation.pause();
    else if (!paused && animation.playState === 'paused') animation.play();
  }
}
function stop() {
  generation++;
  animations.forEach(animation => animation.cancel()); animations = [];
  enabled.value = false;
  document.body.classList.remove('casper-live');
  resizeObserver?.disconnect();
  if (geometryFrame != null) cancelAnimationFrame(geometryFrame);
  geometryFrame = undefined;
}
async function configure() {
  stop();
  if (!props.active || preference.matches || !body.value?.animate) return;
  const version = generation;
  await nextTick();
  const image = body.value.querySelector('img');
  try { await image.decode(); } catch { return; }
  if (version !== generation || !props.active || preference.matches) return;
  const frames = geometry();
  if (!frames) return;
  const options = { duration: CASPER_DURATION, iterations: Infinity, easing: 'linear' };
  animations = [body.value.animate(frames.body, options), accessories.value.animate(frames.accessories, options)];
  const start = document.timeline.currentTime;
  animations.forEach(animation => { animation.startTime = start; });
  enabled.value = true;
  document.body.classList.add('casper-live');
  const anchor = document.querySelector('.siteBrandBar [data-casper-home-anchor]');
  if (anchor) resizeObserver.observe(anchor);
  syncPlayback();
}

watch(() => props.active, configure);
onMounted(() => {
  resizeObserver = new ResizeObserver(queueGeometry);
  appObserver = new MutationObserver(queueGeometry);
  appObserver.observe(document.querySelector('#app'), { childList: true, subtree: true });
  bodyObserver = new MutationObserver(syncPlayback);
  bodyObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  window.addEventListener('resize', queueGeometry, { passive: true });
  window.addEventListener('scroll', queueGeometry, { passive: true, capture: true });
  document.addEventListener('visibilitychange', syncPlayback);
  preference.addEventListener('change', configure);
  configure();
});
onBeforeUnmount(() => {
  stop(); appObserver?.disconnect(); bodyObserver?.disconnect();
  window.removeEventListener('resize', queueGeometry);
  window.removeEventListener('scroll', queueGeometry, true);
  document.removeEventListener('visibilitychange', syncPlayback);
  preference.removeEventListener('change', configure);
});
</script>

<style>
.casperMascotLayer { position: fixed; inset: 0; z-index: 80; overflow: hidden; pointer-events: none !important; }
.casperMascotLayer * { pointer-events: none !important; }
.casperActor { position: absolute; top: 0; left: 0; width: 100px; height: 100px; transform-origin: 0 0; will-change: transform, opacity; }
body.overlay-open .casperMascotLayer { visibility: hidden; }
@media (prefers-reduced-motion: reduce) { .casperMascotLayer { display: none !important; } }
</style>
