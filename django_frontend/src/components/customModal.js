import React, { useEffect, useState } from "react";
import { 
    Form, FormGroup, Label, Input, Button,
    Modal, ModalHeader, ModalBody, ModalFooter
} from "reactstrap";
import SubmitButton from "./Submit";

function CustomModel(props) {
    let message;
    const attendanceForms = ['CheckIn', 'CheckOut']
    const student = (attendanceForms.includes(props.formType) && props.formData.student ? props.formData.student['first_name'] + ' ' + props.formData.student['last_name'] : null)
    message = `Are you sure you would like to ${props.formType}  ${student}`
    return(
        <>
            <Modal isOpen={props.active}>
                <ModalHeader
                onClick={props.toggle}
                >
                Attendance
                </ModalHeader>
                <ModalBody>
                {message}
                </ModalBody>
                <ModalFooter>
                <SubmitButton handleSubmit={props.onSubmit} />
                {' '}
                <Button 
                    onClick={props.toggle}
                    color='primary'
                    outline
                >
                    Cancel
                </Button>
                </ModalFooter>
            </Modal>
        </>
    )
}

export default CustomModel;