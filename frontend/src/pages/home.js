import React from 'react';
import { useState, useEffect } from "react";
import axios from "axios"
import { useNavigate } from "react-router-dom"

import "./home.css"

function Home() {
  const [users,setUsers] = useState([])
  const navigate = useNavigate()

  useEffect(()=>{
    const fetchData = async()=>{
      const config = {
        "method":"GET",
        "url":"http://localhost:5000/fetchUsers",
        headers: {
          'Content-Type': 'application/json'
        },
      }

      const res = await axios(config)
      console.log(res.data.users)
      setUsers(res.data.users)
    }
    fetchData()  
  },[])

  const handleUserSelect=(user)=>{
    localStorage.setItem('username',user.name)
    navigate(`/groups/${user._id}`)
  }

  const usersListDisplay=()=>{
    return users.map(user=>{
      return(
        <div className='username-indiv' key={user._id} onClick={()=>handleUserSelect(user)}>
          {user.name}
        </div>
      )
    })
  }

  return (
    <div className="home">
      <h1>Users List</h1>
      {usersListDisplay()}
      <div className='username-indiv'>
          +
      </div>
    </div>
  );
}

export default Home;
