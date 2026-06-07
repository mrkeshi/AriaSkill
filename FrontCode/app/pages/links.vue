<template>
  <section class="my-8">
    <UiCardBlury>
      <!-- هدر سکشن -->
      <div class="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
        <div class="p-2 bg-classic-gold/20 rounded-lg text-classic-gold">
          <Icon name="mdi:link-box-variant-outline" class="text-2xl" />
        </div>
        <div>
          <h2 class="text-xl font-bold text-white">لیست صفحات طراحی شده</h2>
          <p class="text-sm text-gray-400 mt-1">جهت تحویل و بررسی توسط تیم بک‌اند</p>
        </div>
      </div>

      <!-- جدول لینک‌ها -->
      <div class="overflow-x-auto rounded-xl border border-white/10">
        <table class="w-full text-right text-sm text-gray-300">
          <thead class="bg-white/10 text-white font-medium uppercase tracking-wider">
            <tr>
              <th scope="col" class="px-6 py-4 w-16 text-center">ردیف</th>
              <th scope="col" class="px-6 py-4">نام صفحه</th>
              <th scope="col" class="px-6 py-4">توضیحات</th>
              <th scope="col" class="px-6 py-4 w-32 text-center">عملیات</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/10 bg-slate-900/20">
            <tr v-for="(page, index) in pages" :key="index" class="hover:bg-white/5 transition-colors duration-200">
              <td class="px-6 py-4 text-center text-gray-500 font-mono">{{ index + 1 }}</td>
              <td class="px-6 py-4 font-medium text-white flex items-center gap-2 whitespace-nowrap">
                <Icon :name="page.icon" class="text-classic-gold text-lg" />
                {{ page.name }}
              </td>
              <td class="px-6 py-4 text-gray-400 min-w-[200px]">{{ page.description }}</td>
              <td class="px-6 py-4 text-center">
                <a 
                  :href="page.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-slate-900 bg-classic-gold rounded-lg hover:bg-yellow-400 hover:shadow-[0_0_15px_rgba(212,175,55,0.4)] transition-all whitespace-nowrap"
                >
                  مشاهده
                  <Icon name="mdi:open-in-new" class="text-sm" />
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UiCardBlury>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { generateSeoMeta } from '~/utilities/seo';

const pages = ref([
  
   {
    name: 'صفحه اصلی',
    description: 'صفحه اصلی و لندینگ پیج سایت',
    url: '/',
    icon: 'mdi:home'
  },
    {
    name: 'درباره ما',
    description: 'این صفحه درباره سایت می باشد که البته تزئینی و بدون کاربرد هست',
    url: '/about',
    icon: 'mdi:about'
  },
  {
    name: 'وبلاگ',
    description: 'صفحه تزئینی وبلاگ، این صفحه قرار نیست طراحی بشود یا کاری انجام دهد.',
    url: '/blog',
    icon: 'mdi:post'
  },
  {
    name: 'جستجوی پروژه',
    description: 'صفحه جستجو برای پروژه، که اختیاری هست با الاستیک سرچ پیاده شود.',
    url: '/explore',
    icon: 'mdi:search'
  },
  {
    name: 'سینگل پروژه',
    description: 'صفحه تکی مربوط به یک پروژه هست که اطلاعات پروژه را به صورت کامل نشان میدهد.',
    url: '/projects/pr-fdg',
    icon: 'mdi:folder-open'
  },
  {
    name: 'فیلترکردن پروژه',
    description: 'در این قسمت پروژه ها بر اساس دسته بندی و.. فیلتر و نمایش داده میشوند',
    url: '/projects/filter',
    icon: 'mdi:filter'
  },
  {
    name: 'ورود',
    description: 'صفحه ای که برای ورود کاربران مورد استفاده قرار میگیرد',
    url: '/user/login',
    icon: 'mdi:login'
  },
   {
    name: 'ثبت نام',
    description: 'این قسمت برای ثبت نام کاربران هم از طریق گوگل هم از طریق نام نویسی طراحی شده است',
    url: '/user/register',
    icon: 'mdi:register'
  },
   {
    name: 'فراموشی رمز عبور',
    description: 'صفحه ای که برای فراموشی رمز عبور استفاده می شود',
    url: '/user/forgotpass',
    icon: 'mdi:lock'
  },
  {
    name: 'تغییر پسورد',
    description: 'در این صفحه، رمز عبور ورود کاربر تغییر داده می شود.',
    url: '/user/resetpass',
    icon: 'mdi:lock-open'
  },
  {
    name: 'مشاهده پروفایل',
    description: 'در این قسمت میتوانید اطلاعات پروفایل یک نفر را مشاهده کنید',
    url: '/@ali',
    icon: 'mdi:account-group'
  },  
  {
    name: 'داشبورد',
    description: 'صفحه داشبورد کاربران می باشد که میتوانند اطلاعات تحلیلی و آمار ها را مشاهده کنند.',
    url: '/dashboard',
    icon: 'mdi:view-dashboard-outline'
  },
  {
    name: 'ویرایش پروفایل',
    description: 'در این قسمت کاربر میتواند اطلاعات پروفایلش را ویرایش کند.',
    url: '/dashboard/profile',
    icon: 'mdi:account-edit'
  },

  {
    name: 'افزودن پروژه جدید',
    description: 'فرم ثبت پروژه با قابلیت آپلود فایل، تصویر و جستجوی تکنولوژی‌ها',
    url: '/dashboard/projects/add',
    icon: 'mdi:plus-box-outline'
  },
  {
    name: 'مدیریت پروژه‌ها',
    description: 'جدول لیست پروژه‌ها به همراه تکنولوژی‌های استفاده شده',
    url: '/dashboard/projects',
    icon: 'mdi:tag-outline'
  },
  {
    name: 'مدیریت نظرات',
    description: 'جدول لیست نظرات کاربران با قابلیت پاسخگویی',
    url: '/dashboard/comments',
    icon: 'mdi:comment-multiple-outline'
  },
   {
    name: 'نوتیفیکیشن',
    description: 'صفحه مشاهده نوتیفیکیشن های ارسالی',
    url: '/dashboard/notifications',
    icon: 'mdi:bell'
  },
]);
const seo = generateSeoMeta({
      title: `پیشرو کونی`,
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
.bg-classic-gold { background-color: #D4AF37; }
.text-classic-gold { color: #D4AF37; }
</style>
