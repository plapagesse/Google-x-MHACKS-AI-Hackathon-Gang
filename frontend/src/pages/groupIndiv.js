import { useState, useEffect, useRef } from "react"
import { useParams } from "react-router-dom"
import ReactMarkdown from 'react-markdown';
import axios from "axios"

import CreateMeeting from "./createMeetingScreen"
import hamburgericon from "../Hamburger_icon.svg.png"
import homeicon from "../home_icon.png"
import "./groupIndiv.css"

function GroupIndiv() {
    const fileUpload = useRef()
    const { groupId } = useParams()
    const [createMessageNeverOpened, setCreateMessageNeverOpened] = useState(true)
    const [displayCreateMessage, setDisplayCreateMessage] = useState(false)
    const [displayPopup, setDisplayPopup] = useState(false)
    const [groupMembers, setGroupMembers] = useState([])
    const [meetings, setMeetings] = useState([])
    const [menuNeverOpened, setMenuNeverOpened] = useState(true)
    const [menuOpen, setMenuOpen] = useState(false)

    const [selectedMeeting, setSelectedMeeting] = useState(null)
    const [selectedTab, setSelectedTab] = useState("Summary")

    //const username = localStorage.getItem("username")
    const groupname = localStorage.getItem("groupname")

    useEffect(() => {
        const fetchData = async () => {
            const config = {
                "method": "GET",
                "url": "http://localhost:5000/fetchIndivGroup",
                headers: {
                    'Content-Type': 'application/json'
                },
                params: {
                    "group_id": groupId
                }
            }
            const res = await axios(config)
            setGroupMembers(res.data.group_info.users)
            res.data.meetings.sort((a, b) => {
                return new Date(a.meetingDateTime) - new Date(b.meetingDateTime);
            })
            for(let meeting of res.data.meetings){
                if(meeting.videolink){
                    const response = await fetch(`http://localhost:5000/getVideo?video_path=${meeting.videolink}`)
                    const videoBlob = await response.blob();
                    meeting.videolink = (URL.createObjectURL(videoBlob))
                }
            }
            setMeetings(res.data.meetings)
        }
        fetchData()
    }, [groupId])

    const createMessage = () => {
        return (
            <div className={
                `group-main-right-header-createmessage 
                ${displayCreateMessage ? "group-main-right-header-createmessage-slidein" : "group-main-right-header-createmessage-slideout"}`}>
                Create new meeting?
            </div>
        )
    }

    const handleMouseHover = () => {
        setDisplayCreateMessage(true)
        if (createMessageNeverOpened)
            setCreateMessageNeverOpened(false)
    }

    const handleMouseHover2 = () => {
        setMenuOpen(true)
        if (menuNeverOpened)
            setMenuNeverOpened(false)
    }

    const createMembersList = () => {
        return groupMembers.map(name => {
            return (
                <div className="group-members-indiv" key={name}>
                    {name}
                </div>
            )
        })
    }

    const handleSelectMeeting = (el) => {
        setSelectedMeeting(el)
    }

    const displayMeetingsMenu = () => {
        return (
            <div
                onMouseLeave={() => setMenuOpen(false)}
                className={
                    `group-main-left-expand
                    ${menuOpen ? "group-main-left-expand-slidein" : "group-main-left-expand-slideout"}
                    `
                }
            >
                <div className="group-main-left-expand-home">
                    <img src={homeicon} alt="home" />
                    Home
                </div>
                {
                    meetings.map(el => {
                        const dateTime = new Date(el.meetingDateTime);
                        const period = dateTime.getHours() < 12 ? 'am' : 'pm';
                        return (
                            <div key={el._id} className="group-main-left-expand-indiv" onClick={() => handleSelectMeeting(el)}>
                                <p><strong>{el.name}</strong></p>
                                <p>{`
                                    ${dateTime.getMonth() + 1}/${dateTime.getDate()}/${dateTime.getFullYear()}, ${dateTime.getHours() % 12 || 12}:${dateTime.getMinutes()} ${period}
                                `}</p>
                            </div>
                        )
                    })
                }
            </div>
        )
    }

    const handleFileSubmit = async () => {
        const file = fileUpload.current.files[0]
        const formData = new FormData();
        formData.append('file', file);
        const uploadUrlConfig = {
            "method": "POST",
            "url": "http://localhost:5000/handleFileUpload",
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            data: formData,
            params: {
                "meetingId": selectedMeeting._id
            }
        }
        const res = await axios(uploadUrlConfig)
        console.log(res.data)
    }

    const displayRightContent = () => {
        if (selectedMeeting) {
            const dateTime = new Date(selectedMeeting.meetingDateTime);
            const period = dateTime.getHours() < 12 ? 'am' : 'pm';
            if (selectedMeeting.videolink) {
                let content = ""
                if (selectedTab === "Summary") {
                    content = selectedMeeting.meetingSummary
                }
                if (selectedTab === "ToDo's") {
                    content = selectedMeeting.future_tasks
                }
                if (selectedTab === "Feedback") {
                    content = selectedMeeting.meetingProductivitySummary.join("\n")
                }
                if (selectedTab === "IndividualFeedback") {
                    content = selectedMeeting.memberIndivFeedback.Vara
                }
                return (
                    <div className="group-main-right-meetingindiv">
                        <div className="group-main-right-meetingindiv-left">
                            <video controls>
                                <source src={selectedMeeting.videolink} type="video/mp4" />
                                Your browser does not support the video tag.
                            </video>
                            <h1>{selectedMeeting.name} - {dateTime.getMonth() + 1}/{dateTime.getDate()}/{dateTime.getFullYear()}, {dateTime.getHours() % 12 || 12}:{dateTime.getMinutes()} {period}</h1>
                            <p>{selectedMeeting.description}</p>
                        </div>
                        <div className="group-main-right-meetingindiv-right">
                            <div className="group-main-right-content-meetingindiv-tabs">
                                <div
                                    className={selectedTab === "Summary" && "group-main-right-content-meetingindiv-tabs-selected"}
                                    onClick={() => setSelectedTab("Summary")}
                                >Summary</div>
                                <div
                                    className={selectedTab === "ToDo's" && "group-main-right-content-meetingindiv-tabs-selected"}
                                    onClick={() => setSelectedTab("ToDo's")}
                                >ToDo's</div>
                                <div
                                    className={selectedTab === "Feedback" && "group-main-right-content-meetingindiv-tabs-selected"}
                                    onClick={() => setSelectedTab("Feedback")}
                                >Feedback</div>
                                <div
                                    className={selectedTab === "IndividualFeedback" && "group-main-right-content-meetingindiv-tabs-selected"}
                                    onClick={() => setSelectedTab("IndividualFeedback")}
                                >Vara's Feedback</div>
                            </div>
                            <div className="group-main-right-content-meetingindiv-content">
                                <ReactMarkdown children={content} />
                            </div>
                        </div>

                    </div>
                )
            }
            else {
                return (
                    <div className="group-main-right-meetingUpload">
                        <h1>{selectedMeeting.name} - {dateTime.getMonth() + 1}/{dateTime.getDate()}/{dateTime.getFullYear()}, {dateTime.getHours() % 12 || 12}:{dateTime.getMinutes()} {period}</h1>
                        <p>{selectedMeeting.description}</p>
                        <input ref={fileUpload} type="file" />
                        <button onClick={handleFileSubmit}>Submit</button>
                    </div>
                )
            }
        }
        return (
            <div className="group-main-right-content">
                <div className="group-main-right-content-left">
                    <h1>Upcoming Meetings:</h1>
                    <div>

                    </div>
                </div>
                <div className="group-main-right-content-right">
                    <h1>Members:</h1>
                    <div>
                        {createMembersList()}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="group">
            {displayPopup && <CreateMeeting groupId={groupId} handleClose={setDisplayPopup} />}
            <div className="group-main">
                {!menuNeverOpened && displayMeetingsMenu()}
                <div className="group-main-left">
                    <img onMouseEnter={() => handleMouseHover2()} src={hamburgericon} alt="menu" />
                </div>
                <div className="group-main-right">
                    <div className="group-main-right-header">
                        <h1>{groupname}</h1>
                        <button onClick={() => setDisplayPopup(true)} onMouseOver={() => handleMouseHover()} onMouseOut={() => setDisplayCreateMessage(false)}>+</button>
                        {!createMessageNeverOpened && createMessage()}
                    </div>
                    {displayRightContent()}
                </div>
            </div>
        </div>
    );
}

export default GroupIndiv;
