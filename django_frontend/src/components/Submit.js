import React, { Component } from "react";
import { Form, FormGroup, Label, Input, Button } from "reactstrap";

function SubmitButton(props) {

    return(
        <Button 
            type="submit" 
            onClick={props.handleSubmit} 
            color="primary" 
            outline
        >
            Submit
        </Button>
    )
}
export default SubmitButton;