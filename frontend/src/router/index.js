import { createRouter, createWebHistory } from "vue-router";
const HomePage = () => import("../pages/HomePage.vue");
const CatalogPage = () => import("../pages/CatalogPage.vue");
const FAQPage = () => import("../pages/FAQPage.vue");
const ContactsPage = () => import("../pages/ContactsPage.vue");
const RulesPage = () => import("../pages/RulesPage.vue");
const LoginPage = () => import("../pages/LoginPage.vue");
const RegPage = () => import("../pages/RegPage.vue");
const TicketPage = () => import("../pages/TicketPage.vue");
const ProfilePage = () => import("../pages/ProfilePage.vue");
const GuidePage = () => import("../pages/GuidePage.vue");
const ReviewPage = () => import("../pages/ReviewPage.vue");
const NotFoundPage = () => import("../pages/NotFoundPage.vue");

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
    { path: "/guide", name: "guide", component: GuidePage },
    { path: "/review", name: "review", component: ReviewPage },
    { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage },
  ],
});
