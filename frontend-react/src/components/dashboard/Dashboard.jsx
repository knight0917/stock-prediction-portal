import React, {useEffect} from 'react'
// import axios from 'axios'
import axiosInstance from '../../axiosINstance'


const Dashboard = () => {
    
    useEffect(() =>{
        const fetchProtectedData = async () =>{
            try{
                const response = await axiosInstance.get('/protected-view')
                console.log('Success: ', response.data)
            }catch(error){
                console.error('Error fetching data:', error)
            }
        }
        fetchProtectedData()
    }, [])

  return (
    <>
        <h1 className='text-light container'>Dashboard</h1>
    </>
  )
}

export default Dashboard