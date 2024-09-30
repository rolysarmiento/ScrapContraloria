import React from 'react';
import Box from '@mui/material/Box';
import SideNav from '../SideNav'

export default function Config() {
  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <SideNav />
        <h1> Configuraciones </h1>
      </Box>
    </>
  )
}
