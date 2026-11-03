<template>
  <component :is="currentHomepage" />
</template>

<script setup>
import { computed } from "vue";
import { siteSettings } from "../lib/siteState";
import HomepageMode0 from "./HomePage0.vue";
import HomepageMode1 from "./HomePage1.vue";
import HomepageMode2 from "./HomePage2.vue";

const mode = computed(() => String(siteSettings.value?.mode ?? "0"));
const currentHomepage = computed(() => {
  if (mode.value === "1") return HomepageMode1;
  if (mode.value === "2") return HomepageMode2;
  return HomepageMode0;
});
</script>