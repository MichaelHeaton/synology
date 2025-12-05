#!/usr/bin/env python3
"""
Synology DSM API Client
Provides functions to interact with Synology DSM API
"""

import json
import sys
import urllib.parse
from typing import Dict, Optional, Any


class SynologyAPI:
    """Client for Synology DSM API"""

    def __init__(self, url: str, username: str, password: str, verify_ssl: bool = False):
        """
        Initialize Synology API client

        Args:
            url: Synology DSM URL (e.g., https://172.16.15.5:5001)
            username: DSM username
            password: DSM password
            verify_ssl: Whether to verify SSL certificates
        """
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session_id: Optional[str] = None
        self.device_id: Optional[str] = None

    def _request(self, api: str, method: str, version: int = 1,
                 params: Optional[Dict[str, Any]] = None,
                 session_required: bool = True,
                 http_method: str = 'GET') -> Dict[str, Any]:
        """
        Make a request to the Synology DSM API

        Args:
            api: API name (e.g., 'SYNO.Core.Share')
            method: Method name (e.g., 'list', 'get', 'create')
            version: API version
            params: Additional parameters
            session_required: Whether session ID is required
            http_method: HTTP method ('GET' or 'POST')

        Returns:
            JSON response as dictionary
        """
        import urllib.request
        import ssl

        # Build base URL
        base_url = f"{self.url}/webapi/entry.cgi"

        # Build query parameters
        query_params = {
            'api': api,
            'method': method,
            'version': version,
        }

        # Add session ID if required and available
        if session_required and self.session_id:
            query_params['_sid'] = self.session_id

        # Add additional parameters
        if params:
            query_params.update(params)

        # Create SSL context
        ctx = ssl.create_default_context()
        if not self.verify_ssl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        # Make request
        try:
            if http_method == 'POST':
                # POST request - send data in body
                data = urllib.parse.urlencode(query_params).encode('utf-8')
                req = urllib.request.Request(base_url, data=data, method='POST')
            else:
                # GET request - send data in URL
                url = f"{base_url}?{urllib.parse.urlencode(query_params)}"
                req = urllib.request.Request(url)

            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                return json.loads(error_body)
            except json.JSONDecodeError:
                return {'success': False, 'error': {'code': e.code, 'message': error_body}}
        except Exception as e:
            return {'success': False, 'error': {'code': -1, 'message': str(e)}}

    def login(self, session_type: str = 'Core', otp_code: Optional[str] = None,
              device_name: Optional[str] = None, device_id: Optional[str] = None) -> bool:
        """
        Authenticate with Synology DSM

        Args:
            session_type: Session type (e.g., 'FileStation', 'Core', 'DSM')
                          Default is 'Core' for administrative operations
            otp_code: 2FA code if required
            device_name: Device name for trusted device
            device_id: Device ID for trusted device

        Returns:
            True if authentication successful, False otherwise
        """
        params = {
            'account': self.username,
            'passwd': self.password,
            'format': 'sid',
            'session': session_type
        }

        if otp_code:
            params['otp_code'] = otp_code
        if device_name:
            params['device_name'] = device_name
        if device_id:
            params['device_id'] = device_id

        response = self._request('SYNO.API.Auth', 'login', version=3,
                                params=params, session_required=False)

        if response.get('success'):
            self.session_id = response.get('data', {}).get('sid')
            self.device_id = response.get('data', {}).get('did')
            return True
        else:
            error = response.get('error', {})
            print(f"Authentication failed: {error.get('code')} - {error.get('message', 'Unknown error')}")
            return False

    def logout(self) -> bool:
        """Logout from Synology DSM"""
        if not self.session_id:
            return True

        response = self._request('SYNO.API.Auth', 'logout', version=3,
                                params={}, session_required=True)
        self.session_id = None
        self.device_id = None
        return response.get('success', False)

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current logged-in user

        Returns:
            User information dictionary, or None on error
        """
        response = self._request('SYNO.Core.User', 'get', version=1,
                                params={'uid': self.username}, session_required=True)

        if response.get('success'):
            return response.get('data', {})
        else:
            error = response.get('error', {})
            print(f"Failed to get user info: {error.get('code')} - {error.get('message', 'Unknown error')}")
            return None

    def list_shares(self, additional: Optional[list] = None) -> Optional[Dict[str, Any]]:
        """
        List all shared folders

        Args:
            additional: List of additional fields to include

        Returns:
            Response dictionary with shares list, or None on error
        """
        if additional is None:
            additional = [
                "share_rights", "encryption", "is_support_acl",
                "volume_status", "owner"
            ]

        params = {
            'additional': json.dumps(additional),
            'limit': '1000',
            'offset': '0'
        }

        response = self._request('SYNO.Core.Share', 'list', version=1, params=params)

        if response.get('success'):
            return response.get('data', {})
        else:
            error = response.get('error', {})
            print(f"Failed to list shares: {error.get('code')} - {error.get('message', 'Unknown error')}")
            return None

    def get_share(self, name: str, additional: Optional[list] = None) -> Optional[Dict[str, Any]]:
        """
        Get details of a specific shared folder

        Args:
            name: Share name
            additional: List of additional fields to include

        Returns:
            Share details dictionary, or None on error
        """
        if additional is None:
            additional = [
                "share_rights", "encryption", "volume_status",
                "is_support_acl", "owner", "time_machine_quota"
            ]

        params = {
            'name': name,
            'additional': json.dumps(additional)
        }

        response = self._request('SYNO.Core.Share', 'get', version=1, params=params)

        if response.get('success'):
            return response.get('data', {})
        else:
            error = response.get('error', {})
            error_code = error.get('code', 'unknown')
            # 402 means share doesn't exist, which is fine for our use case
            if error_code == 402:
                return None  # Share doesn't exist
            print(f"Failed to get share '{name}': {error_code} - {error.get('message', 'Unknown error')}")
            return None

    def create_share(self, name: str, vol_path: str, description: str = "",
                     enable_share_quota: bool = False,
                     enable_encryption: bool = False) -> Optional[Dict[str, Any]]:
        """
        Create a new shared folder

        Args:
            name: Share name
            vol_path: Volume path (e.g., /volume1)
            description: Share description
            enable_share_quota: Enable quota
            enable_encryption: Enable encryption

        Returns:
            Response dictionary, or None on error
        """
        params = {
            'name': name,
            'vol_path': vol_path,
            'enable_share_quota': 'true' if enable_share_quota else 'false',
            'enable_encryption': 'true' if enable_encryption else 'false'
        }

        # Note: API uses 'desc' not 'description' per documentation
        if description:
            params['desc'] = description

        # Create method requires POST according to documentation
        response = self._request('SYNO.Core.Share', 'create', version=1, params=params, http_method='POST')

        # If we get 403, it might be a version issue - but let's not auto-retry
        # as that could mask other issues

        if response.get('success'):
            return response.get('data', {})
        else:
            error = response.get('error', {})
            print(f"Full API Response: {json.dumps(response, indent=2)}")
            error_code = error.get('code', 'Unknown')
            error_msg = error.get('message', 'Unknown error')
            print(f"Failed to create share '{name}': {error_code} - {error_msg}")
            return None


def main():
    """Main function with command-line interface"""
    import os
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Synology DSM API Client')
    parser.add_argument('command', choices=['list', 'create', 'get', 'check-perms'],
                       help='Command to execute: list (all shares), create (new share), get (specific share), check-perms (check user permissions)')
    parser.add_argument('--name', help='Share name (for create/get commands)')
    parser.add_argument('--volume', help='Volume path (for create command, e.g., /volume1)')
    parser.add_argument('--description', help='Share description (for create command)')

    args = parser.parse_args()

    # Try to load .env file if it exists
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            # Fallback: manually parse .env file
            print("Loading .env file manually (python-dotenv not installed)...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    # Get configuration from environment
    url = os.getenv('SYNOLOGY_URL')
    username = os.getenv('SYNOLOGY_USER')
    password = os.getenv('SYNOLOGY_PASS')
    verify_ssl = os.getenv('SYNOLOGY_VERIFY_SSL', 'false').lower() == 'true'

    # Validate required variables
    if not url or not username or not password:
        print("Error: Missing required environment variables")
        print("Required: SYNOLOGY_URL, SYNOLOGY_USER, SYNOLOGY_PASS")
        print(f"  SYNOLOGY_URL: {'✓' if url else '✗'}")
        print(f"  SYNOLOGY_USER: {'✓' if username else '✗'}")
        print(f"  SYNOLOGY_PASS: {'✓' if password else '✗'}")
        print()
        print("Create a .env file in the synology/ directory with:")
        print("  SYNOLOGY_URL=https://172.16.15.5:5001")
        print("  SYNOLOGY_USER=your-username")
        print("  SYNOLOGY_PASS=your-password")
        print("  SYNOLOGY_VERIFY_SSL=false")
        sys.exit(1)

    # Initialize client
    api = SynologyAPI(url, username, password, verify_ssl=verify_ssl)

    # Authenticate
    print("Authenticating...")
    if not api.login():
        print("Authentication failed!")
        sys.exit(1)

    print(f"✓ Authenticated successfully (Session: {api.session_id[:10]}...)")
    print()

    try:
        # Handle different commands
        if args.command == 'list':
            # List all shares
            print("Fetching all shared folders...")
            shares_data = api.list_shares()

            if not shares_data:
                print("✗ Failed to list shares")
                sys.exit(1)

            shares = shares_data.get('shares', [])
            print(f"✓ Found {len(shares)} shared folders:")
            print()

            # Print table header
            print(f"{'Name':<20} {'Volume':<15} {'Description':<40}")
            print("-" * 75)

            # Print each share
            for share in shares:
                name = share.get('name', 'N/A')
                volume = share.get('vol_path', 'N/A')
                desc = share.get('desc', '')
                print(f"{name:<20} {volume:<15} {desc:<40}")

        elif args.command == 'get':
            # Get specific share
            if not args.name:
                print("Error: --name required for 'get' command")
                sys.exit(1)

            print(f"Fetching share: {args.name}")
            share_data = api.get_share(args.name)

            if share_data:
                print(f"✓ Share found:")
                print(f"  Name: {share_data.get('name', 'N/A')}")
                print(f"  Volume: {share_data.get('vol_path', 'N/A')}")
                print(f"  Description: {share_data.get('desc', 'N/A')}")
                print(f"  UUID: {share_data.get('uuid', 'N/A')}")
            else:
                print(f"✗ Share '{args.name}' not found")
                sys.exit(1)

        elif args.command == 'create':
            # Create new share
            if not args.name:
                print("Error: --name required for 'create' command")
                sys.exit(1)
            if not args.volume:
                print("Error: --volume required for 'create' command (e.g., /volume1)")
                sys.exit(1)

            description = args.description or ''

            print(f"Creating share: {args.name}")
            print(f"  Volume: {args.volume}")
            print(f"  Description: {description or '(empty)'}")
            print()

            result = api.create_share(
                name=args.name,
                vol_path=args.volume,
                description=description
            )

            if result:
                print(f"✓ Share '{args.name}' created successfully!")
                print(f"  Response: {json.dumps(result, indent=2)}")
            else:
                print(f"✗ Failed to create share '{args.name}'")
                print()
                print("NOTE: Creating shared folders requires Administrator privileges.")
                print("The 'dms-tf-user' account needs to be in the 'administrators' group.")
                print("Check: Control Panel → User & Group → dms-tf-user → Edit → User Groups")
                sys.exit(1)

        elif args.command == 'check-perms':
            # Check user permissions/role
            print("Checking user permissions...")
            print(f"  Username: {username}")
            print()
            print("NOTE: To create shared folders, the user must be an Administrator.")
            print("Check: Control Panel → User & Group → dms-tf-user → Edit → User Groups")
            print("  → Ensure 'administrators' group is checked")
            print()
            print("Application Privileges (File Station, SMB) are for USING applications,")
            print("not for administrative actions like creating shares.")

    finally:
        # Always logout
        print()
        print("Logging out...")
        api.logout()
        print("✓ Done")


if __name__ == '__main__':
    main()

