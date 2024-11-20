<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const currencies = ref([]) // 통화 목록
const response = ref([]) // 전체 응답 데이터
const selectedState = ref('송금 받으실 때') // 선택된 상태
const selectedCurrency = ref('미국 달러') // 기본 통화
const selectedCurrencyUnit = ref('USD') // 기본 단위
const selectedTtb = ref() // 송금 받으실 때
const selectedTts = ref() // 송금 보내실 때
const selectedDeal = ref() // 매매 기준율

const calculateVariable = ref() // 계산 기준 값
const krwInput = ref() // 원화 입력 값
const otherInput = ref() // 외화 입력 값

const states = ['송금 받으실 때', '송금 보내실 때', '매매 기준율'] // 상태 목록
const isLoading = ref(true) // 로딩 상태
const error = ref(null) // 에러 메시지

const userStore = useUserStore()

const emit = defineEmits(['passCurrency'])

onMounted(async () => {
  try {
    const res = await axios.get(`${userStore.API_URL}/currencies/exchange/`)
    response.value = res.data.filter(data => data['ttb'] !== '0')

    currencies.value = response.value.map(item => item['cur_nm'])
    const units = response.value.map(item => item['cur_unit'])
    emit('passCurrency', currencies.value, units)

    // 기본 값 설정 (미국 달러)
    const usdInfo = response.value.find(item => item['cur_nm'] === '미국 달러')
    selectedTtb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
    selectedTts.value = Number(usdInfo['tts'].replaceAll(',', ''))
    selectedDeal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
    calculateVariable.value = selectedTtb.value
  } catch (err) {
    console.error('환율 데이터를 가져오는 중 오류:', err)
    error.value = '환율 데이터를 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
})

// 통화 선택 시 값 업데이트
watch(selectedCurrency, () => {
  const selectedInfo = response.value.find(item => item['cur_nm'] === selectedCurrency.value)
  if (!selectedInfo) return

  selectedCurrencyUnit.value = selectedInfo['cur_unit']
  const factor = selectedCurrency.value === '일본 옌' || selectedCurrency.value === '인도네시아 루피아' ? 100 : 1

  selectedTtb.value = Number(selectedInfo['ttb'].replaceAll(',', '')) / factor
  selectedTts.value = Number(selectedInfo['tts'].replaceAll(',', '')) / factor
  selectedDeal.value = Number(selectedInfo['deal_bas_r'].replaceAll(',', '')) / factor

  calculateVariable.value =
    selectedState.value === '송금 받으실 때'
      ? selectedTtb.value
      : selectedState.value === '송금 보내실 때'
      ? selectedTts.value
      : selectedDeal.value

  inputEventOther()
})

// 상태 변경 시 값 업데이트
watch(selectedState, () => {
  calculateVariable.value =
    selectedState.value === '송금 받으실 때'
      ? selectedTtb.value
      : selectedState.value === '송금 보내실 때'
      ? selectedTts.value
      : selectedDeal.value

  inputEventOther()
})

// 계산 함수
const roundToTwo = num => +(Math.round(num + 'e+2') + 'e-2')

const inputEventKrw = () => {
  otherInput.value = roundToTwo(krwInput.value / calculateVariable.value)
}

const inputEventOther = () => {
  krwInput.value = roundToTwo(otherInput.value * calculateVariable.value)
}
</script>

<template>
  <v-card>
    <v-form v-if="!isLoading && !error">
      <v-container>
        <v-row>
          <v-col cols="3" offset="9">
            <v-select
              color="#1089FF"
              variant="outlined"
              :items="states"
              density="compact"
              label="기준"
              v-model="selectedState"
            ></v-select>
          </v-col>
        </v-row>

        <v-row no-gutter>
          <v-col cols="3">
            <v-select
              color="#1089FF"
              variant="outlined"
              label="통화 선택"
              :items="currencies"
              v-model="selectedCurrency"
            ></v-select>
          </v-col>
          <v-col cols="9">
            <v-text-field
              type="number"
              color="#1089FF"
              variant="outlined"
              :label="selectedCurrencyUnit"
              v-model="otherInput"
              @input="inputEventOther"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row class="my-0">
          <v-text-field
            type="number"
            append-inner-icon="mdi-currency-krw"
            color="#1089FF"
            variant="outlined"
            label="KRW"
            class="mx-3"
            v-model="krwInput"
            @input="inputEventKrw"
          ></v-text-field>
        </v-row>
      </v-container>
    </v-form>

    <v-progress-circular v-if="isLoading" indeterminate color="#1089FF"></v-progress-circular>

    <!-- 에러 메시지 -->
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
  </v-card>
</template>

<style scoped>
</style>
