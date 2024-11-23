import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/users'
import HomeView from '../views/HomeView.vue';
import RecommendationView from '@/views/RecommendationView.vue';
import SurveyBot from '../components/SurveyBot.vue';
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import BankMapView from '@/views/BankMapView.vue';
import MyPageView from '@/views/MyPageView.vue';
import MyPage from '@/components/MyPage.vue';
import ProductListView from '@/views/ProductListView.vue';
import ProductCompareView from '@/views/ProductCompareView.vue';
import PopupMenu from '@/components/PopupMenu.vue';
import ExchangeView from '@/views/ExchangeView.vue';
import NewsView from '@/views/NewsView.vue';
import CommunityView from '@/views/CommunityView.vue';

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
    
    {
      path: "/nearBank",
      name: "nearBank",
      component: BankMapView,
    },
    {
      path: '/mypage/:username*',
      name: 'mypage',
      component: MyPageView,
      beforeEnter: (to, from) => {
        const userStore = useUserStore()
        if (!userStore.isLogin) {
          alert('로그인 후 이용 가능합니다.')
          return { name: 'signIn'}
        }
      },
      children: [
        {
          path: '',
          name: 'myPage',
          component: MyPage
        },
        // {
        //   path: 'products',
        //   name: 'productManage',
        //   component: ProductManage
        // },
        // {
        //   path: 'recommend',
        //   name: 'productRecommend',
        //   component: ProductRecommend
        // }
      ]
    },
    {
      path: "/productList",
      name: "productList",
      component: ProductListView,
    },
    {
      path: "/productcompare",
      name: "productcompare",
      component: ProductCompareView
    },
    { 
      path: '/popup-menu',
      name: 'PopupMenu',
      component: PopupMenu 
    },
  { 
    path: '/exchange',
    name: 'Exchange',
    component: ExchangeView,
  },
  { 
    path: '/news',
    name: 'News',
    component: NewsView,
  },
  {
    path: '/community',
    name: 'Community',
    component: CommunityView,
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
