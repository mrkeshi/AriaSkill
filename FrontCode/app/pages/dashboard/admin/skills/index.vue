<template>
  <UiCardBlury>
 <Confirm
      v-model="isdel"
      title="حذف مهارت"
      description="آیا برای حذف این آیتم مطمئن هستید؟"
      @confirm="deleteItem"
    />

    <div class="transition-all">

      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-white tracking-wide">مدیریت مهارت‌ها</h2>
        <div class="flex items-center gap-3">

          <span class="bg-classic-gold/10 text-classic-gold border border-classic-gold/30 px-3 py-1 rounded-full text-xs">
            {{ skills.length }} مهارت ثبت شده
          </span>
          <NuxtLink to="/dashboard/admin/skills/create" class="bg-classic-gold text-slate-900 hover:bg-yellow-400 px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-all shadow-[0_0_15px_rgba(212,175,55,0.2)]">
            <Icon name="mdi:plus" class="text-lg" />
            افزودن جدید
          </NuxtLink>
        </div>
      </div>

      <SkeletonSimple v-if="pending" :repeat="5" class="h-16 mb-2" />


      <div v-else class="overflow-x-auto rounded-xl border border-white/10 bg-white/5 backdrop-blur-md shadow-inner">
        <table class="w-full text-right whitespace-nowrap">
          <thead class="bg-white/5 text-gray-300 text-sm border-b border-white/10">
            <tr>
              <th class="p-4 font-medium w-16">#</th>
              <th class="p-4 font-medium">آیکون</th>
              <th class="p-4 font-medium">نام مهارت</th>
              <th class="p-4 font-medium">شناسه (Slug)</th>
              <th class="p-4 font-medium">عملیات</th>
            </tr>
          </thead>

          <tbody class="text-gray-200 text-sm divide-y divide-white/5">
            <tr
              v-for="(item, index) in skills"
              :key="item.id"
              class="hover:bg-white/5 transition duration-200 group"
            >
              <td class="p-4 text-gray-500 group-hover:text-gray-400 transition">{{ index + 1 }}</td>
              <td class="p-4">
                <div class="w-10 h-10 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center shadow-inner group-hover:border-classic-gold/30 transition-colors">
                <img :src="item.icon" class="w-10 h-10" alt="">
                </div>
              </td>
              <td class="p-4 font-medium text-white/90">{{ item.name }}</td>
              <td class="p-4 text-gray-400 font-mono text-xs dir-ltr">
                <span class="px-2 py-1 rounded-md bg-black/20 border border-white/5">{{ item.slug }}</span>
              </td>
              <td class="p-4">
                <div class="flex gap-2">
<NuxtLink
  :to="`/dashboard/admin/skills/editskills?id=${item.id}`"
  class="bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 p-2 rounded-lg text-blue-400 transition inline-flex items-center justify-center"
>
  <Icon name="mdi:pencil-outline" class="text-lg" />
</NuxtLink>
                  <button @click="delid=item.id;isdel=true" class="bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 p-2 rounded-lg text-rose-400 transition"><Icon name="mdi:trash-can-outline" class="text-lg mt-1"/></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>


        <div v-if="skills.length === 0" class="p-8 text-center text-gray-500 flex flex-col items-center gap-3">
           <Icon name="mdi:database-off-outline" class="text-4xl text-gray-600" />
           <p>هیچ مهارتی یافت نشد.</p>
        </div>
      </div>

  
      <div v-if="skills.length > 0" class="mt-6 flex justify-center">
              <UiPagination :totalPages="totalPages" />
      </div>
    </div>
  </UiCardBlury>
</template>

<script setup>
import { useCustomToastify } from '~/composable/useCustomToasitify';
import { deleteSkillsService, getSkillsService } from '~/services/skills/skills.Service';

definePageMeta({ layout: 'dashboard' })
useHead({ title: 'لیست مهارت‌ها' });

const isdel=ref(false)
const delid=ref(0)
const route = useRoute();

const currentPage = computed(() => Number(route.query.page) || 1);


const { data,refresh, pending } = await useAsyncData(
  "skills-list",
  () => getSkillsService(currentPage.value),
  {
    watch: [currentPage] 
  }
);

const skills = computed(() => data.value?.data?.results || []);

const totalPages = computed(() => {
  const count = data.value?.data?.count || 0;
  return Math.ceil(count / 10); 
});
const {showInfo}=useCustomToastify()
const deleteItem=async()=>{
  await deleteSkillsService(delid.value).then((_)=>{
    showInfo({title:'حذف مهارت',message:'مهارت با موفقیت حذف شد.'})
    refresh()
  })
}
</script>
