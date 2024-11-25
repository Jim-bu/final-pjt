<template>
  <div class="map-component">
    <div class="controls">
      <label>
        도/광역시:
        <select v-model="selectedProvince" @change="updateCities">
          <option disabled value="">도/광역시 선택</option>
          <option v-for="info in mapStore.infos" :key="info.id" :value="info.prov">
            {{ info.prov }}
          </option>
        </select>
      </label>

      <label>
        도시:
        <select v-model="selectedCity" :disabled="!selectedProvince">
          <option disabled value="">도시 선택</option>
          <option v-for="city in availableCities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </label>

      <label>
        은행:
        <select v-model="selectedBank">
          <option disabled value="">은행 선택</option>
          <option v-for="bank in mapStore.banks" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </label>

      <button class="search-btn" @click="searchOnMap">검색</button>
    </div>

    <div id="mapContainer" class="map"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useMapStore } from "@/stores/map";
import { loadKakaoMap } from "@/stores/map";

// Kakao 지도 객체와 관련된 상태
const map = ref<any>(null);
const markers = ref<any[]>([]);
const infowindow = ref<any>(null);

// Pinia 상태
const mapStore = useMapStore();
const selectedProvince = ref("");
const selectedCity = ref("");
const selectedBank = ref("");

// 선택한 도/광역시에 따른 도시 목록 계산
const availableCities = computed(() => {
  const selectedInfo = mapStore.infos.find((info) => info.prov === selectedProvince.value);
  return selectedInfo ? selectedInfo.city : [];
});

// 지도 초기화
const initializeMap = async () => {
  try {
    const kakao = await loadKakaoMap();
    kakao.maps.load(() => {
      const mapContainer = document.getElementById("mapContainer");
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 서울 중심
        level: 3,
      };

      map.value = new kakao.maps.Map(mapContainer, mapOption);
      infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 });
    });
  } catch (error) {
    console.error("지도 초기화 실패:", error);
  }
};

// 검색 기능
const searchOnMap = () => {
  if (!selectedProvince.value || !selectedCity.value || !selectedBank.value) {
    alert("모든 항목을 선택해주세요.");
    return;
  }

  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`;
  performSearch(keyword);
};

// Kakao Places API로 장소 검색
const performSearch = (keyword: string) => {
  const kakao = (window as any).kakao;
  const ps = new kakao.maps.services.Places();

  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      displayMarkers(data);

      // 첫 번째 결과를 중심으로 지도 이동
      if (data.length > 0) {
        const firstPlace = data[0];
        map.value.setCenter(new kakao.maps.LatLng(firstPlace.y, firstPlace.x));
      }
    } else {
      alert("검색 결과가 없습니다.");
    }
  });
};

// 마커 표시
const displayMarkers = (places: any[]) => {
  const kakao = (window as any).kakao;

  // 기존 마커 제거
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];

  places.forEach((place) => {
    const marker = new kakao.maps.Marker({
      map: map.value,
      position: new kakao.maps.LatLng(place.y, place.x),
    });

    kakao.maps.event.addListener(marker, "click", () => {
      infowindow.value.setContent(`
        <div style="padding:5px;">
          <strong>${place.place_name}</strong><br>
          도로명 주소: ${place.road_address_name || "정보 없음"}<br>
          지번 주소: ${place.address_name || "정보 없음"}<br>
          전화번호: ${place.phone || "정보 없음"}<br>
          <a href="${place.place_url}" target="_blank">자세히 보기</a>
        </div>
      `);
      infowindow.value.open(map.value, marker);
    });

    markers.value.push(marker);
  });
};

// 도시 목록 초기화
const updateCities = () => {
  selectedCity.value = "";
};

// 컴포넌트 마운트 시 지도 초기화
onMounted(() => {
  initializeMap();
});
</script>

<style scoped>
.map-component {
  max-width: 600px;
  margin: 0 auto;
  font-family: "Arial", sans-serif;
}

.controls {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.controls label {
  display: flex;
  flex-direction: column;
  font-size: 14px;
  color: #333;
}

.controls select {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-btn {
  background-color: #b8ac8e;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #857945;
}

.map {
  width: 100%;
  height: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
