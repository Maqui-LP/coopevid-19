  //creo el mapa con coordenada inicial plaza moreno
  let myMap = L.map('myMap').setView([ -34.9206722, -57.9561499],13)
  //variable para la marca
  let marker;
  //link al template del mapa sacado de ngx-leaflet
  const urlOpenLayers = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

  function onMapClick(e){
    //alert("hiciste click en: " + e.latlng);
    //obtengo lat-long del evento
    const lat = e.latlng.lat;
    const long = e.latlng.lng;
    //si ya hay marcador lo elimino para no tener muchos al mismo tiempo
    if(marker){
      myMap.removeLayer(marker);
    }
    //genero el marcador y seteo el popup con la lat lng
    marker = L.marker([lat,long],{draggable:true}).bindPopup(e.latlng.toString()).openPopup().addTo(myMap);
    document.getElementById("lat").value= lat;
    document.getElementById("long").value = long;
  }
  
  myMap.on('click', onMapClick);


  L.tileLayer(urlOpenLayers,{
      maxZoom:15
  }).addTo(myMap)
