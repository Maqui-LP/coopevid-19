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

        <!-- Mapa -->
      <div style="height: 550px;">
        <l-map 
          style="height: 90%; width: 100%"
          :zoom="zoom"
          :center="center"
          @update:zoom="zoomUpdated"
          @update:center="centerUpdated"
          @click="setUbicacion"
        >
          <l-tile-layer :url="url" > </l-tile-layer>
          
          <l-marker :lat-lng="[form.lat,form.long ]" />
        </l-map>
      </div>
      <!-- Vue captcha Component -->
      <div class="form-row">
        <div class="form-group col-md-12">
          <vue-recaptcha
            :sitekey="form.key"
            :loadRecaptchaScript="true"
            @verify="onVerify"
            @expired="onExpired"
            ref="recaptcha"
          />
        </div>
      </div>
      <b-button type="submit" variant="primary">Enviar Solicitud</b-button>
      <b-button type="reset" variant="danger">Limpiar el Formulario</b-button>
    </b-form>
  </div>
</template>

<script>
  import VueRecaptcha from "vue-recaptcha"
  import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'
  export default {
    name:'FormularioCargaCentro',
    components: {
      LMap,
      LTileLayer,
      LMarker, 
      VueRecaptcha
    },
    data() {
      return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        zoom: 14,
        center: [-34.9187, -57.956],
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
          type_id:'',
          municipio_id:'',
          verified: false,
          key: process.env.VUE_GOOGLE_RECAPTCHA_SITE_KEY
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
        if (this.verified) {
          const requestOptions = {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.form)
          }; 
          fetch("http://localhost:5000/api/centros", requestOptions)
          .then(response => {
          if(response.status == 200){
            alert("El centro fue cargado con exito")
            this.onReset(evt)
          }else{
            alert("No fue posible realizar la carga del centro. Verifique la informacion cargada y pruebe nuevamente. En caso de persistir el problema contactese con el administrador del sitio")
          }
          })
        } else {
          alert("Es necesario validar captcha");
        }

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
        this.verified = false;
        this.$refs.recaptcha.reset();
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
      zoomUpdated(zoom) {
        this.zoom = zoom
      },
      centerUpdated(center) {
        this.center = center
      },
      setUbicacion(event){
        this.form.lat = event.latlng.lat
        this.form.long = event.latlng.lng
      },
      onVerify(response) {
      this.verified = !!response;
      },
      onExpired() {
        this.verified = false;
      }
    }
  }
</script>


<style>

</style>