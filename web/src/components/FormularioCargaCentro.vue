<template>
  <div class="m-5 p-5">

    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <!-- Nombre del centro y mail -->
      <div class="form-row">
            <div class="form-group col-md-6">
                  <b-form-group id="input-group-2" label="Nombre del centro:" label-for="input-2">
                    <b-form-input
                      id="input-2"
                      v-model="form.name"
                      required
                      placeholder="Ingresa el nombre del centro"
                    ></b-form-input>
                  </b-form-group>
            </div>    
            <div class="form-group col-md-6">
                <b-form-group
                  id="input-group-1"
                  label="Mail:"
                  label-for="input-1"
                  description="Nunca compartiremos tu direccion con terceras partes."
                >
                  <b-form-input
                    id="input-1"
                    v-model="form.mail"
                    type="mail"
                    required
                    placeholder="Ingresa un mail"
                  ></b-form-input>
                </b-form-group>
            </div>
      </div>

        <!-- Direccion y Telefono -->
      <div class="form-row">
            <div class="form-group col-md-6">
                  <b-form-group id="input-group-5" label="Direccion:" label-for="input-5">
                    <b-form-input
                      id="input-5"
                      v-model="form.address"
                      required
                      placeholder="Ingresa la direccion del centro"
                    ></b-form-input>
                  </b-form-group>
            </div>    
            <div class="form-group col-md-6">
                <b-form-group
                  id="input-group-6"
                  label="Telefono:"
                  label-for="input-6"
                >
                  <b-form-input
                    id="input-1"
                    v-model="form.phone"
                    type="text"
                    required
                    placeholder="Ingresa un telefono"
                  ></b-form-input>
                </b-form-group>
            </div>
      </div>


        <!-- Municipio y Tipo de Centro -->      
        <div class="form-row">
            <div class="form-group col-md-6">
                <b-form-group id="input-group-3" label="Tipo de centro:" label-for="input-3">
                    <b-form-select
                        id="input-3"
                        v-model="form.type_id"
                        required
                    >
                      <option v-for="each in tipos" v-bind:key="each.id" v-bind:value="each.id">
                        {{ each.tipo }}
                      </option>

                    </b-form-select>
                </b-form-group>
            </div>

            <div class="form-group col-md-6">
                <b-form-group id="input-group-4" label="Municipio:" label-for="input-4">
                    <b-form-select
                        id="input-4"
                        v-model="form.municipio_id"
                        required
                    >
                      <option v-for="each in municipios" v-bind:key="each.id" v-bind:value="each.id">
                        {{ each.name }}
                      </option>
                    </b-form-select>
                </b-form-group>            
            </div>
        </div>


        <!-- Hora de inicio y de cierre -->
      <div class="form-row">
            <div class="form-group col-md-6">
                  <b-form-group id="input-group-7" label="Hora de inicio:" label-for="input-7">
                    <b-form-input
                      id="input-7"
                      v-model="form.openHour"
                      required
                      type="time"
                    ></b-form-input>
                  </b-form-group>
            </div>    
            <div class="form-group col-md-6">
                <b-form-group
                  id="input-group-8"
                  label="Hora de cierre:"
                  label-for="input-8"
                >
                  <b-form-input
                    id="input-8"
                    v-model="form.closeHour"
                    type="time"
                    required
                  ></b-form-input>
                </b-form-group>
            </div>
      </div>



        <!-- Latitud y Longitud -->
      <div class="form-row">
            <div class="form-group col-md-6">
                  <b-form-group id="input-group-9" label="Latitud:" label-for="input-9">
                    <b-form-input
                      id="input-9"
                      v-model="form.lat"
                      required
                      placeholder="Ingresa la latitud"
                    ></b-form-input>
                  </b-form-group>
            </div>    
            <div class="form-group col-md-6">
                <b-form-group
                  id="input-group-10"
                  label="Longitud:"
                  label-for="input-10"
                >
                  <b-form-input
                    id="input-10"
                    v-model="form.long"
                    required
                    placeholder="Ingresa la longitud"
                  ></b-form-input>
                </b-form-group>
            </div>
      </div>

              <!-- Web -->
      <div class="form-row">
            <div class="form-group col-md-12">
                  <b-form-group id="input-group-11" label="Direccion web:" label-for="input-11">
                    <b-form-input
                      id="input-11"
                      v-model="form.web"
                      required
                      type="url"
                      placeholder="Ingresa la direccion web"
                    ></b-form-input>
                  </b-form-group>
            </div>    
      </div>

      <b-button type="submit" variant="primary">Enviar Solicitud</b-button>
      <b-button type="reset" variant="danger">Limpiar el Formulario</b-button>
    </b-form>
  </div>
</template>

<script>
  export default {
    name:'FormularioCargaCentro',
    data() {
      return {
        form: {
          name: '',
          mail: '',
          address:'',
          phone:'',
          openHour:'',
          closeHour:'',
          web:'',
          lat:'',
          long:'',
          type_id:null,
          municipio_id:null,
        },
        municipios:[],
        tipos:[{id: 1, tipo: "Ropa"},
               {id: 2,tipo: "Comida"},
               {id: 3, tipo: "Muebles"},
               {id: 4, tipo: "Higiene Personal"},
               {id: 5, tipo: "Higiene del Hogar"}
        ],
        show: true
      }
    },
  beforeCreate: function () {
    fetch("https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135",{
      "method": "GET",
    })
  .then(response => {
    return response.json()
    .then(body => this.municipios = body.data.Town)
  });
  },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
        const requestOptions = {
          method: "POST",
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(this.form)
        };
        fetch("http://localhost:5000/api/centros", requestOptions)
        .then(response => response.json())
        .then(data => (console.log(data)));
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.name = ''
        this.form.mail = ''
        this.form.address = ''
        this.form.phone = ''
        this.form.openHour = ''
        this.form.closeHour = ''
        this.form.web = ''
        this.form.lat = ''
        this.form.long = ''
        this.form.type_id = null
        this.form.municipio_id = null
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>


<style>

</style>