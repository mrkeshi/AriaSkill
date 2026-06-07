<template>
<UiCardBlury>
        <div class="flex flex-wrap items-center justify-between gap-4 text-gray-300 text-sm">
          <span class="flex items-center gap-2">
            <Icon name="mdi:calendar" class="text-light-gold text-lg"/>
            {{ toJalaliLong(project.created_at) }}
          </span>
          <div class="flex items-center gap-2 text-gray-300 text-sm">
            <Icon name="mdi:shape-outline" class="text-light-gold text-lg"/>
            {{ project.project_type_display || project.project_type }}
          </div>
          <span class="flex items-center gap-2">
            <Icon name="mdi:comment-outline" class="text-light-gold text-lg"/>
            {{ project.comments_count }} نظر
          </span>
        </div>
    </UiCardBlury>
</template>

<script lang="ts" setup>
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import { toJalaliLong } from '~/utilities/dateHelpers'

defineProps<{ project: ProjectDTO }>()
</script>
