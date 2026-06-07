<template>
  <UiCardBlury>
    <Confirm
      v-model="deleteModal"
      title="حذف کاربر"
      :description="deleteDescription"
      @confirm="deleteUser"
    />

    <Transition name="overlay">
      <div
        v-if="passwordModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
      >
        <Transition name="modal">
          <div class="w-full max-w-md mx-4 rounded-2xl border border-white/10 bg-black/60 backdrop-blur-xl p-8 shadow-xl">
            <h2 class="text-xl font-bold text-bone-white text-center">تغییر رمز عبور</h2>
            <p class="text-gray-400 text-center mt-3">
              {{ selectedUser?.username || selectedUser?.email }}
            </p>

            <form class="mt-8 space-y-4" @submit.prevent="changePassword">
              <div>
                <label class="block text-sm font-medium mb-2 text-bone-white" for="admin-user-password">رمز عبور جدید</label>
                <input
                  id="admin-user-password"
                  v-model="passwordForm.password"
                  type="password"
                  class="w-full px-4 py-3 rounded-lg border border-white/10 bg-white/5 text-white focus:ring-1 focus:ring-classic-gold focus:border-classic-gold outline-none transition-all dir-ltr text-left"
                  autocomplete="new-password"
                  required
                >
              </div>

              <div>
                <label class="block text-sm font-medium mb-2 text-bone-white" for="admin-user-password-confirm">تکرار رمز عبور</label>
                <input
                  id="admin-user-password-confirm"
                  v-model="passwordForm.password_confirm"
                  type="password"
                  class="w-full px-4 py-3 rounded-lg border border-white/10 bg-white/5 text-white focus:ring-1 focus:ring-classic-gold focus:border-classic-gold outline-none transition-all dir-ltr text-left"
                  autocomplete="new-password"
                  required
                >
              </div>

              <div class="flex items-center justify-center gap-4 pt-4">
                <button
                  type="button"
                  class="px-5 py-2 rounded-xl bg-white/10 text-gray-300 hover:bg-white/20 transition"
                  @click="closePasswordModal"
                >
                  لغو
                </button>
                <button
                  type="submit"
                  :disabled="passwordLoading"
                  class="flex items-center justify-center gap-2 px-5 py-2 rounded-xl bg-classic-gold text-black font-semibold min-w-[130px] disabled:opacity-60"
                >
                  <Icon v-if="passwordLoading" name="mdi:loading" class="animate-spin text-xl" />
                  <span>{{ passwordLoading ? 'در حال ثبت' : 'ثبت تغییرات' }}</span>
                </button>
              </div>
            </form>
          </div>
        </Transition>
      </div>
    </Transition>

    <div class="transition-all">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between mb-6">
        <div>
          <h2 class="text-xl font-bold text-white tracking-wide">مدیریت کاربران</h2>
          <p class="text-sm text-gray-400 mt-2">مشاهده، جستجو و مدیریت وضعیت حساب‌های کاربری</p>
        </div>

        <span class="bg-cyan-400/10 text-cyan-300 border border-cyan-400/30 px-3 py-1 rounded-full text-xs w-fit">
          {{ toPersianNumerals(totalUsers) }} کاربر
        </span>
      </div>

      <form class="mb-5 flex flex-col gap-3 md:flex-row" @submit.prevent="submitSearch">
        <div class="relative flex-1">
          <Icon name="mdi:magnify" class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 text-xl" />
          <input
            v-model="searchInput"
            type="search"
            placeholder="جستجو بر اساس نام کاربری، ایمیل یا نام"
            class="w-full rounded-xl border border-white/10 bg-white/5 py-3 pr-12 pl-4 text-white placeholder:text-gray-500 outline-none transition focus:border-classic-gold/60 focus:bg-white/10"
          >
        </div>

        <div class="flex gap-2">
          <button
            type="submit"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-classic-gold px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-yellow-400"
          >
            <Icon name="mdi:magnify" class="text-lg" />
            جستجو
          </button>
          <button
            v-if="searchQuery"
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-gray-300 transition hover:bg-white/10"
            @click="clearSearch"
          >
            <Icon name="mdi:close" class="text-lg" />
            پاک کردن
          </button>
        </div>
      </form>

      <SkeletonSimple v-if="pending" :repeat="5" class="h-16 mb-2" />

      <div v-else class="overflow-x-auto rounded-xl border border-white/10 bg-white/5 backdrop-blur-md shadow-inner">
        <table class="w-full text-right whitespace-nowrap">
          <thead class="bg-white/5 text-gray-300 text-sm border-b border-white/10">
            <tr>
              <th class="p-4 font-medium w-16">#</th>
              <th class="p-4 font-medium">کاربر</th>
              <th class="p-4 font-medium">ایمیل</th>
              <th class="p-4 font-medium">نقش</th>
              <th class="p-4 font-medium">وضعیت</th>
              <th class="p-4 font-medium">آخرین ورود</th>
              <th class="p-4 font-medium">عملیات</th>
            </tr>
          </thead>

          <tbody class="text-gray-200 text-sm divide-y divide-white/5">
            <tr
              v-for="(item, index) in users"
              :key="item.id"
              class="hover:bg-white/5 transition duration-200 group"
            >
              <td class="p-4 text-gray-500 group-hover:text-gray-400 transition">
                {{ toPersianNumerals((currentPage - 1) * pageSize + index + 1) }}
              </td>
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <div class="h-11 w-11 overflow-hidden rounded-xl border border-white/10 bg-white/5 flex items-center justify-center text-cyan-300">
                    <img
                      v-if="item.avatar"
                      :src="resolveMediaUrl(item.avatar)"
                      :alt="item.username"
                      class="h-full w-full object-cover"
                    >
                    <Icon v-else name="mdi:account-outline" class="text-2xl" />
                  </div>
                  <div>
                    <p class="font-medium text-white/90">{{ displayName(item) }}</p>
                    <p class="text-xs text-gray-500 dir-ltr text-left">{{ item.username }}</p>
                  </div>
                </div>
              </td>
              <td class="p-4 text-gray-300 dir-ltr text-left">{{ item.email }}</td>
              <td class="p-4">
                <span
                  class="px-2 py-1 rounded-md border text-xs"
                  :class="item.is_superuser || item.is_staff ? 'bg-cyan-400/10 text-cyan-300 border-cyan-400/30' : 'bg-white/5 text-gray-300 border-white/10'"
                >
                  {{ roleLabel(item) }}
                </span>
              </td>
              <td class="p-4">
                <span
                  class="inline-flex items-center gap-2 px-2 py-1 rounded-md border text-xs"
                  :class="item.is_active ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' : 'bg-rose-500/10 text-rose-300 border-rose-500/30'"
                >
                  <span class="h-2 w-2 rounded-full" :class="item.is_active ? 'bg-emerald-400' : 'bg-rose-400'"></span>
                  {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                </span>
              </td>
              <td class="p-4 text-gray-400">{{ toJalali(item.last_login) }}</td>
              <td class="p-4">
                <div class="flex gap-2">
                  <button
                    class="border p-2 rounded-lg transition inline-flex items-center justify-center"
                    :class="item.is_active ? 'bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/30 text-amber-300' : 'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30 text-emerald-300'"
                    :disabled="statusLoadingId === item.id || isCurrentUser(item)"
                    :title="item.is_active ? 'غیرفعال کردن' : 'فعال کردن'"
                    @click="toggleStatus(item)"
                  >
                    <Icon v-if="statusLoadingId === item.id" name="mdi:loading" class="text-lg animate-spin" />
                    <Icon v-else :name="item.is_active ? 'mdi:account-cancel-outline' : 'mdi:account-check-outline'" class="text-lg" />
                  </button>

                  <button
                    class="bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 p-2 rounded-lg text-blue-400 transition inline-flex items-center justify-center"
                    title="تغییر رمز عبور"
                    @click="openPasswordModal(item)"
                  >
                    <Icon name="mdi:key-outline" class="text-lg" />
                  </button>

                  <button
                    class="bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 p-2 rounded-lg text-rose-400 transition inline-flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isCurrentUser(item)"
                    title="حذف کاربر"
                    @click="openDeleteModal(item)"
                  >
                    <Icon name="mdi:trash-can-outline" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="users.length === 0" class="p-8 text-center text-gray-500 flex flex-col items-center gap-3">
          <Icon name="mdi:account-search-outline" class="text-4xl text-gray-600" />
          <p>کاربری یافت نشد.</p>
        </div>
      </div>

      <div v-if="users.length > 0" class="mt-6 flex justify-center">
        <UiPagination :totalPages="totalPages" />
      </div>
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
import type { AdminUserDTO } from '~/models/User/UserDTO'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { changeAdminUserPasswordService, deleteAdminUserService, getAdminUsersService, updateAdminUserStatusService } from '~/services/user/user.Service'
import { toJalali, toPersianNumerals } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

definePageMeta({ layout: 'dashboard' })
useHead({ title: 'مدیریت کاربران' })

const route = useRoute()
const auth = useAuthStore()
const { showInfo } = useCustomToastify()

const pageSize = 8
const deleteModal = ref(false)
const passwordModal = ref(false)
const selectedUser = ref<AdminUserDTO | null>(null)
const searchInput = ref(String(route.query.search || ''))
const statusLoadingId = ref<number | null>(null)
const passwordLoading = ref(false)
const passwordForm = reactive({
  password: '',
  password_confirm: '',
})

const currentPage = computed(() => Number(route.query.page) || 1)
const searchQuery = computed(() => String(route.query.search || '').trim())

const { data, refresh, pending } = await useAsyncData(
  'admin-users-list',
  () => getAdminUsersService(currentPage.value, searchQuery.value),
  {
    watch: [currentPage, searchQuery],
  },
)

const users = computed(() => data.value?.data?.results || [])
const totalUsers = computed(() => data.value?.data?.count || 0)
const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize))
const deleteDescription = computed(() => {
  const name = selectedUser.value?.username || selectedUser.value?.email || ''
  return `آیا برای حذف ${name} مطمئن هستید؟`
})

