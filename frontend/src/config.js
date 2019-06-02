export const tasks = [
	{id:'1', navTitle: 'DEFAULTSORT', title:'Iztrūkstošs DEFAULTSORT',description:'Šiem rakstiem visdrīzāk nepieciešams DEFAULTSORT. Pārbaudi, vai noteikts pareizi'},
	{id:'2', navTitle: 'Vienādi vārdi pēc kārtas', title:'Divi vienādi vārdi pēc kārtas',description:'Šajos rakstos kāds vārds atkārtojas divas reizes pēc kārtas, kas lielākajā daļā gadījumu nav labi!'},
	{id:'3', navTitle: 'Sekojošs', title:'Vārda "sekojošais" lietojums',description:'Šajos rakstos izmantots vārds "sekojošs", kas parasti lietots ar nozīmi "šāds"'},
	//{id:'4', navTitle: 'Infokaste', title:'Pilsētas bez infokastes',description:'Šajos rakstos par pilsētām nav pievienotas infokaste'},
];

//export const urlendpoint = 'http://127.0.0.1:5000/';


export const urlendpoint = (process.env.NODE_ENV === 'development')
    ? 'http://127.0.0.1:5000/'
	: '//tools.wmflabs.org/edgarsdev/';
//'http://127.0.0.1:5000/'