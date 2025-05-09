# Dark Web Crawler + Threat Intelligence Extractor

A powerful cybersecurity tool for monitoring and analyzing threats from the dark web. This project provides a secure way to crawl .onion sites, detect potential threats, and visualize the data through an intuitive dashboard.

> **Note**: The current implementation has been tested with test data only. Real-time monitoring with Tor network requires proper Tor Browser installation and configuration.

## Features

### Core Functionality
- Secure crawling of .onion sites using Tor network
- Real-time threat detection and monitoring
- Pattern-based threat identification
- Automatic data logging and storage
- Interactive dark-themed dashboard

### Threat Detection Capabilities
- Credentials and Personal Data
  - Email addresses
  - Passwords
  - Personal information
- Financial Threats
  - Credit card numbers
  - Bitcoin addresses
  - Financial fraud patterns
- Malware and Exploits
  - Malware distribution
  - Exploit kits
  - Hacking tools
- Data Leaks
  - Database dumps
  - Compromised credentials
  - Sensitive information
- Cybercrime Tools
  - Hacking services
  - Exploit marketplaces
  - Malicious software

### Dashboard Features
- Real-time threat monitoring
- Interactive statistics
- Advanced filtering options
- Time-based analysis
- Severity classification
- Detailed threat context

## Current Status

The project is currently running in test mode with the following characteristics:
- Successfully implemented and tested with sample threat data
- Dashboard fully functional with test data visualization
- Real-time monitoring capabilities implemented but not tested with actual .onion sites
- Tor network integration ready but requires Tor Browser installation for real-time operation

## Prerequisites

- Python 3.8 or higher
- Tor Browser (for real-time crawling)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Varadarsul/darkweb-threat-monitor.git
cd dark-web-crawler
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install Tor Browser:
   - Download from [Tor Project](https://www.torproject.org/download/)
   - Install and configure according to your operating system

## Project Structure

```
dark-web-crawler/
├── crawler.py           # Main crawler implementation
├── db.py               # Database management
├── tor_session.py      # Tor connection handling
├── dashboard/
│   ├── app.py         # Flask application
│   └── templates/
│       └── index.html # Dashboard interface
├── onion_sites.txt    # List of monitored .onion sites
├── test_data.py       # Test data generation
└── requirements.txt   # Project dependencies
```

## Usage

### Running the Dashboard (Test Mode)
1. Start the dashboard:
```bash
python dashboard/app.py
```
2. Access the dashboard at `http://localhost:5000`
3. View test data and dashboard functionality
4. The dashboard will show sample threats that demonstrate the system's capabilities

### Running with Real-Time Monitoring
1. Install and configure Tor Browser
2. Start Tor Browser and ensure it's running in the background
3. Start the dashboard:
```bash
python dashboard/app.py
```
4. The crawler will automatically:
   - Connect to Tor network
   - Start monitoring .onion sites
   - Detect and log threats
   - Update the dashboard in real-time

> **Important**: Real-time monitoring has not been tested yet. The system is ready for real-time operation but requires proper Tor Browser installation and configuration.

### Dashboard Features
- View total threats detected
- Filter by severity (High/Medium/Low)
- Search for specific threats
- Filter by time range (24h, 7d, 30d)
- View detailed threat information
- Monitor real-time updates

### Screenshot
![Dashboard Preview](https://github.com/Varadarsul/darkweb-threat-monitor/blob/main/Screenshot%202025-05-09%20185122.png?raw=true)

## Security Considerations

- Always use Tor Browser for accessing .onion sites
- Never share or expose your Tor connection details
- Follow ethical guidelines for dark web research
- Use the tool responsibly and legally
- Keep your system and dependencies updated

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring their use of this tool complies with applicable laws and regulations. The developers are not responsible for any misuse or damage caused by this program. 
