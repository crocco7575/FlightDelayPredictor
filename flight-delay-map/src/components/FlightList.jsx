import React from 'react';
import './FlightList.css'

function FlightList({ flights, setSelectedFlight}) {
    if (!flights|| flights.length === 0) return <p className="flight-list"> No results to show.</p>;

    return (
        <div className="flight-list">
            <h1 id="results-header"> Results</h1>
            {flights.map((flight, index) => (
                <div
                    key={index}
                    className="flight-card"
                    onClick={() => setSelectedFlight(flight)}
                >
                    <h3>{flight.flight_number}</h3>
                    <p>
                        {flight.origin} → {flight.destination}
                    </p>
                    <p>
                        {flight.date}
                    </p>
                    <p>
                        Departure: {flight.departure_time}
                    </p>
                    <p>
                        Arrival: {flight.arrival_time}
                    </p>
                    {console.log(flight)}
                    
                </div>
            ))}
            
        </div>
    );
}
export default FlightList
