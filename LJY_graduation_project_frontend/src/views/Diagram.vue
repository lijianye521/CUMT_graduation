<template>
  <div>
    <AccuracyChart />
  </div>
  <div>
    <EpochChart />
  </div>
  <div>
    <CompareChart />
  </div>
</template>

<script>
import AccuracyChart from '@/components/AccuracyChart.vue'
import EpochChart from '@/components/EpochChart.vue'
import CompareChart from '@/components/CompareChart.vue'
export default {
  components: {
    AccuracyChart,
    EpochChart,
    CompareChart
  }
}
</script>
