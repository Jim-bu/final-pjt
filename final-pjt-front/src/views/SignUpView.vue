<script setup>
import { computed, ref } from 'vue';
import { useUserStore } from '@/stores/users';
import { useVuelidate } from '@vuelidate/core';
import { email, required, minLength, maxLength, alphaNum, sameAs, helpers } from '@vuelidate/validators';
import { useRouter, useRoute } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const checkList = ['service', 'info'];
const selected = ref([]);
const show1 = ref(false);
const show2 = ref(false);

const isAgreeAll = computed({
  get() {
    return checkList.length === selected.value.length;
  },
  set(e) {
    selected.value = e ? checkList : [];
  },
});

const errorAgree = ref('ㅤ');

const initialState = {
  username: '',
  name: '',
  email: '',
  password1: '',
  password2: '',
};

const state = ref({
  ...initialState,
});

const rules = {
  username: {
    required: helpers.withMessage('아이디를 입력해주세요.', required),
    alphaNum: helpers.withMessage('영어 대소문자와 숫자만 입력가능합니다.', alphaNum),
    minLength: helpers.withMessage('5자 이상 입력해야합니다.', minLength(5)),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20)),
  },
  name: {
    required: helpers.withMessage('닉네임을 입력해주세요.', required),
    maxLength: helpers.withMessage('20자 이하로 입력해야합니다.', maxLength(20)),
  },
  email: {
    required: helpers.withMessage('이메일을 입력해주세요.', required),
    email: helpers.withMessage('이메일 주소가 정확한지 확인해 주세요.', email),
    maxLength: helpers.withMessage('100자 이하로 입력해야합니다.', maxLength(100)),
  },
  password1: {
    required: helpers.withMessage('비밀번호를 입력해주세요.', required),
    minLength: helpers.withMessage('8자 이상 입력해주세요.', minLength(8)),
    maxLength: helpers.withMessage('16자 이하로 입력해주세요.', maxLength(16)),
  },
  password2: {
    required: helpers.withMessage('비밀번호 확인은 필수 사항입니다.', required),
    sameAsPassword: helpers.withMessage(
      '비밀번호가 일치하지 않습니다.',
      sameAs(computed(() => state.value.password1))
    ),
  },
};

const v$ = useVuelidate(rules, state);

const clearForm = () => {
  v$.value.$reset();
  Object.assign(state.value, initialState);
};

const signUp = async () => {
  v$.value.$validate();

  if (selected.value.length !== checkList.length) {
    errorAgree.value = '약관에 동의하셔야 합니다.';
    return;
  }

  if (v$.value.$invalid) {
    return;
  }

  try {
    const payload = {
      username: state.value.username,
      name: state.value.name,
      email: state.value.email,
      password1: state.value.password1,
      password2: state.value.password2,
    };

    await userStore.signUp(payload);

    // 자동 로그인 처리
    const loginPayload = {
      username: state.value.username,
      password: state.value.password1,
    };
    await userStore.logIn(loginPayload);

    alert('회원가입이 완료되었습니다!');
    const redirectPath = route.query.redirect || '/main';
    router.push(redirectPath);

    clearForm();
  } catch (error) {
    alert('회원가입 중 문제가 발생했습니다. 다시 시도해 주세요.');
  }
};
</script>


<template>
  <v-card class="container">
    <h1 class="title">Sign up to <span class="highlight">WWW</span></h1>

    <div class="checkbox">
      <p class="warning" v-text="errorAgree"></p>
      <v-checkbox
        color="#A58E74"
        label="(필수) 서비스 이용약관 동의"
        value="service"
        v-model="selected"
      ></v-checkbox>
      <v-checkbox
        color="#A58E74"
        label="(필수) 개인정보 처리 동의"
        value="info"
        v-model="selected"
      ></v-checkbox>
      <v-checkbox color="#A58E74" v-model="isAgreeAll">
        <template v-slot:label>
          <span>전체 동의</span>
        </template>
      </v-checkbox>
    </div>

    <form @submit.prevent="signUp">
      <v-text-field
        variant="outlined"
        color="#A58E74"
        label="아이디"
        v-model="state.username"
        :error-messages="v$.username.$errors.map((e) => e.$message)"
        @input="v$.username.$touch"
        @blur="v$.username.$touch"
      ></v-text-field>

      <v-text-field
        variant="outlined"
        color="#A58E74"
        label="닉네임"
        v-model="state.name"
        :error-messages="v$.name.$errors.map((e) => e.$message)"
        @input="v$.name.$touch"
        @blur="v$.name.$touch"
      ></v-text-field>

      <v-text-field
        variant="outlined"
        color="#A58E74"
        label="이메일"
        v-model="state.email"
        :error-messages="v$.email.$errors.map((e) => e.$message)"
        @input="v$.email.$touch"
        @blur="v$.email.$touch"
      ></v-text-field>

      <v-text-field
        variant="outlined"
        color="#A58E74"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show1 ? 'text' : 'password'"
        label="비밀번호"
        v-model="state.password1"
        @click:append="show1 = !show1"
        :error-messages="v$.password1.$errors.map((e) => e.$message)"
        @input="v$.password1.$touch"
        @blur="v$.password1.$touch"
      ></v-text-field>

      <v-text-field
        variant="outlined"
        color="#A58E74"
        :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
        :type="show2 ? 'text' : 'password'"
        label="비밀번호 확인"
        v-model="state.password2"
        @click:append="show2 = !show2"
        :error-messages="v$.password2.$errors.map((e) => e.$message)"
        @input="v$.password2.$touch"
        @blur="v$.password2.$touch"
      ></v-text-field>

      <v-btn block variant="flat" color="#A58E74" @click.prevent="signUp">
        회원가입
      </v-btn>
    </form>

    <router-link class="redirect-link" :to="{ name: 'login', query: { redirect: route.query.redirect } }">
      이미 계정이 있으신가요? 로그인
    </router-link>
  </v-card>
</template>


<style scoped>
.container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 20px;
  background-color: #ffefcd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #424530;
}

.highlight {
  color: #A58E74;
}

.checkbox {
  margin: 1rem 0;
  text-align: left;
}

form > * {
  margin-bottom: 1rem;
}

.redirect-link {
  margin-top: 1rem;
  font-size: 0.9rem;
  text-decoration: underline;
  color: #424530;
}
</style>
