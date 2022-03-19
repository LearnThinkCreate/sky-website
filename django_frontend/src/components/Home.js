import React, { Component } from "react";
import NavHeader from "./Navbar";
import { Container, Row, Col } from "reactstrap";
// import {AttendanceForm} from "./Attendance";
import {UserSearch} from "./Search";
import {AttendanceFormikForm} from "./Attendnace"
class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPage: "Attendance",
            formType: 'CheckIn',
            CsrfToken: document.querySelector('[name=csrfmiddlewaretoken]').value,
            userRoles: [],
            firstName: '',
            last_name: '',
            userId: '',
        }

        this.updateCsrfToken = this.updateCsrfToken.bind(this);
        this.changePage = this.changePage.bind(this);
    }
    

    componentDidMount() {
        fetch('/api/user')
        .then(response => response.json())
        .then(user =>{
            this.setState({
                userId: user['id'],
                userRoles: user['roles'],
                firstName: user['preferred_name'] === '' ? user['first_name'] : user['preferred_name'],
                lastName: user['last_name']
            })
        }
        )
        this.updateCsrfToken();
    }

    updateCsrfToken() {
        this.setState({
            CsrfToken: document.querySelector('[name=csrfmiddlewaretoken]').value
        })
    }

    changePage(page, form) {
        const formData = (page === "Attendance") ? form : '';
        this.setState({
            currentPage: page,
            formType: formData
        })
      }

    
    render () {
        // Changing page
        const page = this.state.currentPage;
        const formType = this.state.formType;
        const apiHeaders =  {
            'Accecpt': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': this.state.CsrfToken
        }
        let form;

        console.log('-------------------------')
        console.log(this.state.userRoles)
        console.log('-------------------------')
        console.log(this.state.userRoles.includes('Attendance Manager'))
        console.log('-------------------------')
        console.log(page)
        console.log('-------------------------')
        if (page === "Attendance" && this.state.userRoles.includes('Attendance Manager')) {
            if (formType === 'CheckIn') {
                form = <AttendanceFormikForm 
                updateToken={this.updateCsrfToken} 
                formType={formType}
                apiHeaders={apiHeaders}
            />
            }
            else if (formType === "CheckOut") {
                form = <AttendanceFormikForm 
                updateToken={this.updateCsrfToken} 
                formType={formType}
                apiHeaders={apiHeaders}
            />
            }
        }
        else {
            form = null
        }

        return (
        <div className="home-page">
            <NavHeader onClick={this.changePage} />
            <Container>
                <Row>
                    <Col style={{padding: "10px"}}>
                    <Row>
                        <h2>Attendance Form</h2>
                        <hr></hr>
                        {form}
                    </Row>
                        
                    </Col>
                    <Col style={{padding: "10px", borderLeft:" 2px solid black"}}>
                        <Row>
                            <h2>Student ID Lookup</h2>
                            <hr></hr>
                            <UserSearch
                                apiHeaders={apiHeaders}
                                updateToken={this.updateCsrfToken} 
                             />
                        </Row>
                    </Col>
                </Row>
            </Container>
        </div>
        )

    }
}

export default Home;