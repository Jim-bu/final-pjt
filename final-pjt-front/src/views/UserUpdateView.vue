<template>
  <div class="update-page">
    <h2>회원 정보 수정</h2>
    <div v-if="loading" class="loading">
      데이터를 불러오는 중...
    </div>
    <form v-else @submit.prevent="handleSubmit" class="update-form">
      <!-- 프로필 이미지 섹션 -->
      <div class="profile-image-section">
  <div class="current-image">
    <template v-if="previewImage || userStore.userInfo?.profile_image">
      <img 
        :src="previewImage || userStore.userInfo.profile_image"
        :alt="userStore.userInfo?.username"
        @error="handleImageError"
      />
    </template>
    <div v-else class="no-image">
      <span>{{ getInitials(userStore.userInfo?.name || userStore.userInfo?.username) }}</span>
    </div>
  </div>
  <div class="image-upload">
    <label for="profile-image" class="upload-label">
      프로필 이미지 변경
    </label>
    <input
      type="file"
      id="profile-image"
      accept="image/*"
      @change="handleImageChange"
      class="file-input"
    />
  </div>
  <p class="image-help-text" v-if="selectedFile">
    선택된 파일: {{ selectedFile.name }}
  </p>
</div>


      <!-- 기본 정보 섹션 -->
      <div class="form-section">
        <h3>기본 정보</h3>
        <div class="form-group">
          <label for="name">닉네임</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            class="form-input"
            placeholder="닉네임을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="age">나이</label>
          <input
            id="age"
            v-model.number="formData.age"
            type="number"
            class="form-input"
            placeholder="나이를 입력하세요"
          />
        </div>
      </div>

      <!-- 자산 정보 섹션 -->
      <div class="form-section">
        <h3>자산 정보</h3>
        <div class="form-group">
          <label for="money">현재 자산</label>
          <input
            id="money"
            v-model.number="formData.money"
            type="number"
            class="form-input"
            placeholder="현재 자산을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="salary">연봉</label>
          <input
            id="salary"
            v-model.number="formData.salary"
            type="number"
            class="form-input"
            placeholder="연봉을 입력하세요"
          />
        </div>
      </div>

      <!-- 예금 희망 정보 섹션 -->
      <div class="form-section">
        <h3>예금 희망 정보</h3>
        <div class="form-group">
          <label for="desire_amount_deposit">예금 희망 금액</label>
          <input
            id="desire_amount_deposit"
            v-model.number="formData.desire_amount_deposit"
            type="number"
            class="form-input"
            placeholder="예금 희망 금액을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="deposit_period">예금 희망 기간 (월)</label>
          <input
            id="deposit_period"
            v-model.number="formData.deposit_period"
            type="number"
            class="form-input"
            placeholder="예금 희망 기간을 입력하세요"
          />
        </div>
      </div>

      <!-- 적금 희망 정보 섹션 -->
      <div class="form-section">
        <h3>적금 희망 정보</h3>
        <div class="form-group">
          <label for="desire_amount_saving">월 적금 희망 금액</label>
          <input
            id="desire_amount_saving"
            v-model.number="formData.desire_amount_saving"
            type="number"
            class="form-input"
            placeholder="월 적금 희망 금액을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="saving_period">적금 희망 기간 (월)</label>
          <input
            id="saving_period"
            v-model.number="formData.saving_period"
            type="number"
            class="form-input"
            placeholder="적금 희망 기간을 입력하세요"
          />
        </div>
      </div>

      <!-- 버튼 그룹 -->
      <div class="button-group">
        <button type="button" class="cancel-button" @click="handleCancel">
          취소
        </button>
        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? '업데이트 중...' : '정보 수정' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useUserStore } from '@/stores/users';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const loading = ref(false);
const previewImage = ref(null);
const selectedFile = ref(null);

// 프로필 이미지 URL 계산
const profileImageUrl = computed(() => {
  if (userStore.userInfo?.profile_image) {
    return `${import.meta.env.VITE_APP_API_URL}${userStore.userInfo.profile_image}`;
  }
  return '/default-profile.png';
});

