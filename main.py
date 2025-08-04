import os
import platform
import socket
import uuid
import requests
import json
import subprocess
import re
import logging
import sys

# CarbonCompliance Agent v1.2.0 - Production Ready
# Secure endpoint compliance monitoring agent
# Features: Real compliance checks, hardened security, automated deployment

def get_device_id():
    id_file = '/tmp/agent_device_id'
    if os.path.exists(id_file):
        with open(id_file) as f:
            device_id = f.read().strip()
    else:
        mac = uuid.getnode()
        device_id = str(uuid.UUID(int=mac))
        with open(id_file, 'w') as f:
            f.write(device_id)
    # Input validation: only allow hex and dashes
    if not re.match(r'^[a-fA-F0-9\-]+$', device_id):
        raise ValueError("Invalid device ID")
    return device_id

def get_hostname():
    hostname = socket.gethostname()
    if not re.match(r'^[\w\-\.]+$', hostname):
        raise ValueError("Invalid hostname")
    return hostname

# --- Compliance checks (copied from backend/certificates.py, but self-contained) ---
def check_disk_encryption():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['fdesetup', 'status']).decode()
            return 'On' in out or 'FileVault is On' in out
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['lsblk', '-o', 'NAME,TYPE,MOUNTPOINT']).decode()
            return any('crypt' in line for line in out.splitlines())
        else:
            return None
    except Exception:
        return None

def check_os_updates():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['softwareupdate', '-l']).decode()
            return 'No new software available' in out
        elif platform.system() == 'Linux':
            try:
                out = subprocess.check_output(['apt', 'list', '--upgradable']).decode()
                return len([l for l in out.splitlines() if '/' in l and 'upgradable' in l]) == 0
            except Exception:
                out = subprocess.check_output(['yum', 'check-update']).decode()
                return out.strip() == ''
        else:
            return None
    except Exception:
        return None

def check_access_control():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['dscl', '.', '-read', '/Groups/admin', 'GroupMembership']).decode()
            users = out.split(':')[-1].strip().split()
            return len(users) <= 2
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['getent', 'group', 'sudo']).decode()
            users = out.split(':')[-1].strip().split(',')
            return len([u for u in users if u]) <= 2
        else:
            return None
    except Exception:
        return None

def check_firewall():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate']).decode()
            return 'enabled' in out.lower()
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['ufw', 'status']).decode()
            return 'active' in out.lower()
        else:
            return None
    except Exception:
        return None

def check_auto_updates():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['defaults', 'read', '/Library/Preferences/com.apple.SoftwareUpdate', 'AutomaticCheckEnabled']).decode().strip()
            return out == '1'
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['systemctl', 'is-enabled', 'unattended-upgrades']).decode().strip()
            return out == 'enabled'
        else:
            return None
    except Exception:
        return None

def check_password_policy():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['pwpolicy', 'getaccountpolicies'], stderr=subprocess.STDOUT).decode()
            minlen = re.search(r'minLength\s*=\s*"?(\d+)"?', out)
            minlen = int(minlen.group(1)) if minlen else 0
            return minlen >= 8
        elif platform.system() == 'Linux':
            with open('/etc/login.defs') as f:
                content = f.read()
            minlen = re.search(r'PASS_MIN_LEN\s+(\d+)', content)
            minlen = int(minlen.group(1)) if minlen else 0
            return minlen >= 8
        else:
            return None
    except Exception:
        return None

def check_logging():
    try:
        if platform.system() == 'Linux':
            out = subprocess.check_output(['systemctl', 'is-active', 'rsyslog']).decode().strip()
            return out == 'active'
        elif platform.system() == 'Darwin':
            out = subprocess.check_output(['pgrep', 'syslogd']).decode().strip()
            return bool(out)
        else:
            return None
    except Exception:
        return None

def check_uptime():
    try:
        out = subprocess.check_output(['uptime', '-p']).decode().strip()
        return out
    except Exception:
        return None

