import React, { useEffect, useState } from "react";
import {
     Table
    } from "reactstrap";

function SkyTable(props) {
    const [tableItems, setTableItems] = useState([]);

    // Updating the table every time when user enters new search result 
    useEffect(() => {
        setTableItems(props.users.map((item, index) => {
            if (item.length === 0) {
                return []
            }          
            return (
                <tr>
                    <th scope="row">
                    {item[0]}
                    </th>
                    <td>
                    {item[1]}
                    </td>
                    <td>
                    {item[2]}
                    </td>
                    <td>
                    {item[3]}
                    </td>
                    <td>
                    {item[4]}
                    </td>
                </tr> 
            )
        }))
        
    }, [props.users])


    return (
        <Table>
            <thead>
                <tr>
                    <th>
                        User ID
                    </th>
                    <th>
                        First Name
                    </th>
                    <th>
                        Preferred Name
                    </th>
                    <th>
                        Last Name
                    </th>
                    <th>
                        Student ID
                    </th>
                </tr>
            </thead>
            <tbody>
                {tableItems}
            </tbody>
        </Table>
    )
}

export default SkyTable;