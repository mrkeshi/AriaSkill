<template>
  <div :class="['grid','grid-cols-1', 'my-8 sm:grid-cols-2' , `lg:grid-cols-${lgGrid}` ,'gap-8',] ">

  <ProjectCard
    v-for="project in projects"
    :key="project.id"
    :project="project"
    :min="props.min"
  />
  </div>
</template>

<script lang="ts" setup>
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import type { PropType } from 'vue'

const props= defineProps({
  projects:{
    type:Array as PropType<ProjectDTO[]>,
    default:() => []
  },
  lgGrid:{
    type:String,
    default:'3',
  },
  min:{
    type:Boolean,
    default:false
  }
})
</script>

<style>

</style>
