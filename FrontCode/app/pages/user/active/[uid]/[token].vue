
<template>
  <div>
    <transition name="slide-up">
      <SimpleCard
        v-if="showCard"
        title="فعالسازی اکانت!"
        description="اکانت شما با موفقیت در سایت آریا کرفت فعال شد"
        icon="mdi:account-check-outline"
        to="index"
        to-name="بازگشت به صفحه لاگین"
      />
    </transition>


  </div>
</template>

<script setup lang="ts">
import {ref } from 'vue'

import SimpleCard from '~/components/Ui/SimpleCard.vue'
import type { ActiveUserDTO} from '~/models/User/AuthDTO'
import { generateSeoMeta } from '~/utilities/seo'
import { activeUserService, changePasswordService } from '~/services/user/user.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
const {showError,showSuccess}=useCustomToastify()
const loading = ref(false)
const showCard = ref(false)
const route=useRoute()
const pa:ActiveUserDTO=reactive({

  uid:'',
  token:''
})


  

  onMounted(async () => {
  pa.uid=route.params.uid as string
  pa.token=route.params.token as string
  loading.value = true

  try{
    await activeUserService(pa)
    showCard.value = true

    
  }catch(e){
    showError({title:"خطا",message:"خطا در فعالسازی اکانت شما، ممکن است اکانت فعال باشد یا توکن شما اشتباه باشد"})
  }finally{
   loading.value = false
  
  }
})
const seo = generateSeoMeta({
      title: `فعالسازی اکانت  `,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["فعالسازی اکانت "],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)

</script>
