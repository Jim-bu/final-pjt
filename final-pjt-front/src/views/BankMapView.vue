<template>
  <div>
    <h1>근처 은행 찾기</h1>
    <Map />
  </div>
</template>

<script>
import Map from "@/components/Map.vue";

export default {
  name: "BankMapView",
  components: { Map },
};
</script>
