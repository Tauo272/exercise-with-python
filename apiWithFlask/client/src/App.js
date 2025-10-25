import './App.css';
import { useState } from 'react';



function App() {
  const [text, setText] = useState("");

  function setVariable(event){
    setText(event.target.value);
  }
  function submitName(sendName){
    fetch("http://localhost:5000", {
      method : "POST",
      headers : { "Content-Type" : "application/json" },
      body : JSON.stringify({"name" : sendName})
    })
  }
  function dontChange(event){
    event.preventDefault();
  }
  return (
    <>
    <div>
      <form onSubmit={dontChange}>
        <input type='text'placeholder='Nombre' onChange={setVariable} value={text}></input>
        <button type='submit' onClick={() => submitName(text)} >submit</button>
      </form>
    </div>
    </>
  );
}

export default App;
