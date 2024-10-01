<template>
<div class="card">
  <Menubar :model="items">
    <template #item="{ item, props, hasSubmenu }">
      <RouterLink :to="item.route" v-bind="props.action" activeClass="text-primary">
        <span :class="item.icon" />
        <span class="ml-2">{{ item.label }}</span>
        <span v-if="hasSubmenu" class="pi pi-fw pi-angle-down ml-2" />
      </RouterLink>
    </template>
  </Menubar>
</div>
<RouterView>

</RouterView>

<DynamicDialog modal :pt="{root: {style: 'min-width: 80%'}, mask: {style: 'color: yellow;'}}"/>

</template>


<script setup>

import { ref, computed } from 'vue'


const items = ref([
    {
        label: 'Home',
        icon: 'pi pi-home',
        route: '/'
    },
    {
        label: 'Glosses',
        icon: 'pi pi-star',
        route: '/glosses'
    },
    {
        label: 'AddVariation',
        icon: 'pi pi-star',
        route: '/new-expression'
    },
    {
      label: 'AddFrame',
      icon: 'pi pi-star',
      route: '/new-frame'
    },
    {
      label: 'AddRoutine',
      icon: 'pi pi-star',
      route: '/new-routine'
    },
    {
      label: 'AllFrames',
      icon: 'pi pi-star',
      route: '/all-frames'
    },
    {
      label: 'AllRoutines',
      icon: 'pi pi-star',
      route: '/all-routines'
    },
    {
      label: 'AllConstructions',
      icon: 'pi pi-star',
      route: '/all-cxs'
    },
    {
      label: 'Search',
      icon: 'pi pi-search',
      route: '/search'
    }
]);



</script>

<style></style>