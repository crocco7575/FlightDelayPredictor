import myLogo from './myLogo.webp';
import './App.css';
import FlightSearch from './components/FlightSearch';
import FlightList from './components/FlightList';
import { useState } from 'react';
import FlightMap from './components/FlightMap';
import PredictionPanel from './components/PredictionPanel';
function App() {

  //set flights as empty array
  const [flights, setFlights] = useState([])
  const [selectedFlight, setSelectedFlight] = useState(null)
  return (
    <div className="App">
      <div className='top'>
      {/* Header for website */}
      <div className="header">
        <h1>Flight Delay Predictor</h1>
        <img className='logo' src={myLogo}/>
      </div>
      
      {/* Flight search component */}
      <FlightSearch setFlights={setFlights} setSelectedFlight={setSelectedFlight}/>
      {/* Showing flight options based on inputted flight number*/}
      {selectedFlight === null ? (
          <FlightList flights={flights} setSelectedFlight={setSelectedFlight} />
        ) : (
          <div className="map-and-panel">
            <FlightMap
              originIATA={selectedFlight.origin}
              destinationIATA={selectedFlight.destination}
            />
            <PredictionPanel flight={selectedFlight} />
          </div>
        )}
      
      </div>

      
    </div>
  ); 
}

export default App;
