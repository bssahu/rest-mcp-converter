#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
REST to MCP Converter

This module provides functionality to convert REST API endpoints into MCP (Microservice Control Plane)
servers using Spring Boot and Amazon Bedrock's Claude model. It analyzes REST endpoints, generates
appropriate configurations, and creates a Spring Boot project with the necessary components.

Author: Your Name
License: MIT
"""

import os
import json
import boto3
import requests
import yaml
from jinja2 import Template
from dotenv import load_dotenv
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

class RestToMcpConverter:
    """
    A converter that transforms REST API endpoints into MCP servers.
    
    This class handles the entire conversion process, from analyzing REST endpoints
    to generating a complete Spring Boot project with MCP configuration.
    
    Attributes:
        config (Dict[str, Any]): Configuration loaded from config.yaml
        bedrock: AWS Bedrock client for AI model interactions
    """

    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize the converter with configuration.

        Args:
            config_path (str): Path to the configuration file. Defaults to 'config.yaml'.
        """
        load_dotenv()
        self.config = self._load_config(config_path)
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            Dict[str, Any]: Loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the configuration file is invalid.
        """
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _call_claude(self, prompt: str) -> str:
        """
        Call Claude model via AWS Bedrock.

        Args:
            prompt (str): The prompt to send to Claude.

        Returns:
            str: Claude's response.

        Raises:
            Exception: If the API call fails.
        """
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = self.bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    def analyze_rest_endpoint(self, rest_endpoint: str) -> Dict[str, Any]:
        """
        Analyze a REST endpoint using Claude to understand its structure.

        Args:
            rest_endpoint (str): The REST endpoint to analyze.

        Returns:
            Dict[str, Any]: Analysis of the REST endpoint including methods,
                           schemas, parameters, and authentication requirements.

        Raises:
            Exception: If the analysis fails.
        """
        prompt = f"""
        Analyze this REST endpoint and provide a detailed JSON structure:
        {rest_endpoint}
        
        Include:
        1. HTTP methods supported
        2. Request/Response schemas
        3. Path parameters
        4. Query parameters
        5. Headers
        6. Authentication requirements
        
        Format the response as a valid JSON object.
        """
        
        analysis = self._call_claude(prompt)
        return json.loads(analysis)
    
    def generate_mcp_config(self, rest_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate MCP configuration based on REST analysis.

        Args:
            rest_analysis (Dict[str, Any]): Analysis of the REST endpoint.

        Returns:
            Dict[str, Any]: MCP configuration including controller structure,
                           request mappings, and security requirements.

        Raises:
            Exception: If the configuration generation fails.
        """
        prompt = f"""
        Convert this REST API analysis into a Spring Boot REST controller configuration:
        {json.dumps(rest_analysis, indent=2)}
        
        Include:
        1. Controller class structure
        2. Request mappings
        3. Method signatures
        4. Request/Response models
        5. Security requirements
        
        Format the response as a valid YAML configuration.
        """
        
        mcp_config = self._call_claude(prompt)
        return yaml.safe_load(mcp_config)
    
    def generate_spring_boot_project(self, mcp_config: Dict[str, Any], output_path: str) -> None:
        """
        Generate a Spring Boot project with MCP configuration.

        Args:
            mcp_config (Dict[str, Any]): MCP configuration.
            output_path (str): Path where the project should be generated.

        Raises:
            Exception: If project generation fails.
        """
        # Create project structure
        project_path = Path(output_path)
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generate pom.xml
        pom_template = self._load_template('templates/pom.xml.j2')
        pom_content = pom_template.render(
            project_name=self.config['project']['name'],
            version=self.config['project']['version']
        )
        
        with open(project_path / 'pom.xml', 'w') as f:
            f.write(pom_content)
        
        # Generate application.yml
        app_config_template = self._load_template('templates/application.yml.j2')
        app_config_content = app_config_template.render(
            mcp_config=mcp_config,
            server_port=self.config['server']['port']
        )
        
        config_path = project_path / 'src/main/resources'
        config_path.mkdir(parents=True, exist_ok=True)
        
        with open(config_path / 'application.yml', 'w') as f:
            f.write(app_config_content)
        
        # Generate main application class
        main_class_template = self._load_template('templates/MainApplication.java.j2')
        main_class_content = main_class_template.render(
            package_name=self.config['project']['package']
        )
        
        java_path = project_path / f"src/main/java/{self.config['project']['package'].replace('.', '/')}"
        java_path.mkdir(parents=True, exist_ok=True)
        
        with open(java_path / 'MainApplication.java', 'w') as f:
            f.write(main_class_content)
        
        # Generate REST controller
        controller_template = self._load_template('templates/RestController.java.j2')
        controller_content = controller_template.render(
            package_name=self.config['project']['package'],
            endpoints=mcp_config['endpoints']
        )
        
        with open(java_path / 'RestController.java', 'w') as f:
            f.write(controller_content)
    
    def _load_template(self, template_path: str) -> Template:
        """
        Load a Jinja2 template from file.

        Args:
            template_path (str): Path to the template file.

        Returns:
            Template: Loaded Jinja2 template.

        Raises:
            FileNotFoundError: If the template file doesn't exist.
        """
        with open(template_path, 'r') as f:
            return Template(f.read())
    
    def convert(self, rest_endpoint: str, output_path: str) -> Dict[str, Any]:
        """
        Convert a REST endpoint to an MCP server.

        Args:
            rest_endpoint (str): The REST endpoint to convert.
            output_path (str): Path where the MCP server should be generated.

        Returns:
            Dict[str, Any]: Result of the conversion including status and message.

        Raises:
            Exception: If the conversion fails.
        """
        try:
            # Analyze REST endpoint
            rest_analysis = self.analyze_rest_endpoint(rest_endpoint)
            
            # Generate MCP configuration
            mcp_config = self.generate_mcp_config(rest_analysis)
            
            # Generate Spring Boot project
            self.generate_spring_boot_project(mcp_config, output_path)
            
            return {
                'status': 'success',
                'message': f'MCP server generated successfully at {output_path}',
                'config': mcp_config
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def main():
    """Main entry point for the converter."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert REST endpoint to MCP server')
    parser.add_argument('rest_endpoint', help='REST API endpoint to convert')
    parser.add_argument('output_path', help='Output path for the MCP server')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    
    args = parser.parse_args()
    
    converter = RestToMcpConverter(args.config)
    result = converter.convert(args.rest_endpoint, args.output_path)
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main() 