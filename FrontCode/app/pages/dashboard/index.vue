<template>
  <div class="space-y-8">

<DashboardDataCard></DashboardDataCard>


    <div class="grid lg:grid-cols-3 gap-8">
  <DashboardDownloadChartVisitProject></DashboardDownloadChartVisitProject>
   <DashboardNotifBox></DashboardNotifBox>

    </div>

   <DashboardRecentActive></DashboardRecentActive>

  </div>
</template>
<script lang="ts" setup>
/**
 * @page AriaCraftDashboardIndex
 * @description Central administrative overview deck orchestrating primary user metrics, system notifications, and analytics charts.
 * Acts as a layout root layout container for nested data visualizers and telemetry cards.
 * 
 * @architecture
 * - Grid Geometry: deploys a responsive 3-column composite view dividing interactive time-series plots and messaging boxes.
 * - Sub-Component Scope: Lazy-resolves global auto-imported UI elements while strictly declaring explicit localized graphing widgets.
 * - Style Capsule: Implements legacy layout classes (`.stat-card`, `.project-row`) scoped to secure layout presentation boundaries.
 * 
 * @metadata
 * - SEO Layer: Populates standard meta keys and access authorship configurations onto the active document head context.
 */
import DownloadChartVisitProject from '~/components/Dashboard/DownloadChartVisitProject.vue';
import CardBlury from '~/components/Ui/CardBlury.vue';
import { generateSeoMeta } from '~/utilities/seo';

definePageMeta({
  layout: "dashboard"
})

const seo = generateSeoMeta({
      title: `داشبورد آریا کرفت`,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["افزودن پروژه"],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)
</script>
<style scoped>

.stat-card{
display:flex;
align-items:center;
gap:14px;
padding:20px;
border-radius:16px;
background:rgba(255,255,255,0.04);
border:1px solid rgba(255,255,255,0.08);
backdrop-filter:blur(12px);
transition:.25s
}

.stat-card:hover{
border-color:#d4af37;
background:rgba(255,255,255,0.06)
}

.stat-icon{
width:46px;
height:46px;
display:flex;
align-items:center;
justify-content:center;
border-radius:12px;
background:rgba(212,175,55,0.15);
color:#d4af37
}

.stat-number{
font-size:20px;
font-weight:700;
color:white
}

.stat-label{
font-size:14px;
color:#9ca3af
}


.project-row{
display:flex;
justify-content:space-between;
align-items:center;
padding:12px 0;
border-bottom:1px solid rgba(255,255,255,0.05)
}

.notification{
display:flex;
align-items:center;
gap:10px;
color:#d1d5db
}

.activity{
display:flex;
align-items:center;
gap:10px;
color:#d1d5db
}

.dot{
width:8px;
height:8px;
border-radius:50%;
background:#d4af37
}

</style>
