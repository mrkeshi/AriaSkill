// ApexCharts plugin to register the Vue component globally
import VueApexCharts from 'vue3-apexcharts'
 
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueApexCharts)
  nuxtApp.vueApp.component('apexchart', VueApexCharts)
})
 
