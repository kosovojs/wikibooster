import React from 'react';
import { Navbar, Nav, NavDropdown, Tooltip, OverlayTrigger } from 'react-bootstrap';

const Header = (props) => {
	//
	const { isAuth, username, tasks, wikis, wiki } = props;

	const wikiLang = wiki && wiki.replace('wiki', '');

	const taskList = tasks
		.filter(item => item.hasArticles !== null)
		.map((item, key) => <NavDropdown.Item key={key} href={`#/${wiki}/task/${item.url_id}`}>{item.nav_title}</NavDropdown.Item>);

	const wikiList = wikis
		//.filter(item => item.hasArticles !== null)
		.map((item, key) => <NavDropdown.Item key={key} href={`#/${item}`}>{item}</NavDropdown.Item>);

	return <Navbar expand="lg" bg="dark" variant="dark">
		<Navbar.Brand href="#/">WikiBooster</Navbar.Brand>
		<Navbar.Toggle aria-controls="navbar-nav" />
		<Navbar.Collapse id="navbar-nav">
			<Nav>
				<NavDropdown title="Wikis" id="nav-wikis">
					{wikiList}
				</NavDropdown>
				{wiki !== null && taskList.length > 0 &&
					<NavDropdown title="Tasks" id="nav-tasks">
						{taskList}
					</NavDropdown>}
			</Nav>
			<Nav className="ml-auto">
				<OverlayTrigger
					placement="bottom"
					delay={{ show: 200 }}
					overlay={<Tooltip id="t-github">Github</Tooltip>}
				>
					<Nav.Link href="https://github.com/kosovojs/wikibooster" target="_blank" rel="noopener noreferrer"><i className="fab fa-github spaced fa-lg"></i></Nav.Link>
				</OverlayTrigger>
			</Nav>
			<Nav>
				{isAuth ? <>
					<NavDropdown title={`Hi, ${username}!`} id="nav-tasks">
						{wiki && <NavDropdown.Item href={`//${wikiLang}.wikipedia.org/wiki/Special:Contributions/${username}`}>Contributions</NavDropdown.Item>}
						<NavDropdown.Item href="/booster/logout"><i className="fas fa-sign-out-alt"></i> Logout</NavDropdown.Item>
					</NavDropdown>
				</> : <Nav.Link href="/booster/login"><i className="fas fa-sign-in-alt"></i> Login</Nav.Link>}
			</Nav>
		</Navbar.Collapse>
	</Navbar>;
};

export default Header;