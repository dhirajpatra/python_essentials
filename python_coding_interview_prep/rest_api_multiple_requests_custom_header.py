import requests
import json
import logging
from typing import List, Dict, Any, Optional
# This import is necessary for handling parallel execution of API calls
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_calls.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RESTAPIClient:
    """A client for making REST API calls with multiple system IDs."""
    
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize the REST API client.
        
        Args:
            base_url: Base URL of the API endpoint
            username: Username for authentication
            password: Password for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        # Use a session to persist settings across requests
        self.session = requests.Session()
        # Set authentication for the session
        self.session.auth = (username, password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def call_api_for_single_id(self, sys_id: str) -> Dict[str, Any]:
        """
        Call the API for a single system ID.
        
        Args:
            sys_id: The system ID to query
            
        Returns:
            Dictionary containing the response or error details
        """
        result = {
            'sys_id': sys_id,
            'success': False,
            'data': None,
            'error': None,
            'status_code': None,
            'timestamp': time.time()
        }
        
        try:
            # Construct the full URL with the system ID
            url = f"{self.base_url}/{sys_id}"
            
            # Make the API call with a timeout
            response = self.session.get(url, timeout=30)
            result['status_code'] = response.status_code
            
            if response.status_code == 200:
                try:
                    result['data'] = response.json()
                    result['success'] = True
                    logger.info(f"Successfully fetched data for sys_id: {sys_id}")
                except json.JSONDecodeError as e:
                    result['error'] = f"Invalid JSON response: {str(e)}"
                    logger.error(f"JSON decode error for sys_id {sys_id}: {str(e)}")
            else:
                result['error'] = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"API call failed for sys_id {sys_id}: {result['error']}")
                
        except requests.exceptions.Timeout:
            result['error'] = "Request timeout"
            logger.error(f"Timeout for sys_id {sys_id}")
        except requests.exceptions.ConnectionError:
            result['error'] = "Connection error"
            logger.error(f"Connection error for sys_id {sys_id}")
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request failed: {str(e)}"
            logger.error(f"Request failed for sys_id {sys_id}: {str(e)}")
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error for sys_id {sys_id}: {str(e)}")
        
        return result
    
    def call_api_for_multiple_ids(self, sys_ids: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Call the API for multiple system IDs in parallel.
        
        Args:
            sys_ids: List of system IDs to query
            max_workers: Maximum number of parallel threads
            
        Returns:
            List of response dictionaries for each system ID
        """
        results = []
        failed_ids = []
        
        logger.info(f"Starting API calls for {len(sys_ids)} system IDs")

        # Use ThreadPoolExecutor to handle parallel API calls
        # keep max_workers to a reasonable number below the number of available CPU cores to avoid overwhelming the server
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks. Builds a dictionary mapping each background Future object back to its original sys_id.
            # This keeps track of which result belongs to which ID
            future_to_sys_id = {
                # It will submit the call_api_for_single_id function for each sys_id in sys_ids
                executor.submit(self.call_api_for_single_id, sys_id): sys_id for sys_id in sys_ids
            }

            # Process completed tasks
            # Watches the tasks and yields each Future the moment its API call finishes.
            # It does not wait in order; it yields fast tasks first.
            for future in as_completed(future_to_sys_id):
                # Get the system ID associated with the completed future task
                sys_id = future_to_sys_id[future]
                print(f"*********************{sys_id}")
                try:
                    # Wait for the result with a timeout to avoid hanging indefinitely
                    result = future.result(timeout=60)
                    results.append(result)
                    
                    if not result['success']:
                        failed_ids.append(sys_id)
                        
                except Exception as e:
                    logger.error(f"Error processing sys_id {sys_id}: {str(e)}")
                    failed_ids.append(sys_id)
                    results.append({
                        'sys_id': sys_id,
                        'success': False,
                        'data': None,
                        'error': f"Processing error: {str(e)}",
                        'status_code': None,
                        'timestamp': time.time()
                    })
        
        # Log summary
        successful = len(results) - len(failed_ids)
        logger.info(f"API calls completed. Successful: {successful}, Failed: {len(failed_ids)}")
        
        if failed_ids:
            logger.warning(f"Failed system IDs: {failed_ids}")
        
        return results
    
    def call_api_sequential(self, sys_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Call the API for multiple system IDs sequentially.
        This is alternative to the parallel approach
        and can be useful for debugging or when the API has strict rate limits.
        
        Args:
            sys_ids: List of system IDs to query
            
        Returns:
            List of response dictionaries for each system ID
        """
        results = []
        
        logger.info(f"Starting sequential API calls for {len(sys_ids)} system IDs")
        
        for sys_id in sys_ids:
            result = self.call_api_for_single_id(sys_id)
            results.append(result)
            
        return results

# Initialize client
client = RESTAPIClient(
    # base_url="https://api.example.com/api/records",
    base_url="http://localhost:8000/item",
    username="Alice",
    password="secret123"
)

# You can modify the session headers
client.session.headers.update({
    'X-Custom-Header': 'custom-value',
    'API-Version': 'v2'
})

# Call API for multiple IDs
# sys_ids = ["id1", "id2", "id3", "id4"]
sys_ids = [4, 6, 7, 8, 9, 2]
results = client.call_api_for_multiple_ids(sys_ids)

# Process results
for result in results:
    if result['success']:
        print(f"✅ {result['sys_id']}: {result['data']}")
    else:
        print(f"❌ {result['sys_id']}: {result['error']}")