import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RecommendationView from '@/views/RecommendationView.vue';
import SurveyBot from '../components/SurveyBot.vue';

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
