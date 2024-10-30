import {Typography, Container, List, ListItem, Link} from '@mui/material';


export default function HelpPage() {
    return (
        <Container maxWidth="md" className="p-14">
            <Typography variant="h3" gutterBottom>Help Center</Typography>
            <Typography variant="body1" paragraph className="whitespace-pre-line pb-10">
                {`Welcome to the Kalimera AI Help Center. 
                Here, you can find answers to common questions, user guides, and support resources to help you get the most out of our products.`}
            </Typography>
            <Typography variant="h4" gutterBottom>Frequently Asked Questions</Typography>
            <List>
                <ListItem>How do I get started with Kalimera AI?</ListItem>
                <ListItem>What are the pricing options for your services?</ListItem>
                <ListItem>How can I contact support?</ListItem>
                <ListItem>Where can I find user guides and documentation?</ListItem>
            </List>
            <Typography variant="h4" gutterBottom>Contact Support</Typography>
            <Typography variant="body1" paragraph>
                If you need further assistance, please don't hesitate to contact our support team at <Link
                href="mailto:support@kalimera.ai">support@kalimera.ai</Link>. We're here to help you with any issues or
                questions you may have.
            </Typography>
        </Container>
    )
}

