import React, {  useLayoutEffect, useState } from "react";
import { Input } from "reactstrap";


function AttendanceCodes(props) {

    const [value, setValue] = useState('');
    const [listItems, setListItems] = useState([]);

    useLayoutEffect(() => {
        fetch ('api/attendance-codes')
        .then(response => response.json())
        .then(data =>{ 
            const codes = data['codes']
             setListItems(codes.map((code) => 
                <option key={code['id']} id={'attendance-code-' + code['id']}>
                    {code['name']}
                </option>
            ))
        })
        props.updateToken();
    }, [])

    return (   
        <Input
            id="attendanceCode"
            name="attendanceCode"
            type="select"
            value={props.value}
            onChange={props.onChange}
        >     
            { listItems }
        </Input>
    )
}

export default AttendanceCodes;