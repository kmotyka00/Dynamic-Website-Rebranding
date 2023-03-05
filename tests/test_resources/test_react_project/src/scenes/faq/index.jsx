import {Box, useTheme, Typography} from '@mui/material';
import Header from '../../components/Header';
import {Accordion} from '@mui/material';
import {AccordionSummary} from '@mui/material';
import {AccordionDetails} from '@mui/material';
import { ExpandMoreOutlined } from '@mui/icons-material';
import { tokens } from '../../theme';



const FAQ = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box m='20px'>
            <Header title='FAQ' subtitle='Frequently Asked Questions'/>
            
                {[1, 2, 3, 4 , 5, 6, 7, 8].map((questionNumber) => (
                <Accordion key={questionNumber} defaultExpanded={questionNumber===3 || questionNumber === 6}>
                    <AccordionSummary expandIcon={<ExpandMoreOutlined/>}>
                        <Typography color={colors.greenAccent[500]} variant='h5'>
                            Question no.{questionNumber} 
                        </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography> 
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            ))}
        </Box>
    )
}

export default FAQ;