<template>
  <div class="max-w-3xl mx-auto space-y-6">

    <div>
      <h2 class="text-2xl font-bold text-white mb-2">افزودن مهارت جدید</h2>
      <p class="text-gray-400">مهارت‌های خود را همراه با آیکون وارد کنید.</p>
    </div>

    <UiCardBlury class="p-6">
      <Form :validation-schema="SkillsSchema" @submit="submitForm" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <div class="md:col-span-2">

          <UiInput 
            rtl
            name="name" 
            label="نام مهارت" 
            placeholder="مثال: Vue.js" 
            v-model="form.name"
          />
        </div>

        <div class="md:col-span-2 flex flex-col sm:flex-row items-start gap-6">
        
          <div class="flex-1 w-full">

            <UiFileAttachment 
              name="icon" 
              label="انتخاب آیکون" 
              accept="image/jpeg, image/png"
              hint="فرمت‌های مجاز: JPG, PNG (حداکثر ۲ مگابایت)"
              v-model="form.icon"
            />
          </div>
  
          <div class="w-32 h-32 shrink-0 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center overflow-hidden shadow-inner">
            <img 
              v-if="imagePreview" 
              :src="imagePreview" 
              class="w-full h-full object-cover transition-transform duration-300 hover:scale-110" 
              alt="پیش‌نمایش آیکون"
            />
            <Icon v-else name="solar:gallery-bold-duotone" class="text-5xl text-gray-500/50" />
          </div>
        </div>

        <div class="md:col-span-2 flex justify-end mt-4 pt-4 border-t border-white/5">
           <UiButton :disabled="loading" variant="gold" type="submit" full class="mt-6 text-md">
               {{ loading ? 'در حال ثبت...' : 'ثبت مهارت' }}
          </UiButton>
        </div>

      </Form>
    </UiCardBlury>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onBeforeUnmount } from 'vue';
import { Form } from 'vee-validate';
import { SkillsSchema } from '~/validation/Skills/CreateSkills';
import { useCustomToastify } from '~/composable/useCustomToasitify';
import { createSkillService } from '~/services/skills/skills.Service';

definePageMeta({ layout: 'dashboard' });

useHead({
  title: 'افزودن مهارت'
});

const loading = ref(false);
const imagePreview = ref(null);


const form = reactive({
  name: '',
  icon: null
});

watch(() => form.icon, (newFile) => {
  if (imagePreview.value) {
    URL.revokeObjectURL(imagePreview.value);
    imagePreview.value = null;
  }
  
  if (newFile) {
    imagePreview.value = URL.createObjectURL(newFile);
  }
});

onBeforeUnmount(() => {
  if (imagePreview.value) {
    URL.revokeObjectURL(imagePreview.value);
  }
});

const { showSuccess } = useCustomToastify();
const router = useRouter();

const submitForm = async () => {
  loading.value = true;
  try {
    const formData = new FormData();
    formData.append('name', form.name);
    
    if (form.icon) {
      formData.append('icon', form.icon);
    }

    await createSkillService(formData);
    showSuccess({
      title: 'ثبت مهارت',
      message: 'آیتم با موفقیت اضافه شد'
    });
    router.push("/dashboard/admin/skills/");
    
  } catch (error) {
    console.error('خطا در ثبت مهارت:', error);
  } finally {
    loading.value = false;
  }
};
</script>