// 이미지 로드 실패 시 처리
const handleImageError = (e) => {
  e.target.src = '/default-profile.png';
};

// 이미지 파일 선택 처리
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    // 파일 크기 체크 (예: 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('파일 크기는 5MB를 초과할 수 없습니다.');
      event.target.value = '';
      return;
    }
    
    // 이미지 파일 타입 체크
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드 가능합니다.');
      event.target.value = '';
      return;
    }

    selectedFile.value = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

// 폼 데이터 초기화
const formData = ref({
  name: '',
  age: null,
  money: null,
  salary: null,
  desire_amount_deposit: null,
  deposit_period: null,
  desire_amount_saving: null,
  saving_period: null,
});

// 초기 데이터 로드
const loadUserData = () => {
  if (userStore.userInfo) {
    formData.value = {
      name: userStore.userInfo.name || '',
      age: userStore.userInfo.age || null,
      money: userStore.userInfo.money || null,
      salary: userStore.userInfo.salary || null,
      desire_amount_deposit: userStore.userInfo.desire_amount_deposit || null,
      deposit_period: userStore.userInfo.deposit_period || null,
      desire_amount_saving: userStore.userInfo.desire_amount_saving || null,
      saving_period: userStore.userInfo.saving_period || null,
    };
  }
};

// 폼 제출 처리
const handleSubmit = async () => {
  loading.value = true;
  try {
    const formDataToSend = new FormData();
    
    if (selectedFile.value) {
      formDataToSend.append('profile_image', selectedFile.value);
    }

    Object.keys(formData.value).forEach(key => {
      if (formData.value[key] !== null && formData.value[key] !== '') {
        formDataToSend.append(key, formData.value[key]);
      }
    });

    await userStore.updateUserInfo(formDataToSend);
    // 업데이트 후 사용자 정보 갱신
    await userStore.getUserInfo();
    
    alert('회원 정보가 성공적으로 수정되었습니다.');
    router.push({ 
      name: 'myPage', 
      params: { username: userStore.userInfo.username } 
    });
  } catch (error) {
    console.error('Update error:', error);
    alert('회원 정보 수정에 실패했습니다.');
  } finally {
    loading.value = false;
  }
};

// 취소 처리
const handleCancel = () => {
  // 미리보기 이미지와 선택된 파일 정리
  if (previewImage.value) {
    URL.revokeObjectURL(previewImage.value);
  }
  previewImage.value = null;
  selectedFile.value = null;
  router.back();
};

// 컴포넌트 언마운트 시 미리보기 URL 정리
onBeforeUnmount(() => {
  if (previewImage.value) {
    URL.revokeObjectURL(previewImage.value);
  }

// 컴포넌트 마운트 시
onMounted(() => {
  loadUserData();
});
});

// 이니셜 가져오기 함수
const getInitials = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};
</script>

<style scoped>
.update-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.update-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

h3 {
  color: #495057;
  margin-bottom: 20px;
  font-size: 18px;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #495057;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3a774e;
  box-shadow: 0 0 0 2px rgba(58, 119, 78, 0.1);
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.submit-button, .cancel-button {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button {
  background-color: #3a774e;
  color: white;
}

.submit-button:hover {
  background-color: #2d5d3d;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}

.cancel-button:hover {
  background-color: #5a6268;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

@media (max-width: 768px) {
  .update-page {
    max-width: 100%;
    padding: 15px;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-button, .cancel-button {
    width: 100%;
  }
}

.current-image {
  width: 150px;
  height: 150px;
  margin: 0 auto 16px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #e4c089;
  background-color: #f5f5f5;
}

.current-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e4c089;
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.profile-image-section {
  text-align: center;
  margin-bottom: 24px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.image-upload {
  margin: 16px 0;
}

.upload-label {
  display: inline-block;
  padding: 8px 16px;
  background-color: #e4c089;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-label:hover {
  background-color: #d8b679;
}

.file-input {
  display: none;
}

.image-help-text {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}
</style>