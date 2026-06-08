<template>
  <ui-card-blury>
        <h3 class="text-white font-semibold mb-4">تکنولوژی‌های استفاده شده</h3>

        <div class="flex flex-wrap gap-2">
          <div
            v-for="skill in skills"
            :key="skill.id"
            class="backdrop-blur-md transition hover:opacity-50 shadow-2xl p-2 bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5"
          >
            <img v-if="skill.icon" :src="resolveMediaUrl(skill.icon)" class="h-5 w-5 object-contain" :alt="skill.name">
            <Icon v-else name="mdi:code-tags" class="h-5 w-5 text-classic-gold" />
            <span class="text-white text-sm">{{ skill.name }}</span>
          </div>

          <span v-if="skills.length === 0" class="text-gray-500 text-sm">مهارتی ثبت نشده است.</span>
        </div>

        </ui-card-blury>
</template>
<!-- Skill Box Component -->
<script lang="ts" setup>
import type { SkillDTO } from '~/models/Skill/SkillDTO'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

defineProps<{ skills: SkillDTO[] }>()
</script>
