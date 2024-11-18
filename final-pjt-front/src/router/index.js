import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RecommendationView from '@/views/RecommendationView.vue';
import SurveyBot from '../components/SurveyBot.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/survey',
    name: 'Survey',
    component: SurveyBot,
  },
  {
    path: '/recommendation',
    name: 'Recommendation',
    component: RecommendationView,
  },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
