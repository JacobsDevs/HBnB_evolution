import React, { useState, useEffect } from 'react'

function App() {

  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/api/v1/amenities"
    ).then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
      {data.map((x, i) => (
        <p id={i}>{x.name}
          <br></br>
          {x.id}</p>
      ))
      }
    </div >
  )
}

export default App
