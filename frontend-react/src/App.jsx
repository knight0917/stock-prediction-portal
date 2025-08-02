import './assets/css/style.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Main from './components/Main'
import Register from './components/Register'
import Header from './components/header'
import Footer from './components/footer'
import Login from './components/Login'


function App() {

  return (
    <>
      <BrowserRouter>
        <Header />
          <Routes>
            <Route path='/' element={<Main />} />
            <Route path='/register' element={<Register />} />
            <Route path='/login' element={<Login />} />
          </Routes>
          <Footer />
      </BrowserRouter>
    </>
  )
}

export default App