watch(searchQuery, (value) => {
  searchInput.value = value
})

const displayName = (user: AdminUserDTO) => {
  const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim()
  return fullName || user.username || user.email
}

const roleLabel = (user: AdminUserDTO) => {
  if (user.is_superuser) return 'مدیر کل'
  if (user.is_staff) return 'مدیر'
  return 'کاربر'
}

const isCurrentUser = (user: AdminUserDTO) => user.email === auth.user.email

const submitSearch = async () => {
  await navigateTo({
    query: {
      ...route.query,
      page: undefined,
      search: searchInput.value.trim() || undefined,
    },
  })
}

const clearSearch = async () => {
  searchInput.value = ''
  await navigateTo({
    query: {
      ...route.query,
      page: undefined,
      search: undefined,
    },
  })
}

const openDeleteModal = (user: AdminUserDTO) => {
  selectedUser.value = user
  deleteModal.value = true
}

const deleteUser = async () => {
  if (!selectedUser.value) return
  await deleteAdminUserService(selectedUser.value.id)
  showInfo({ title: 'حذف کاربر', message: 'کاربر با موفقیت حذف شد.' })
  selectedUser.value = null
  await refresh()
}

const toggleStatus = async (user: AdminUserDTO) => {
  statusLoadingId.value = user.id
  try {
    await updateAdminUserStatusService(user.id, !user.is_active)
    showInfo({
      title: 'وضعیت حساب',
      message: user.is_active ? 'حساب کاربر غیرفعال شد.' : 'حساب کاربر فعال شد.',
    })
    await refresh()
  } finally {
    statusLoadingId.value = null
  }
}

const openPasswordModal = (user: AdminUserDTO) => {
  selectedUser.value = user
  passwordForm.password = ''
  passwordForm.password_confirm = ''
  passwordModal.value = true
}

const closePasswordModal = () => {
  if (passwordLoading.value) return
  passwordModal.value = false
  selectedUser.value = null
}

const changePassword = async () => {
  if (!selectedUser.value) return
  passwordLoading.value = true
  try {
    await changeAdminUserPasswordService(selectedUser.value.id, passwordForm)
    showInfo({ title: 'تغییر رمز عبور', message: 'رمز عبور کاربر با موفقیت تغییر کرد.' })
    passwordModal.value = false
    selectedUser.value = null
  } finally {
    passwordLoading.value = false
  }
}
</script>
