import React, { useState, useEffect } from 'react'
import { Outlet } from 'react-router'

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
        <p>Welcome to HBnB</p>
      </div>
    </>
  )
}

export default Root;

