import React from 'react';
import { useState, useRef } from 'react';
import axios from "axios"

import "./createMeetingScreen.css"

function CreateMeeting(props) {
    const [agendaList, setAgendaList] = useState([])
    const nameRef = useRef()
    const descriptionRef = useRef()
    const meetinglinkRef = useRef()
    const meetingDateTimeRef = useRef()

    const createNewAgendaItem = () => {
        setAgendaList(prevList => [...prevList, ""])
    }

    const handleInputChange = (e, index) => {
        setAgendaList(prevList => {
            const newList = [...prevList]
            newList[index] = e.target.value
            return newList
        })
    }

    const handleRemoveAgendaItem = (index) => {
        setAgendaList(prevList => {
            const newList = [...prevList]
            newList.splice(index, 1)
            return newList
        })
    }

    const handleClose = () => {
        props.handleClose(false)
    }

    const handleSubmit = async () => {
        const params = {
            "name": nameRef.current.value,
            "description": descriptionRef.current.value,
            "meetingLink": meetinglinkRef.current.value,
            "meetingDateTime": meetingDateTimeRef.current.value,
            "agenda": [...agendaList],
            "groupId": props.groupId
        }
        const config = {
            "method": "POST",
            "url": "http://localhost:5000/createMeeting",
            headers: {
                'Content-Type': 'application/json'
            },
            data: params
        }
        await axios(config)
        window.location.reload();
    }

    return (
        <div onClick={handleClose} className='dark-background'>
            <div onClick={(e) => e.stopPropagation()} className="create-meeting">
                <h1>New Meeting</h1>
                <div className='create-meeting-inputsection'>
                    <div className='create-meeting-inputsection-indiv'>
                        <p>Name</p>
                        <input ref={nameRef} />
                    </div>
                    <div className='create-meeting-inputsection-indiv'>
                        <p>Meeting Link</p>
                        <input ref={meetinglinkRef} />
                    </div>
                </div>
                <div className='create-meeting-inputsection'>
                    <div className='create-meeting-inputsection-indiv'>
                        <p>Description</p>
                        <textarea ref={descriptionRef} />
                        <p>Meeting Date/Time</p>
                        <input ref={meetingDateTimeRef} type='datetime-local' />
                    </div>
                    <div className='create-meeting-inputsection-indiv'>
                        <p>Agenda/Tasks</p>
                        <div className='create-meeting-inputsection-agendawrapper'>
                            {
                                agendaList.map((el, index) => {
                                    console.log(index)
                                    return (
                                        <div>
                                            <input value={el} onChange={(e) => handleInputChange(e, index)} />
                                            <button onClick={() => handleRemoveAgendaItem(index)}>X</button>
                                        </div>
                                    )
                                })
                            }
                            <div onClick={() => createNewAgendaItem()} className='create-meeting-inputsection-agendawrapper-add'>{"+"}</div>
                        </div>
                    </div>
                </div>
                <div className='create-meeting-buttons'>
                    <button className='create-meeting-buttons-cancel' onClick={handleClose}>Cancel</button>
                    <button className='create-meeting-buttons-create' onClick={handleSubmit}>Create</button>
                </div>
            </div>
        </div>

    );
}

export default CreateMeeting;