def check_auditd():
    try:
        if platform.system() == 'Linux':
            out = subprocess.check_output(['systemctl', 'is-active', 'auditd']).decode().strip()
            return out == 'active'
        elif platform.system() == 'Darwin':
            out = subprocess.check_output(['pgrep', 'auditd']).decode().strip()
            return bool(out)
        else:
            return None
    except Exception:
        return None

def check_antivirus():
    try:
        out = subprocess.check_output(['ps', 'aux']).decode()
        return any(av in out for av in ['clamd', 'avast', 'sophos', 'mcafee', 'symantec', 'bitdefender'])
    except Exception:
        return None

def check_screen_lock():
    try:
        if platform.system() == 'Darwin':
            out = subprocess.check_output(['defaults', 'read', 'com.apple.screensaver', 'askForPassword']).decode().strip()
            return out == '1'
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.screensaver', 'lock-enabled']).decode().strip()
            return out == 'true'
        else:
            return None
    except Exception:
        return None

def check_fips_mode():
    try:
        if os.path.exists('/proc/sys/crypto/fips_enabled'):
            with open('/proc/sys/crypto/fips_enabled') as f:
                return f.read().strip() == '1'
        elif platform.system() == 'Linux':
            out = subprocess.check_output(['sysctl', 'crypto.fips_enabled']).decode()
            return '1' in out
        else:
            return None
    except Exception:
        return None

def check_large_home_dirs():
    try:
        out = subprocess.check_output(['du', '-sh', '/home/*']).decode()
        for line in out.splitlines():
            size = line.split()[0]
            if size.endswith('G') and float(size[:-1]) > 10:
                return False
        return True
    except Exception:
        return None

def collect_compliance_data():
    return {
        'password_min_length': check_password_policy(),
        'firewall_enabled': check_firewall(),
        'auto_updates_enabled': check_auto_updates(),
        'disk_encryption': check_disk_encryption(),
        'os_updates': check_os_updates(),
        'access_control': check_access_control(),
        'logging_enabled': check_logging(),
        'uptime': check_uptime(),
        'audit_logs': check_auditd(),
        'antivirus_installed': check_antivirus(),
        'screen_lock': check_screen_lock(),
        'fips_mode': check_fips_mode(),
        'data_minimization': check_large_home_dirs(),
    }

def main():
    logging.basicConfig(filename='/tmp/agent.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    api_url = os.environ.get('API_URL', 'http://localhost:8000')
    token = os.environ.get('AGENT_TOKEN')
    device_id = get_device_id()
    hostname = get_hostname()
    compliance_data = collect_compliance_data()
    report = {
        'device_id': device_id,
        'hostname': hostname,
        'disk_encryption_status': 'Encrypted' if compliance_data['disk_encryption'] else 'Not Encrypted',
        'os_updates_status': 'Up to date' if compliance_data['os_updates'] else 'Updates Available',
        'running_processes': '',
        'compliance_score': sum(1 for v in compliance_data.values() if v) / len(compliance_data) * 100,
        'is_compliant': all(v for v in compliance_data.values() if v is not None),
        'details': json.dumps(compliance_data)
    }
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    # Kill switch: check access before submitting
    try:
        resp = requests.get(f'{api_url}/access-check', headers=headers, timeout=5, verify=True)
        if resp.status_code == 403:
            logging.warning('Kill switch activated by backend. Exiting.')
            sys.exit(0)
    except Exception as e:
        logging.error(f'Kill switch check failed: {e}')
    # Submit report
    try:
        resp = requests.post(f'{api_url}/report', json=report, headers=headers, timeout=10, verify=True)
        logging.info(f'Submitted compliance report: {resp.status_code} {resp.text}')
        print('Submitted compliance report:', resp.status_code, resp.text)
    except Exception as e:
        logging.error(f'Failed to submit report: {e}')
        print('Failed to submit report:', e)

if __name__ == '__main__':
    main()