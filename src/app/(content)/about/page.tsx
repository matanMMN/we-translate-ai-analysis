import React from 'react';
import {Typography} from '@mui/material';


export default function AboutPage() {
    return (
        <div className="container h-dvh max-h-[calc(100%-180px)] px-14 overflow-y-auto flex flex-col">
            <Typography variant="h3" gutterBottom>About Kalimera AI</Typography>
            <Typography variant="body1" paragraph className="pb-10 whitespace-pre-line">
                {`Kalimera AI is a leading software company specializing in translation and machine translation solutions for businesses. 
                Our products leverage advanced AI technologies to provide accurate and efficient translation services, enabling companies to communicate seamlessly across different languages and markets.`}
            </Typography>
            <Typography variant="h4" gutterBottom>Our Mission</Typography>
            <Typography variant="body1" paragraph className="pb-10 whitespace-pre-line">
                {`Our mission is to break down language barriers and enable global communication through innovative AI-driven solutions. 
                We strive to deliver top-notch products that meet the diverse needs of our clients and help them succeed in an increasingly interconnected world.`}
            </Typography>
            <Typography variant="h4" gutterBottom>Our Team</Typography>
            <Typography variant="body1">
                {`Our team is composed of experts in artificial intelligence, linguistics, and software development, all committed to pushing the boundaries of what's possible in the field of translation technology.`}
            </Typography>
        </div>
    )
}

