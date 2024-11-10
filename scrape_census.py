import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin, unquote
import time

def download_excel_file(url, save_path):
    """Download an Excel file from a given URL and save it to the specified path."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {save_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def extract_excel_links(html_content):
    """Extract Excel file URLs from JavaScript window.open() calls in HTML."""
    # Looking for patterns like: javascript:void(window.open('/path/to/file.xlsx'))
    pattern = r"window\.open\('([^']*\.xlsx)'\)"
    matches = re.findall(pattern, html_content)
    return matches

def sanitize_path(path):
    """Convert a URL path component into a safe directory name."""
    # Remove any illegal filename characters
    return re.sub(r'[<>:"/\\|?*]', '_', path)

def main():
    # Base URLs
    clusters_url = 'https://legacy.winnipeg.ca/census/2021/Clusters/default.asp'
    base_url = 'https://legacy.winnipeg.ca'
    
    # Create base directory for downloads
    base_dir = 'winnipeg_census_2021'
    os.makedirs(base_dir, exist_ok=True)
    
    try:
        # Get the main clusters page
        response = requests.get(clusters_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all cluster links
        cluster_links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'Cluster' in href and href.endswith('.asp'):
                full_url = urljoin(base_url, href)
                cluster_links.append(full_url)
        
        # Process each cluster
        for cluster_url in cluster_links:
            try:
                print(f"\nProcessing cluster: {cluster_url}")
                response = requests.get(cluster_url)
                response.raise_for_status()
                
                # Extract Excel file links
                excel_links = extract_excel_links(response.text)
                
                # Download each Excel file
                for excel_link in excel_links:
                    # Convert relative URL to absolute URL
                    full_url = urljoin(base_url, excel_link)
                    
                    # Create a directory structure that matches the URL path
                    # Decode URL-encoded characters and create safe directory names
                    path_parts = unquote(excel_link).split('/')
                    path_parts = [sanitize_path(part) for part in path_parts if part]
                    
                    # Join with the base directory
                    save_path = os.path.join(base_dir, *path_parts)
                    
                    # Download the file
                    if download_excel_file(full_url, save_path):
                        # Be nice to the server
                        time.sleep(1)
                    
            except Exception as e:
                print(f"Error processing cluster {cluster_url}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error fetching clusters page: {str(e)}")

if __name__ == "__main__":
    main()