import React, { Component } from "react";
import { 
  Navbar, NavbarBrand, NavItem, NavLink,
  Collapse, Nav, NavbarToggler
} from "reactstrap";

function PageButton(props) {
  return (
    <NavItem>
        <NavLink onClick={props.onClick} href="#">
          {props.name}
        </NavLink>
    </NavItem>
  )
}

class NavHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isToggleOn: false
    }
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.setState(prevState => ({
      isToggleOn: !prevState.isToggleOn
    }));
  }

  renderPageButton(page, form) {
    const page_name = (form === '' ? page : form)

    return (
      <PageButton 
        name={page_name}
        onClick={() => this.props.onClick(page, form)}
      />
    );
  }

  render () {
    return (
      <div>
        <Navbar
          color="primary"
          dark
          expand="sm"
          fixed=""
        >
          <NavbarBrand href="#">
            MyTampaPrep
          </NavbarBrand>
          <NavbarToggler onClick={this.handleClick} />
          <Collapse navbar isOpen={this.state.isToggleOn}>
            <Nav
              className="me-auto"
              navbar
            >
            {this.renderPageButton('Attendance', 'CheckIn')}
            {this.renderPageButton('Attendance', 'CheckOut')}
            <NavItem>
              <NavLink href="/logout">
                  Log Out
              </NavLink>
            </NavItem>
            </Nav>
          </Collapse>
        </Navbar>
    </div>
    )
  }
}

export default NavHeader;