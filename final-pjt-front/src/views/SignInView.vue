<template>
  <v-card class="container">
    <h1>Login to <span class="color">www</span></h1>

    <v-form @submit.prevent="logIn" @keypress.enter="logIn">
      <v-text-field
        variant="outlined"
        color="#A58E74"
        label="아이디"
        v-model="username"
      ></v-text-field>
      <v-text-field
        variant="outlined"
        color="#A58E74"
        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show ? 'text' : 'password'"
        label="비밀번호"
        v-model="password"
        @click:append="show = !show"
      ></v-text-field>
      <div v-if="errorMessage" class="warning text-red">
        <p>{{ errorMessage }}</p>
      </div>
      <v-btn block variant="flat" color="#A58E74" @click.prevent="logIn">
        Sign in
      </v-btn>
    </v-form>

    <div class="redirect-link">
      <router-link :to="{ name: 'signup', query: { redirect: route.query.redirect } }">
        계정이 없으신가요? <span>회원가입</span>
      </router-link>
    </div>
  </v-card>
</template>


<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/users';
import { useRouter, useRoute } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const show = ref(false);
const username = ref('');
const password = ref('');
const isRight = ref(true);

const errorMessage = ref('');

const logIn = async () => {
  try {
    const payload = { username: username.value, password: password.value };
    const isLoggedIn = await userStore.logIn(payload);

    if (isLoggedIn) {
      // 로그인 성공 후 리디렉트
      const redirectPath = route.query.redirect || '/survey';
      router.push({ name: 'Survey' });
    } else {
      // 로그인 실패 시
      errorMessage.value = '로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.';
    }
  } catch (error) {
    console.error('Login Error:', error);
    errorMessage.value = '서버에 문제가 발생했습니다. 나중에 다시 시도하세요.';
  }
};

</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 20px;
  background-color: #ffefcd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

form {
  margin-top: 1rem;
}

.redirect-link {
  margin-top: 1rem;
  font-size: 0.9rem;
}

.redirect-link span {
  text-decoration: underline;
  color: #424530;
  font-weight: bold;
}

.warning {
  color: #b00020;
  font-size: 14px;
}
</style>
