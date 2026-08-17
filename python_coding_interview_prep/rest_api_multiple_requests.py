import requests
import json
import logging
from typing import List, Dict, Any, Optional
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
        self.session = requests.Session()
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
            
            # Make the API call
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
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_sys_id = {
                executor.submit(self.call_api_for_single_id, sys_id): sys_id 
                for sys_id in sys_ids
            }
            
            # Process completed tasks
            for future in as_completed(future_to_sys_id):
                sys_id = future_to_sys_id[future]
                try:
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

def process_api_responses(results: List[Dict[str, Any]]) -> None:
    """
    Process and display the API responses.
    
    Args:
        results: List of response dictionaries
    """
    print("\n" + "="*80)
    print("API CALL RESULTS")
    print("="*80)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    # Display successful responses
    print(f"\n✅ SUCCESSFUL CALLS ({len(successful)}):")
    for result in successful:
        print(f"\n  System ID: {result['sys_id']}")
        print(f"  Status: Success")
        print(f"  Status Code: {result['status_code']}")
        if result['data']:
            print(f"  Data: {json.dumps(result['data'], indent=4)}")
    
    # Display failed responses
    if failed:
        print(f"\n❌ FAILED CALLS ({len(failed)}):")
        for result in failed:
            print(f"\n  System ID: {result['sys_id']}")
            print(f"  Status: Failed")
            print(f"  Error: {result['error']}")
            if result['status_code']:
                print(f"  Status Code: {result['status_code']}")
    
    print("\n" + "="*80)
    print(f"TOTAL: {len(results)} | SUCCESS: {len(successful)} | FAILED: {len(failed)}")
    print("="*80)

def main():
    """Main function to demonstrate the API client usage."""
    
    # Example configuration - Replace with your actual values
    BASE_URL = "https://api.example.com/v1/records"  # Replace with your API URL
    USERNAME = "your_username"  # Replace with your username
    PASSWORD = "your_password"  # Replace with your password
    
    # Example system IDs - Replace with your actual system IDs
    SYSTEM_IDS = [
        "SYS001",
        "SYS002", 
        "SYS003",
        "SYS004",
        "SYS005"
    ]
    
    # Create the API client
    client = RESTAPIClient(BASE_URL, USERNAME, PASSWORD)
    
    # Choose between parallel or sequential execution
    USE_PARALLEL = True  # Set to False for sequential execution
    
    try:
        if USE_PARALLEL:
            # Parallel execution (faster for multiple IDs)
            results = client.call_api_for_multiple_ids(SYSTEM_IDS, max_workers=3)
        else:
            # Sequential execution
            results = client.call_api_sequential(SYSTEM_IDS)
        
        # Process and display results
        process_api_responses(results)
        
        # You can also save results to a file if needed
        with open('api_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            logger.info("Results saved to api_results.json")
            
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()