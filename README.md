# REST to MCP Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Java Version](https://img.shields.io/badge/java-17%2B-orange.svg)](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)

This utility converts REST API endpoints into MCP (Microservice Control Plane) servers using Spring Boot and Amazon Bedrock's Claude model. It provides a seamless way to transform existing REST APIs into well-structured, secure, and monitored microservices.

## Features

- 🔄 Automatic REST endpoint analysis
- 🏗️ Spring Boot project generation
- 🔒 Built-in security with rate limiting
- 📊 Monitoring and metrics
- 🔍 Distributed tracing
- 📝 Comprehensive logging
- 🛡️ Fixed Window Counter rate limiting
- 🔄 Request/Response transformation

## Prerequisites

- Python 3.8 or higher
- Java 17 or higher
- Maven 3.6 or higher
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rest-mcp-converter.git
cd rest-mcp-converter
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

4. Set up environment variables:
```bash
export AWS_REGION=us-east-1  # or your preferred region
export MCP_ADMIN_PASSWORD=your-secure-password  # optional, defaults to 'admin'
```

## Configuration

The tool uses a `config.yaml` file for configuration. You can customize the following settings:

- Project name and version
- Server port
- MCP service configuration
- Security settings
- Logging configuration
- Monitoring and tracing settings
- Rate limiting parameters

Example configuration:
```yaml
project:
  name: mcp-server
  version: 1.0.0
  package: com.example.mcp

server:
  port: 8080

mcp:
  version: 1.0.0
  service:
    name: mcp-service
    description: "MCP Service generated from REST endpoint"
  
  security:
    enabled: true
    auth_type: "basic"
    
  rate-limiter:
    enabled: true
    max-requests-per-minute: 60
    window-size-minutes: 1
```

## Usage

1. Basic usage:
```bash
python rest_to_mcp_converter.py <rest-endpoint> <output-path>
```

Example:
```bash
python rest_to_mcp_converter.py https://api.example.com/v1/users ./output/mcp-server
```

2. Using custom configuration:
```bash
python rest_to_mcp_converter.py <rest-endpoint> <output-path> --config custom-config.yaml
```

## Generated MCP Server

The tool generates a Spring Boot project with the following features:

- Spring Boot REST controllers
- Basic authentication
- Fixed Window Counter rate limiting
- Actuator endpoints for monitoring
- Micrometer metrics
- Distributed tracing
- Configurable logging

### Running the MCP Server

1. Navigate to the generated project directory:
```bash
cd <output-path>
```

2. Build the project:
```bash
mvn clean package
```

3. Run the server:
```bash
java -jar target/mcp-server-1.0.0.jar
```

### Accessing the MCP Server

- Default port: 8080
- Default admin credentials:
  - Username: admin
  - Password: admin (or the value of MCP_ADMIN_PASSWORD)

### Monitoring and Management

The MCP server exposes several actuator endpoints:

- Health check: http://localhost:8080/actuator/health
- Metrics: http://localhost:8080/actuator/metrics
- Prometheus metrics: http://localhost:8080/actuator/prometheus

### Rate Limiting

The server implements a Fixed Window Counter algorithm for rate limiting:

- Window size: 1 minute
- Default limit: 60 requests per minute per IP
- Configurable through application.yml
- Returns 429 (Too Many Requests) when limit is exceeded

## Security Considerations

1. Change the default admin password in production
2. Configure proper authentication mechanisms
3. Use HTTPS in production
4. Implement rate limiting
5. Configure CORS appropriately
6. Regular security updates
7. Monitor rate limiting metrics

## Development

### Project Structure

```
rest-mcp-converter/
├── templates/              # Template files
│   ├── pom.xml.j2         # Maven configuration template
│   ├── application.yml.j2 # Spring Boot configuration template
│   └── *.java.j2         # Java source templates
├── rest_to_mcp_converter.py # Main converter script
├── config.yaml            # Default configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## Troubleshooting

1. AWS Bedrock Access Issues:
   - Verify AWS credentials
   - Check region configuration
   - Ensure Bedrock service is enabled

2. Build Issues:
   - Verify Java version (17+ required)
   - Check Maven installation
   - Review pom.xml for dependency issues

3. Runtime Issues:
   - Check application logs
   - Verify port availability
   - Review security configuration

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Spring Boot team for the excellent framework
- Amazon Bedrock team for the Claude model
- All contributors who have helped improve this project 