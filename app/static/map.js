let myMap = L.map('myMap').setView([0,0],2)

const urlOpenLayers = 'https://a.tile.openstreetmap.org/${z}/${x}/${y}.png'

L.tileLayer(urlOpenLayers,{
    maxZoom:15
}).addTo(myMap)
