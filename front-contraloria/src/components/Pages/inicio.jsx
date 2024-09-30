import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import SideNav from '../SideNav';
import NavBar from '../NavBar';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

import axios from 'axios';

// import img from '../../../../scraping/file_img/1CHACHAPOYAS20240304223107883258.png';

const drawerWidth = 220;

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 950,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};


function Inicio() {

  const [open, setOpen] = useState(false);

  const [setdata, setData] = useState('');

  const handleOpen = (data) => {
    setOpen(true);
    setData(data);
  };

  const handleClose = () => setOpen(false);

  const [items, setItems] = useState(['0']);  
  
  useEffect(() => {
    const fetchItems = async () => {
        const response = await axios.get('http://127.0.0.1:8000/distritos/');
        setItems(response.data);      
    };
    fetchItems();
  }, []);

  return (
    <>
    
      <NavBar />
      <Box sx={{ display: 'flex' }}>     

          <SideNav />

          <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
                <TableHead>
                  <TableRow>
                    <TableCell align="center"> Distrito </TableCell>
                    <TableCell align="center"> Fecha </TableCell>
                    <TableCell align="center"> Fuente </TableCell>
                    <TableCell align="center"> OP </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {items.map(item => (
                    <TableRow key={item.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }} >
                      <TableCell component="th" scope="row">
                        {item.id_distrito}
                      </TableCell>
                      <TableCell component="th" scope="row">
                        {item.fecha_reg}
                      </TableCell>
                      <TableCell component="th" scope="row">
                        {item.fuente}
                      </TableCell>
                      <TableCell component="th" scope="row">
                        <Button onClick={() => handleOpen(item)} disableElevation variant="contained" aria-label="Disabled button group" > Ver </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>      

      </Box>



      <Modal open={open} onClose={handleClose} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description">
        <Box sx={style}>              
          
          <Typography id="modal-modal-title" variant="h6" component="h2">
            {setdata.id}
            {setdata.id_distrito}
            {setdata.captura}
            {setdata.fuente}
            {setdata.fecha_reg}
            <img src={setdata.captura} alt="Descripción de la imagen" style={{ width: '800px', height: 'auto' }} />
          </Typography>


        </Box>
      </Modal>



    </>
  )
}

export default Inicio;