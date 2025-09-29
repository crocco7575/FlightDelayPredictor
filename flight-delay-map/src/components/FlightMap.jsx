import { MapContainer, TileLayer, Marker, Polyline, Tooltip } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import L from 'leaflet'
import './FlightMap.css'
//fixing leaflet icon at each destination --> it was showing a weird default logo

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

// --------------------------------------------

function FlightMap({originIATA, destinationIATA}){
    
    const [coords, setCoords] = useState(null);
    //use effect for whenever origin and destination change
    useEffect(() => {
        const fetchCoords = async () => {
          try {
            //calling get airport coords on server
            const res = await fetch(`http://127.0.0.1:5000/api/coords?origin=${originIATA}&destination=${destinationIATA}`);
            const data = await res.json();
            setCoords(data);
          } catch (err) {
            console.error("Error fetching coordinates:", err);
          }
        };
        if (originIATA && destinationIATA) {
            fetchCoords();
          }
        }, [originIATA, destinationIATA]);
    

    if (!coords || !coords.origin || !coords.destination) {
        return null; // or return <p>Loading map...</p>
    }

    // --------------------------
    //origin and destination coordinates for the map component
    let destination = [coords.destination.lat, coords.destination.lng];
    let origin = [coords.origin.lat, coords.origin.lng];
    console.log([origin, destination]);


    
    return(
        <div>
            <h1> Flight Route</h1>
        <MapContainer center={origin} zoom={4} style={{height: "400px", width: "100%"}}> 
            <TileLayer 
              url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>' 
              opacity={1}/> 
            <TileLayer  
              url= {`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=898e6d0f0646ed4034c5c852f8c859cd`}
              attribution='&copy; <a href="https://openweathermap.org/">OpenWeather</a>'
              opacity={1}
              /> 
            <Marker position={origin}>
                <Tooltip permanent>{originIATA}</Tooltip>
            </Marker>
            <Marker position={destination}>
            <Tooltip permanent>{destinationIATA}</Tooltip>
            </Marker>
            <Polyline  positions={[origin, destination]} pathOptions={{ dashArray: '10,10' }} />
            {/* <Marker position={midpoint} icon={planeIcon} /> */}
        </MapContainer>
        </div>
    );
    
};
export default FlightMap