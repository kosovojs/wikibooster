import React from 'react';
import {Navbar, Nav, NavDropdown } from 'react-bootstrap';

const Header = (props) => {
	const {isAuth, username, tasks} = props;
	
	const taskList = tasks.map((item, key) => <NavDropdown.Item key={key} href={`#/task/${item.url_id}`}>{item.nav_title}</NavDropdown.Item>);

return <Navbar expand="lg" bg="dark" variant="dark">
<Navbar.Brand href="#/">WikiBooster</Navbar.Brand>
<Navbar.Toggle aria-controls="navbar-nav" />
<Navbar.Collapse id="navbar-nav">
  <Nav className="mr-auto">
	<NavDropdown title="Uzdevumi" id="nav-tasks">
		{taskList}
	</NavDropdown>
  </Nav>
    <Nav>
		{isAuth ? <div>
	<NavDropdown title={`Sveiks, ${username}!`} id="nav-tasks">
	<NavDropdown.Item href="/booster/logout">Iziet</NavDropdown.Item>
	</NavDropdown>
	  </div> : <Nav.Link href="/booster/login">Ienākt</Nav.Link>}
    </Nav>
</Navbar.Collapse>
</Navbar>;
};

export default Header;