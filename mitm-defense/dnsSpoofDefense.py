import socket
import dns.message
import dns.query
import dns.resolver
import time

def query_dns(domain, server):
    request = dns.message.make_query(domain, dns.rdatatype.A)
    response = dns.query.udp(request, server, timeout=5)
    return response

def monitor_dns(domain, server):
    prev_ips = set()
    while True:
        try:
            response = query_dns(domain, server)
            if response.answer:
                ips = {rr.to_text() for rrset in response.answer for rr in rrset}
                if not prev_ips:
                    prev_ips = ips
                elif prev_ips != ips:
                    print(f"DNS Spoofing detected! IP address for {domain} has changed.")
                    print("Previous IPs:", prev_ips)
                    print("Current IPs:", ips)
                    prev_ips = ips
                else:
                    print(f"Received valid response from {server}: {ips}")
            else:
                print(f"No valid response received from {server}")
        except dns.exception.Timeout:
            print(f"Timeout occurred while querying {server}")
        except dns.resolver.NoNameservers:
            print(f"No nameservers found for {server}")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(5)

if __name__ == "__main__":
    domain = "example.com"
    server = "8.8.8.8"
    monitor_dns(domain, server)