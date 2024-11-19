import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/users'
import HomeView from '../views/HomeView.vue';
import RecommendationView from '@/views/RecommendationView.vue';
import SurveyBot from '../components/SurveyBot.vue';
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/main',
      name: 'Main',
      component: HomeView,
    },
    {
      path: '/',
      name: 'Survey',
      component: SurveyBot,
    },
    {
      path: '/recommendation',
      name: 'Recommendation',
      component: RecommendationView,
    },
    {
      path: '/login',
      name: 'login',
      component: SignInView,
      beforeEnter: (to, from, next) => {
        if (from.name) {
          to.query.redirect = from.fullPath;
        }
        next();
      },
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      beforeEnter: (to, from, next) => {
        if (from.name) {
          to.query.redirect = from.fullPath;
        }
        next();
      },
    },
  ]
});

export function resetRouter() {
  const newRouter = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
  });
  router.matcher = newRouter.matcher;
}

export default router;
