"""
Network scanning utilities
"""

import socket
import threading
import ipaddress

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
    try:
        network = ipaddress.IPv4Network(network_range, strict=False)
    except ValueError:
        print("❌ Network range không hợp lệ")
        return servers_found
    
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