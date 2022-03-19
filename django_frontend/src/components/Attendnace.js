import React, { useEffect, useState } from "react";
import {
     Form, FormGroup, Label, Input, 
     Button, FormFeedback 
    } from "reactstrap";
import { getTimeStamp} from "./utils";
import AttendanceCodes from "./AttendanceCodes";
import CustomModel from "./customModal";
import { useFormik } from "formik";

function AttendanceFormikForm(props) {
    // Changes the Student Input field if there's a invlaid student ID 
    const [validStudent, setValidStudent] = useState(null);
    // Opens & closes modal
    const [modal, setModal] = useState(false);
    // Updates timestamp to be current time if true
    const [timer, setTimer] = useState(true)

    // Default values
    const defaultVal = (props.formType === "CheckIn" ? "Tardy Unexcused" : "Absent Unexcused")
    const labels = (props.formType === "CheckIn" ? "Check In" : "Check Out")

    const formik = useFormik({
        initialValues: { 
        studentId: 0,
        attendanceCode: defaultVal,
        timestamp: getTimeStamp(),
        student: {}
        },
        onSubmit: values => {
            fetch('/api/student/' + values.studentId)
            .then(response => response.json())
            .then(student => {
                if (student['error']) {
                    console.log('error 69');
                    setValidStudent(true);
                }
                else {
                    values.student = student;
                    toggleModal();
                }
            })
            props.updateToken();
        }
    });

    useEffect(() => {
        // Starting timestamp clock
        const interval = setInterval(
            () => {formik.setFieldValue('timestamp', getTimeStamp())},
            1000
        )
        // Storing timer id in state
        setTimer(interval);
        return () => {clearInterval(timer);}
    }, [])

    useEffect(() => {
        // Changing the inital value of the attendance value for checkin/checkout
        formik.setFieldValue('attendanceCode', defaultVal)
    }, [defaultVal])
    
    function handleTimeChange(e) {
        clearInterval(timer);
        formik.setFieldValue('timestamp', e.target.value);
    }

    function toggleModal() {
        setModal(!modal);
    }

    const attendanceCodes = (
        <AttendanceCodes 
            value={formik.values.attendanceCode}
            onChange={formik.handleChange}         
            apiHeaders={props.apiHeaders}        
            updateToken={props.updateToken   }
        />
    )

    const handleSubmit = event => {
        // Preventing page from reloading
        event.preventDefault();

        fetch ('/api/attendance', {
            method: 'POST',
            headers: props.apiHeaders,
            body: JSON.stringify({
                student_id: formik.values.student['id'],
                begin_date: new Date(new Date().toLocaleDateString() + ' ' + formik.values.timestamp).toISOString(),
                end_date: new Date(new Date().toLocaleDateString() + ' ' +formik.values.timestamp).toISOString(),
                start_time: formik.values.timestamp,
                end_time: formik.values.timestamp,
                excuse_type: formik.values.attendanceCode,
                comment: "Testing",
                type: labels
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data['error']) {
                setValidStudent(true);
                return null
            }
            // Re-initalizing the tick
            const interval = setInterval(
                () => {formik.values.timestamp = getTimeStamp()},
                1000
            )
            setTimer(interval);
            formik.resetForm();
            toggleModal();
        })
        props.updateToken();
    }
   
    return (
        <>
        <div className="sky-form">
            <Form
            onSubmit={formik.handleSubmit}
            >
                <FormGroup>
                    <Label for="student-id">Student ID</Label>
                    <Input  
                        id="student-id"
                        name="studentId"
                        placeholder="Student ID"
                        type="number"
                        value={formik.values.studentId}
                        onChange={formik.handleChange}
                        invalid={validStudent}
                    />
                    {validStudent ?
                        <FormFeedback>
                        Invalid Student ID!
                        </FormFeedback>
                        : null
                    }
                </FormGroup>
                <FormGroup>
                    <Label for="attendanceCode">Attendance Type</Label>
                    {attendanceCodes}
                </FormGroup>
                <FormGroup>
                    <Label for="attendance-stamp">{`${labels} Time`}</Label>
                    <Input
                        id="attendance-stamp"
                        name="timestamp"
                        value={formik.values.timestamp}
                        type="time"
                        onChange={handleTimeChange}
                    />
                </FormGroup>
                <Button
                    type="submit" 
                    color="primary"
                    outline
                >
                    {labels}
                </Button>
            </Form>
            {modal ? (
                <>
                <CustomModel 
                    toggle={toggleModal} 
                    onSubmit={handleSubmit}
                    formData={formik.values}
                    formType={props.formType}
                    active={modal}
                />
                </>
            ): null
            }

        </div>       
        </>
    )   
}


export {AttendanceFormikForm}