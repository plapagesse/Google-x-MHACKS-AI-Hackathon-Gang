import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"

import "./groups.css"

function Groups() {
    const navigate = useNavigate()
    const [groupsList, setGroupsList] = useState([])
    const {userId} = useParams()
    const username = localStorage.getItem("username")

    useEffect(()=>{
      const getUserGroups=async()=>{
        const config = {
          "method":"GET",
          "url":"http://localhost:5000/fetchGroups",
          headers: {
            'Content-Type': 'application/json'
          },
          params: {
            "user_id":userId
          }
        }
        const res = await axios(config)
        setGroupsList(res.data.groups)
      }
      getUserGroups()
    },[userId])

    const handleNavigateToIndivGroup=(group)=>{
      localStorage.setItem('groupname',group.name)
      navigate(`/group/${userId}/${group._id}`)
    }

    const createGroupsDisplay=()=>{
      return(
        <div className="groups-content">
          {groupsList.map(group=>{
            return(
              <div className="groups-content-indiv" key={group._id} onClick={()=>handleNavigateToIndivGroup(group)}>
                {group.name}
              </div>
            )
          })}
        </div>
      )
    }

    return (
      <div className="groups">
        <h1 className="groups-header">
          Hi, {username}!
        </h1>
        {createGroupsDisplay()}
      </div>
    );
  }
  
  export default Groups;
  