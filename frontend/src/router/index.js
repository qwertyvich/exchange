import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import CatalogPage from "../pages/CatalogPage.vue";
import FAQPage from "../pages/FAQPage.vue";
import ContactsPage from "../pages/ContactsPage.vue";
import RulesPage from "../pages/RulesPage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegPage from "../pages/RegPage.vue"; 
import TicketPage from "../pages/TicketPage.vue";  
import ProfilePage from "../pages/ProfilePage.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomePage },
    { path: "/login", name: "login", component: LoginPage },
    { path: "/registration", name: "registration", component: RegPage },
    { path: "/faq", name: "faq", component: FAQPage },
    { path: "/contacts", name: "contacts", component: ContactsPage },
    { path: "/rules", name: "rules", component: RulesPage },
    { path: "/catalog", name: "catalog", component: CatalogPage },
    { path: "/tickets/:id", name: "ticket", component: TicketPage },
    { path: "/profile", name: "profile", component: ProfilePage },
  ],
});