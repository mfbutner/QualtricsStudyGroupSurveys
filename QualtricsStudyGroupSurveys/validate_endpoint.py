from typing import Any
from pydantic import BaseModel, HttpUrl, field_validator

class QualtricsEndpoint(BaseModel):
    api_url: HttpUrl
    
    @field_validator('api_url')
    @classmethod
    def validate_qualtrics_url(cls, v: Any) -> HttpUrl:
        # Check scheme
        if v.scheme != "https":
            raise ValueError('URL must use HTTPS')
        
        # Define allowed hosts
        allowed_hosts = {
            "iad1.qualtrics.com", "ca1.qualtrics.com", "fra1.qualtrics.com",
            "sydney.qualtrics.com", "co1.qualtrics.com", "az1.qualtrics.com", 
            "sjc1.qualtrics.com", "gov1.qualtrics.com"
        }
        
        mock_hosts = {"stoplight.io"}
        all_valid_hosts = allowed_hosts | mock_hosts
        
        if v.host not in all_valid_hosts:
            raise ValueError(f'Host must be a valid Qualtrics datacenter or mock server: {sorted(all_valid_hosts)}')
        
        return v
    
    @property
    def is_mock_server(self) -> bool:
        """Check if this is a mock server endpoint"""
        return self.api_url.host == "stoplight.io"
    
    @property
    def base_url(self) -> str:
        """Get the base URL without path"""
        return f"{self.api_url.scheme}://{self.api_url.host}"
    
    def build_api_path(self, endpoint: str) -> str:
        """Build the full API path based on server type"""
        if self.is_mock_server:
            base_path = "/mocks/qualtricsv2/publicapidocs/60917"
        else:
            base_path = "/API/v3"
        
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        return base_path + endpoint