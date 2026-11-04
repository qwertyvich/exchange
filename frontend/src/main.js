import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import './styles/glass-motion.css';
import './styles/home-motion.css';

createApp(App).use(router).mount("#app");
