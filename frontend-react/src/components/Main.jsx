import React from 'react'
import Button from './Button'

const Main = () => {
  return (
    <>
        <div className='container'>
            <div className='p-5 text-center bg-light-dark rounded'>
                <h1 className='text-light'>Stock prediction portal</h1>
                <p className='text-light lead'>Discover the power of AI in the stock market with the I Know First AI Portfolio, our newly rebranded Institutional Portfolio now available to retail investors. Powered by advanced machine learning and quantitative analysis, this portfolio is designed to consistently identify high-potential stocks and deliver market-beating returns.</p>
                <Button class='btn btn-info' text='Login' />
            </div>
        </div>
    </>
  )
}

export default Main