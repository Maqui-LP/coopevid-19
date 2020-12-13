<template>
  <div class="m-5 p-5">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <div class="form-row">
        <div class="form-group col-md-6">
          <b-form-group id="input-group-1" label="Mail" label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              required
              placeholder="Ingresa un email"
            ></b-form-input>
          </b-form-group>
        </div>
        <div class="form-group col-md-6">
          <b-form-group id="input-group-2" label="Centro" label-for="input-2">
            <b-form-select id="input-2" v-model="form.centroId" required>
              <option
                v-for="each in centros"
                v-bind:key="each.id"
                v-bind:value="each.id"
              >
                {{ each.nombre }}
              </option>
            </b-form-select>
          </b-form-group>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group col-md-6">
          <b-form-group id="input-group-3" label="Fecha" label-for="input-3">
            <b-form-input
              id="input-3"
              v-model="form.fecha"
              required
              type="date"
            ></b-form-input>
          </b-form-group>
        </div>
        <div class="form-group col-md-6">
          <b-form-group id="input-group-4" label="Horario" label-for="input-4">
            <b-form-input
              id="input-4"
              v-model="form.hora"
              required
              type="time"
              min="09:00"
              max="15:30"
            ></b-form-input>
          </b-form-group>
        </div>
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

      <div class="form-row">
        <div class="form-group col-md-6">
          <b-button type="submit" variant="primary">Enviar Solicitud</b-button>
        </div>
        <div class="form-group col-md-6">
          <b-button type="reset" variant="danger"
            >Limpiar el Formulario</b-button
          >
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
import VueRecaptcha from "vue-recaptcha";

export default {
  name: "FormularioSacarTurno",
  components: {
    VueRecaptcha,
  },
  data() {
    return {
      form: {
        email: "",
        hora: "",
        fecha: "",
        centroId: null,
        key: "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
      },
      centros: [],
      show: true,
    };
  },
  beforeCreate: function() {
    fetch(`${process.env.VUE_APP_API_BASE}/centros/all`)
      .then((response) => response.json())
      .then((body) => {
        this.centros = body.centros;
      });
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      const { email, hora, fecha, centroId } = this.form;

      if (this.verified && centroId) {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, hora: `${hora}:00`, fecha }),
        };
        fetch(
          `${process.env.VUE_APP_API_BASE}/centros/${centroId}/reserva`,
          requestOptions
        ).then((response) => {
          if (response.status == 200) {
            alert("El centro fue cargado con exito");
            this.onReset(e);
          } else {
            alert(
              "No fue posible realizar la reserva del turno. Verifique la informacion cargada y pruebe nuevamente. En caso de persistir el problema contactese con el administrador del sitio"
            );
          }
        }).catch(() => {
          alert(
            "No fue posible realizar la reserva del turno. Verifique la informacion cargada y pruebe nuevamente. En caso de persistir el problema contactese con el administrador del sitio"
          );
        });
      } else {
        alert("Es necesario validar captcha");
      }
    },
    onReset(e) {
      e.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.hora = "";
      this.form.fecha = "";
      this.form.centroId = null;
      this.verified = false;
      this.$refs.recaptcha.reset();
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onVerify(response) {
      this.verified = !!response;
    },
    onExpired() {
      this.verified = false;
    },
  },
};
</script>
