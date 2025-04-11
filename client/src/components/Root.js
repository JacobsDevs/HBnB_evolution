import React, { useState, useEffect } from 'react'

function Root() {

  const [data, setData] = useState([{}])
  /*useEffect(() => {
    fetch("/api/v1/places"
    ).then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])*/

  return (
    <>
      <div>
        <label>Search</label>
        <input type="text" />
      </div>
      <div>
        <p>Welcome to HBnB</p>
      </div>
    </>
  )
}

export default Root;

