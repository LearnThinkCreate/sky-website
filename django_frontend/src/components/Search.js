import React, {useState, useEffect} from "react";
import { useFormik } from "formik";
import { Form, FormGroup, Label, Input, Button, Row } from "reactstrap";
import SkyTable from "./SkyTable";

const UserSearch = () => {
    const [users, setUsers] = useState([]);

    const formik = useFormik({
        initialValues: { 
        first: "",
        last: "",
        gradeLevel: ""
        },
        onSubmit: values => {
            const url = '/api/student';
            let getUrl = `${url}?first_name=${values.first}&last_name=${values.last}&grade_level=${values.gradeLevel}`
            fetch(getUrl)
            .then(response => response.json())
            .then ( data => {
                setUsers(data['Result']);
            })
        }
    });


    return (
        <>
            <Form 
            onSubmit={formik.handleSubmit}
            >
            <FormGroup>
                <Label for="search-first">First Name</Label>
                <Input
                id="search-first"
                name="first"
                placeholder="Firstname"
                onChange={formik.handleChange}
                value={formik.values.first}
                />
            </FormGroup>
            <FormGroup>
                <Label for="search-last">Last Name</Label>
                <Input
                id="search-last"
                name="last"
                placeholder="Lastname"
                onChange={formik.handleChange}
                value={formik.values.last}
                />
            </FormGroup>
            <FormGroup>
                <Label for="search-gradeLevel">Grade Level</Label>
                <Input
                id="search-gradeLevel"
                name="gradeLevel"
                placeholder="Grade Level"
                type="number"
                onChange={formik.handleChange}
                value={formik.values.studentId}
                />
            </FormGroup>
            <Button 
                    type="submit" 
                    color="primary" 
                    outline
                >
                    Submit
                </Button>
            </Form>
            <Row style={{paddingTop: "30px", paddingLeft: "20px"}}>
                <SkyTable users={users} />
            </Row>
            
        </>
    );
};


export {UserSearch};