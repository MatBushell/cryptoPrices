import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function Ticker(){
  return <h1>This is where the ticker will go...</h1>;
}

function AnotherComponent(){
  return <div>Heres another component to test</div>
}

function App() {
  return (
    <>
      <Ticker />
      <AnotherComponent />
    </>

  );

}

export default App
