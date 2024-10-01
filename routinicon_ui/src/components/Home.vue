<template>
  <Card style="width: 40rem; margin: auto; margin-top: 5rem;" class="pd-card" :pt="{header: {class: 'bg-primary border-round-lg'}}">
        <template #header>
          <div style="height: 1rem;"></div>
        </template>
        <template #title>Main page</template>
        <template #content>
            <p class="m-0">
              {{ this.placeholder }}
            </p>
        </template>
    </Card>

  
</template>


<script>
export default {
  data()  {
    return {
    placeholder: "Here will be some info"
    }
  }
}
</script>

<style>
.bg-primary {
    background-color: #10b981;

}
.pd-card {
    overflow: hidden;
    
}
</style>