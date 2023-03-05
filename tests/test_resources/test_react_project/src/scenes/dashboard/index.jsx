import React from 'react';
import Header from '../../components/Header';
import {Box, Button, IconButton, Typography, useTheme} from '@mui/material';
import { tokens } from '../../theme';
import { mockTransactions } from '../../data/mockData';
import { DownloadOutlined, EmailOutlined } from '@mui/icons-material';
import { Email } from '@mui/icons-material';
import { PointOfSale } from '@mui/icons-material';
import { PersonAdd } from '@mui/icons-material';
import { Traffic } from '@mui/icons-material';
import LineChart from '../../components/LineChart';
import PieChart from '../../components/PieChart';
import GeoChart from '../../components/GeographyChart';
import BarChart from '../../components/BarChart';
import StatBox from '../../components/StatBox';
import ProgressCircle from '../../components/ProgressCircle';

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  
  return (
  <Box m='20px'>
    <Box display='flex' justifyContent='space-between' alignItems='center'>
      <Header title={'DASHBOARD'} subtitle='Welcome to your dashboard'/>
    <Box>
      <Button sx={{backgroundColor: colors.blueAccent[700], color: colors.grey[100], fontSize: '14px', fontWeight: 'bold', padding: '10px 20px'}}>
        <DownloadOutlined sx={{mr: '1000px'}}/>
        Download Reports
      </Button>
    </Box>
    </Box>

    {/* Here is place for Charts and Grid using grid property and components */}
    <Box display='grid' gridTemplateColumns='repeat(12, 1fr)' gridAutoRows='130px' gap='20px'>
      {/* Row 1 Code below */}
      <Box gridColumn='span 3' backgroundColor={colors.primary[400]} display='flex' alignItems='center' justifyContent='center'>
        <StatBox title='12,111' subtitle='Emails Sent' progress='0.75' increase='+14%' icon={<EmailOutlined sx={{color: colors.greenAccent[600], fontSize: '26px'}}/>}/>
      </Box>
      <Box gridColumn='span 3' backgroundColor={colors.primary[400]} display='flex' alignItems='center' justifyContent='center'>
        <StatBox title='233,510' subtitle='Sales Obtained' progress='0.45' increase='+55%' icon={<PointOfSale sx={{color: colors.greenAccent[600], fontSize: '26px'}}/>}/>
      </Box>
      <Box gridColumn='span 3' backgroundColor={colors.primary[400]} display='flex' alignItems='center' justifyContent='center'>
        <StatBox title='233,510' subtitle='New Clients' progress='0.15' increase='+15%' icon={<PersonAdd sx={{color: colors.greenAccent[600], fontSize: '26px'}}/>}/>
      </Box>
      <Box gridColumn='span 3' backgroundColor={colors.primary[400]} display='flex' alignItems='center' justifyContent='center'>
        <StatBox title='233,510' subtitle='Sales Obtained' progress='0.80' increase='+23%' icon={<Traffic sx={{color: colors.greenAccent[600], fontSize: '26px'}}/>}/>
      </Box>

      {/* SECOND ROW - CHARTS */}
      <Box gridColumn='span 8' gridRow='span 2' backgroundColor={colors.primary[400]}>
        <Box mt='25px' p='0 30px' display='flex' justifyContent='space-between' alignItems='center'>
          <Box>
            <Typography variant='h5' fontWeight='600' color={colors.grey[100]}>
              Revenue Generated
            </Typography>
            <Typography variant='h3' fontWeight='bold' color={colors.greenAccent[500]}>
              $110,230,410
            </Typography>
          </Box>
          <Box>
            <IconButton>
              <DownloadOutlined sx={{fontSize: '26px', color: colors.greenAccent[500]}}/>
            </IconButton>
          </Box>
        </Box>
        <Box height='250px' mt='-20px'>
          <LineChart isDashboard={true}/>
        </Box>
        </Box>
        {/* Transactions HERE */}
        <Box gridColumn='span 4' gridRow='span 2' backgroundColor={colors.primary[400]} overflow='auto'>
          <Box display='flex' justifyContent='space-between' alignItems='center' borderBottom={`4px solid ${colors.primary[500]}`} color={colors.grey[100]} p='15px'>
            <Typography color={colors.grey[100]} variant='h5' fontWeight='600'>
              Recent Transaactions
            </Typography>
          </Box>
            {mockTransactions.map((transaction, index) => (
              <Box key={`${transaction.txId}-${index}`} display='flex' justifyContent='space-between' alignItems='center' borderBottom={`4px solid ${colors.primary[500]}`} color={colors.grey[100]} p='15px'>
                <Box>
                  <Typography color={colors.greenAccent[100]} variant='h5' fontWeight='600'>
                    {transaction.txId}
                  </Typography>
                  <Typography color={colors.grey[100]}>
                    {transaction.user}
                  </Typography>
                </Box>
                <Box color={colors.grey[100]}>
                  {transaction.date}
                </Box>
                <Box backgroundColor={colors.greenAccent[500]} p='5px 10px' borderRadius='4px'>
                    ${transaction.cost}
                </Box>
              </Box>
            ))}
          </Box>
          {/* ROW 3 STARTS HERE */}

          <Box gridColumn='span 4' gridRow='span 2' backgroundColor={colors.primary[400]} p='30px'>
              <Typography variant='h5' fontWeight='600'>
                  Campaign
              </Typography>
              <Box display='flex' flexDirection='column' alignItems='center' mt='25px'>
                    <ProgressCircle size='125'/>
                    <Typography variant='h5' color={colors.greenAccent[500]} sx={{marginTop: '15px'}}>
                      $33,521 revenue generated
                    </Typography>
                    <Typography>
                        Includes extra misc expenditures and costs
                    </Typography>
              </Box>
          </Box>
          {/* Bar Chart */}
          <Box gridColumn='span 4' gridRow='span 2' backgroundColor={colors.primary[400]}>
              <Typography variant='h5' fontWeight='600' sx={{padding: '30px 30px 0 30px'}}>
                  Sales quantity
              </Typography>
              <Box height='250px' mt='-20px'>
                    <BarChart isDashboard={true}/>
              </Box>
          </Box>
          {/* Geo Chart */}
          <Box gridColumn='span 4' gridRow='span 2' backgroundColor={colors.primary[400]} p='15px'>
              <Typography variant='h5' fontWeight='600' sx={{marginBottom: '15px'}}>
                  Geography Based Traffic
              </Typography>
              <Box height='210px'>
                    <GeoChart isDashboard={true}/>
              </Box>
          </Box>
        </Box>
      </Box>
  )
}

export default Dashboard;