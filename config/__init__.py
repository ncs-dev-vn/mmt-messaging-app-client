"""
Configuration utilities for chat client
Cung cấp cấu hình với user input, network scanning và fallback values
"""

import socket
import threading
import ipaddress
import time

def get_server_info_from_user():
    """Get server information from user input with auto-discovery option"""
    print("=== Cấu hình Server ===")
    print("1. Tự động quét mạng LAN")
    print("2. Nhập thủ công")
    
    while True:
        try:
            choice = input("Chọn phương thức (1/2) [mặc định: 2]: ").strip()
            if not choice or choice == '2':
                # Manual input
                break
            elif choice == '1':
                # Auto-discovery
                result = auto_discover_servers()
                if result:
                    return result
                # If auto-discovery fails or user cancels, fall back to manual
                print("\n🔄 Chuyển sang nhập thủ công...")
                break
            else:
                print("❌ Chọn 1 hoặc 2")
        except KeyboardInterrupt:
            print("\n🔄 Chuyển sang nhập thủ công...")
            break
    
    # Manual input
    print("\n--- Nhập thủ công ---")
    
    # Input host
    host_input = input("Nhập server host [mặc định: 127.0.0.1]: ").strip()
    host = host_input if host_input else '127.0.0.1'
    
    # Input port with validation
    while True:
        port_input = input("Nhập server port [mặc định: 12345]: ").strip()
        if not port_input:
            port = 12345
            break
        try:
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            else:
                print("❌ Port phải từ 1-65535")
        except ValueError:
            print("❌ Port phải là số")
    
    print(f"✅ Sẽ kết nối tới {host}:{port}")
    return host, port

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "192.168.1.100"  # Fallback

def scan_port(host, port, timeout=1):
    """Scan a single port on a host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # True if port is open
    except:
        return False

def scan_network_for_servers(network_range=None, ports=None, timeout=1):
    """
    Scan LAN để tìm chat servers
    
    Args:
        network_range: CIDR format (e.g., '192.168.1.0/24')
        ports: List of ports to scan (default: [12345, 8080, 3000, 9999])
        timeout: Timeout per port scan (seconds)
    
    Returns:
        List of (host, port) tuples where servers are found
    """
    if ports is None:
        ports = [12345, 8080, 3000, 9999, 5000, 8000]
    
    # Auto-detect network range if not provided
    if network_range is None:
        local_ip = get_local_ip()
        # Assume /24 subnet
        network_parts = local_ip.split('.')
        network_range = f"{'.'.join(network_parts[:3])}.0/24"
    
    print(f"🔍 Đang quét mạng {network_range} trên các port {ports}...")
    print(f"⏱️  Timeout: {timeout}s per port")
    
    servers_found = []
    network = ipaddress.IPv4Network(network_range, strict=False)
    
    def scan_host_ports(host_ip):
        host_str = str(host_ip)
        for port in ports:
            if scan_port(host_str, port, timeout):
                servers_found.append((host_str, port))
                print(f"✅ Tìm thấy server: {host_str}:{port}")
    
    # Use threading for faster scanning
    threads = []
    for host_ip in network.hosts():
        thread = threading.Thread(target=scan_host_ports, args=(host_ip,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        
        # Limit concurrent threads to avoid overwhelming network
        if len(threads) >= 50:
            for t in threads:
                t.join()
            threads = []
    
    # Wait for remaining threads
    for thread in threads:
        thread.join()
    
    return servers_found

def auto_discover_servers():
    """Auto-discover chat servers in LAN"""
    print("🌐 Tự động tìm kiếm chat servers trong mạng LAN...")
    
    # Quick scan with short timeout
    servers = scan_network_for_servers(timeout=0.5)
    
    if servers:
        print(f"\n🎉 Tìm thấy {len(servers)} server(s):")
        for i, (host, port) in enumerate(servers, 1):
            print(f"   {i}. {host}:{port}")
        
        while True:
            try:
                choice = input(f"\nChọn server (1-{len(servers)}) hoặc Enter để manual: ").strip()
                if not choice:
                    return None  # User wants manual input
                
                index = int(choice) - 1
                if 0 <= index < len(servers):
                    selected = servers[index]
                    print(f"✅ Đã chọn server: {selected[0]}:{selected[1]}")
                    return selected
                else:
                    print(f"❌ Chọn từ 1 đến {len(servers)}")
            except ValueError:
                print("❌ Vui lòng nhập số")
            except KeyboardInterrupt:
                return None
    else:
        print("❌ Không tìm thấy server nào trong mạng")
        return None

def get_default_server_info():
    """Get default server information (fallback)"""
    return '127.0.0.1', 12345

def get_connection_timeout():
    """Get connection timeout"""
    return 30

def get_buffer_size():
    """Get buffer size"""
    return 1024

def get_max_nickname_length():
    """Get max nickname length"""
    return 20

def get_max_message_length():
    """Get maximum message length"""
    return 500