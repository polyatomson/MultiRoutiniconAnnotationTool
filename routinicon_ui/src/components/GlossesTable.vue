<template>
  <Card style="overflow: hidden;">
    <template #content>

    <!-- <Button @click="fetchData">Fetch Data</button> -->
  <ContextMenu ref="cm" :model="menuModel" @hide="selectedRow = null" />

    <DataTable :multiSortMeta="[{'field': 'row_number', 'order': 1}]"
    sortMode="multiple" v-model:filters="filters" 
    filterDisplay="row" 
    :globalFilterFields="['gloss', 'class']" 
    v-model:editingRows="editingRows" 
    :value="glosses" 
    editMode="row" 
    dataKey="row_number" 
    @row-edit-save="onRowEditSave"
    contextMenu
    v-model:contextMenuSelection="selectedRow"
    @rowContextmenu="onRowContextMenu"
    :pt="{
        table: { style: 'min-width: 50rem' },
        column: {
            bodycell: ({ state }) => ({
              style:  state['d_editing'] && 'padding-top: 0.6rem; padding-bottom: 0.6rem'
            })
        }
    }">
    <template #header>
                <div>
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </span>
                </div>
      </template>
    <Column field="gloss_id" header="ID" sortable></Column>
    <Column field="gloss" header="Gloss" sortable>
      <template #editor="{ data, field, index }">
        <div>
          <InputText v-model="data[field]" :class="{'p-invalid': GlossExists(data[field], index)}" />
        </div>
          </template>
        <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by gloss" />
        </template>
      </Column>
    
    <Column field="lex" header="Lexical" sortable>
      <template #editor="{ data, field }">
        <Dropdown v-model="data[field]" :options="lex_options" optionLabel="label" optionValue="value">
        </Dropdown>
        </template>
        <template #filter="{ filterModel, filterCallback }">
                    <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="lex_options_filter" class="p-column-filter" style="min-width: 12rem" :showClear="true">
                    </Dropdown>
        </template>
    </Column>
    <Column field="class" header="Class" sortable>
      <template #editor="{ data, field }">
            <InputText v-model="data[field]" />
        </template>
        <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by class" />
        </template>
    </Column>
    <Column :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
  </DataTable>

</template>
</Card>
<Dialog v-model:visible="dialog_show" modal :header="'Gloss ' + examplesForRowR + ' (id' + examplesForRowID + ')'" :style="{ width: '70%' }">
  <glossing-examples :gloss_id="examplesForRowID" :gloss="examplesForRowR"/>
