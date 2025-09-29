import './FlightSearch.css'
import {useState} from 'react'
import axios from 'axios';

function FlightSearch({setFlights, setSelectedFlight}){
    const [flightNumber, setFlightNumber] = useState('')
    const [isLoading, setIsLoading] = useState(false);
    // clean flight number to make sure it's in right format
    const handleClick = async () =>{
        setIsLoading(true)
        setSelectedFlight(null)
        let filteredNumber =flightNumber.toUpperCase()
        filteredNumber = filteredNumber.replace(/[^A-Z0-9]/g, '')
        setFlightNumber(filteredNumber)
        //update this 
        console.log(filteredNumber)  
        try {
            const res = await axios.get(`http://127.0.0.1:5000/api/flights?flightNumber=${filteredNumber}`)
            setFlights(res.data)
            console.log(res.data)  // You’ll use this later to set state
            //setFlights(res.data)
          } catch (e) {
            console.error('Error fetching flight data:', e)
          } finally {
            setIsLoading(false); // 👈 hide spinner
          }
        
    }
    return (
        <div className="input-button-container">
            <input 
                onChange={(e)=> setFlightNumber(e.target.value)}
                value={flightNumber}
                className='userInput'
                placeholder='Enter a call sign ex. DAL272'
                />
            <button onClick={handleClick} className="custom-button">Go!</button>
            {isLoading && <div className="spinner"></div>}
        </div>
    )

}
export default FlightSearch