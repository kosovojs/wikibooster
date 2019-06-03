import React from 'react';
import {Navbar, Nav, NavDropdown } from 'react-bootstrap';
import {tasks} from './config';

const Header = (props) => {
	//isAuth={isAuth} userName={userName}

	const {isAuth, userName} = props;

	const taskList = tasks.map((item, key) => <NavDropdown.Item key={key} href={`#/task/${item.id}`}>{item.navTitle}</NavDropdown.Item>);

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
	<NavDropdown title={`Sveiks, ${userName}!`} id="nav-tasks">
	<NavDropdown.Item href="/booster/logout">Iziet</NavDropdown.Item>
	</NavDropdown>
	  </div> : <Nav.Link href="/booster/login">Ienākt</Nav.Link>}
    </Nav>
</Navbar.Collapse>
</Navbar>;
};

export default Header;