</Dialog>
  </template>
  
  <script>
  import { FilterMatchMode } from 'primevue/api';
  // import { markRaw, defineAsyncComponent } from 'vue';
  // import { useDialog } from 'primevue/usedialog';
  // import GlossingExamples from './GlossingExamples.vue'
  

  // const GlossingExamples = defineAsyncComponent(() => import('./GlossingExamples.vue'));
  export default {
    
    data() {
      return {
        editingRows: [],
        glosses: null,
        lex_options: [{label: "true", value: true}, {label: "false", value: false}],
        lex_options_filter: ["true","false"],
        examples: null,
        dialog_show: false,
        examplesForRowID: null,
        examplesForRowR: null,
        filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                gloss: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                class: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                lex: { value: null, matchMode: FilterMatchMode.EQUALS }
            },
        selectedRow: null,
        menuModel: [
                {label: 'Insert row', icon: 'pi pi-plus pi-times', command: () => this.insertRow(this.selectedRow)},
                {label: 'Delete row', icon: 'pi pi-trash pi-times', command: () => this.deleteRow(this.selectedRow)},
                {label: 'Info', icon: 'pi pi-search', command: () => this.showExamples(this.selectedRow)}
            ]

      }
    },
      methods: {
        onRowContextMenu(event) {
          this.$refs.cm.show(event.originalEvent);
        },

        shiftRowNumeration(rowArray, shiftLocation, up) {
          if (up) {
          for (let index = 0; index < rowArray.length; index++) {
            if (rowArray[index].row_number > shiftLocation) {
              rowArray[index].row_number += 1;
            }
            
          }}
          else {
            for (let index = 0; index < rowArray.length; index++) {
            if (rowArray[index].row_number > shiftLocation) {
              rowArray[index].row_number -= 1;
          }
        }}
      },

        insertRow(row) {
          console.log('inserting after', row.row_number);
          const new_row_number = row.row_number + 1;
          // console.log('new row number', new_row_number);
          this.shiftRowNumeration(this.glosses, row.row_number, true);
          this.glosses.splice(row.row_number, 0, 
          {'gloss_id': 'new', 'gloss': '', 'lex': true, 
          'class': '', row_number: new_row_number}
          );
        },

        deleteRow(row) {
          // console.log(row.gloss_id)
          if (row.gloss_id !== 'new') {
            this.markGlossUselessInDB(row.gloss_id)
            // console.log('before', this.glosses)
            this.glosses.splice((row.row_number-1), 1)
            // console.log(row.row_number)
            // console.log(this.glosses)
            this.shiftRowNumeration(this.glosses, row.row_number, false)
          }
        },

        showExamples(row) {
          console.log('showExamples', row)
          if (row.gloss_id !== 'new') {
            this.dialog_show = true
            this.examplesForRowID = row.gloss_id
            if (row.lex) {this.examplesForRowR = row.gloss}
            else {this.examplesForRowR = row.gloss.toUpperCase()}
            }
          
          else {
            return false
          }
        },

        async markGlossUselessInDB(gloss_id) {
          const response = await fetch(
            'http://localhost:7000/glosses-remove',
            {
              method: 'POST',
              headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'useless_gloss_id':gloss_id}),
          })
        },

        GlossExists(gloss, index) {
          const normGloss = gloss.trim().toLowerCase()
          if (normGloss == '') {
            return true
          }
          else {
            let restOfArray = [...this.glosses]
            const GlossLex = this.glosses[index].lex
            restOfArray.splice(index, 1)
            // console.log('restofarray', restOfArray)
            for (let index = 0; index < restOfArray.length; index++) {
              const givenGloss = restOfArray[index].gloss;
              const givenLex = restOfArray[index].lex;
              if (normGloss === givenGloss && GlossLex == givenLex) {
                return true
              }
            }
            return false
          }
        },

        

        onRowEditSave(event) {
          // console.log(event)
          let { newData, index } = event;
          // console.log('field', field)
          // console.log('old row', this.glosses[index])
          // console.log('new_data', newData)
          if (this.GlossExists(newData.gloss, index)) {
            console.log('preventing save')
            // console.log('editingRows', this.editingRows)
            // console.log('newData', newData)
            this.editingRows = [...this.editingRows, newData];
            // console.log('editingRows', this.editingRows)
            return false
          }
          this.glosses[index] = newData;
          const gloss_row = JSON.stringify(this.glosses[index])
          // console.log(gloss_row)
          
          this.pushData(gloss_row
          ).then((response) => {return response}
          ).then((result) => {return result.json()}
          ).then((resulting_json) => {
            const successfulSave = resulting_json
              // console.log('action', successfulSave.action)
              // console.log('saveRes', successfulSave)
            if (successfulSave.action === 'inserted') {
              this.glosses[index].gloss_id = successfulSave.new_gloss_id
            }
          })
            
        },
        async pushData(gloss_row) {
          const response = await fetch(
          'http://localhost:7000/glosses', 
          {
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: gloss_row,
          })
          // received = await response.json()
          // console.log('received', received)
          return response
          //  received
        },
    async fetchData() {
      const response = await fetch(
          'http://localhost:7000/glosses', 
          {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
          }
          )
        const received = await response.json();
        this.glosses = received
      }
    },
    mounted() {
      this.fetchData();
    }
  };
  </script>
  
  <style></style>