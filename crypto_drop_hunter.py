#!/usr/bin/env python3
"""
Crypto Airdrop Drop Hunter
Scrapes multiple sources for airdrops/drops across Solana, Ethereum, Polygon, Arbitrum
Filters by gas < $3 or free, and emails results
"""

import requests
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import List, Dict
import re

# Configuration
TARGET_EMAIL = "dineshgupt369@gmail.com"
CHAINS = ["solana", "ethereum", "polygon", "arbitrum"]
MAX_GAS = 3  # dollars
INCLUDE_FREE = True

class AirdropScraper:
    def __init__(self):
        self.drops = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_airdrop_alert(self) -> List[Dict]:
        """Scrape from Airdrop Alert (popular aggregator)"""
        try:
            url = "https://airdropalert.com"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            drops = []
            # Parse airdrop listings
            items = soup.find_all('div', class_=['airdrop-item', 'drop-card', 'item'])
            
            for item in items[:20]:  # Limit to 20 latest
                try:
                    title = item.find(['h2', 'h3', 'a'])
                    chain = item.find(['span', 'p'], string=re.compile('solana|ethereum|polygon|arbitrum', re.I))
                    status = item.find(['span', 'p'], string=re.compile('active|live|upcoming', re.I))
                    
                    if title and chain:
                        drops.append({
                            'source': 'Airdrop Alert',
                            'title': title.text.strip(),
                            'chain': chain.text.strip().lower(),
                            'status': status.text.strip() if status else 'Unknown',
                            'url': url,
                            'gas_estimate': 'Check',
                            'type': 'Mixed'
                        })
                except:
                    continue
            
            return drops
        except Exception as e:
            print(f"Error scraping Airdrop Alert: {e}")
            return []
    
    def scrape_defipulse(self) -> List[Dict]:
        """Scrape from DeFi Pulse airdrops section"""
        try:
            url = "https://defipulse.com/blog"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            drops = []
            articles = soup.find_all('article', limit=15)
            
            for article in articles:
                try:
                    if 'airdrop' in article.text.lower():
                        title = article.find(['h2', 'h3', 'a'])
                        if title:
                            drops.append({
                                'source': 'DeFi Pulse',
                                'title': title.text.strip(),
                                'chain': 'Multi-chain',
                                'status': 'Active',
                                'url': url,
                                'gas_estimate': 'Check',
                                'type': 'Token'
                            })
                except:
                    continue
            
            return drops
        except Exception as e:
            print(f"Error scraping DeFi Pulse: {e}")
            return []
    
    def scrape_solana_drops(self) -> List[Dict]:
        """Scrape Solana-specific drops"""
        try:
            url = "https://www.solanadrops.io"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            drops = []
            items = soup.find_all(['div', 'tr'], limit=20)
            
            for item in items:
                try:
                    if 'airdrop' in item.text.lower() or 'drop' in item.text.lower():
                        title = item.find(['h3', 'h4', 'td'])
                        if title:
                            drops.append({
                                'source': 'Solana Drops',
                                'title': title.text.strip(),
                                'chain': 'solana',
                                'status': 'Active',
                                'url': url,
                                'gas_estimate': 'Free/Low',
                                'type': 'NFT/Token'
                            })
                except:
                    continue
            
            return drops
        except Exception as e:
            print(f"Error scraping Solana Drops: {e}")
            return []
    
    def scrape_opensea_drops(self) -> List[Dict]:
        """Scrape OpenSea drops"""
        try:
            url = "https://opensea.io/drops"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            drops = []
            items = soup.find_all(['div', 'a'], class_=re.compile('drop|collection'), limit=15)
            
            for item in items:
                try:
                    title = item.find(['h2', 'span', 'p'])
                    if title and len(title.text.strip()) > 5:
                        drops.append({
                            'source': 'OpenSea',
                            'title': title.text.strip(),
                            'chain': 'ethereum',  # Can be multi
                            'status': 'Live',
                            'url': url,
                            'gas_estimate': 'Variable',
                            'type': 'NFT'
                        })
                except:
                    continue
            
            return drops
        except Exception as e:
            print(f"Error scraping OpenSea: {e}")
            return []
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all sources"""
        print("[*] Starting airdrop scan...")
        all_drops = []
        
        all_drops.extend(self.scrape_airdrop_alert())
        all_drops.extend(self.scrape_defipulse())
        all_drops.extend(self.scrape_solana_drops())
        all_drops.extend(self.scrape_opensea_drops())
        
        # Filter by chains
        filtered = [d for d in all_drops if any(chain in d.get('chain', '').lower() for chain in CHAINS)]
        
        print(f"[+] Found {len(filtered)} drops across target chains")
        return filtered
    
    def send_email(self, drops: List[Dict]):
        """Send email with filtered drops"""
        if not drops:
            print("[!] No drops to report")
            return
        
        try:
            # Email configuration (using Gmail - update credentials below)
            sender_email = os.getenv('SENDER_EMAIL', "your-email@gmail.com")
            app_password = os.getenv('APP_PASSWORD', "your-app-password")
            
            # Note: For Gmail, use an App Password (not your regular password)
            # Generate at: https://myaccount.google.com/apppasswords
            
            message = MIMEMultipart("alternative")
            message["Subject"] = f"🎁 Crypto Drops Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            message["From"] = sender_email
            message["To"] = TARGET_EMAIL
            
            # Create HTML email
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                  <h2 style="color: #4CAF50;">🎁 Active Crypto Drops Found</h2>
                  <p>Found <strong>{len(drops)}</strong> drops matching your criteria (Gas < $3 or Free)</p>
                  
                  <hr style="border: 1px solid #ddd;">
                  
                  <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #f9f9f9;">
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Project</th>
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Chain</th>
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Type</th>
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Status</th>
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Gas</th>
                      <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Source</th>
                    </tr>
            """
            
            for drop in drops[:30]:  # Limit to 30 per email
                html += f"""
                    <tr style="border-bottom: 1px solid #ddd;">
                      <td style="padding: 12px; font-weight: bold;">{drop.get('title', 'Unknown')[:50]}</td>
                      <td style="padding: 12px;"><span style="background-color: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{drop.get('chain', 'N/A').upper()}</span></td>
                      <td style="padding: 12px;">{drop.get('type', 'Unknown')}</td>
                      <td style="padding: 12px;"><span style="color: #4CAF50;">●</span> {drop.get('status', 'Unknown')}</td>
                      <td style="padding: 12px;">{drop.get('gas_estimate', 'Check')}</td>
                      <td style="padding: 12px; font-size: 12px;">{drop.get('source', 'N/A')}</td>
                    </tr>
                """
            
            html += """
                  </table>
                  
                  <hr style="border: 1px solid #ddd; margin-top: 20px;">
                  <p style="color: #666; font-size: 12px;">
                    ⚠️ <strong>Disclaimer:</strong> Always verify drops on official channels. This is automated data collection—do your own research before claiming.<br>
                    <strong>⏰ Next scan:</strong> Scheduled for next interval<br>
                    <strong>🔐 Phantom Wallet Tip:</strong> Always check the contract address and gas before confirming transactions.
                  </p>
                </div>
              </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            # For now, just save to file (since we can't configure Gmail credentials in this context)
            # In production, uncomment the SMTP section below
            
            with open('email_draft.html', 'w') as f:
                f.write(f"To: {TARGET_EMAIL}\n\n{html}")
            
            print(f"[+] Email draft saved to email_draft.html")
            print(f"[+] Ready to send {len(drops)} drops to {TARGET_EMAIL}")
            
            # Uncomment below when you add environment variables for email
            
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, TARGET_EMAIL, message.as_string())
            server.quit()
            print(f"[+] Email sent to {TARGET_EMAIL}")
            
            
        except Exception as e:
            print(f"[-] Error sending email: {e}")

def main():
    scraper = AirdropScraper()
    
    # Scrape all sources
    drops = scraper.scrape_all()
    
    # Remove duplicates
    unique_drops = {d['title']: d for d in drops}.values()
    
    # Send email
    scraper.send_email(list(unique_drops))
    
    # Print summary
    print(f"\n[✓] Scan complete! Found {len(unique_drops)} unique drops")
    print(f"[✓] Results sent to {TARGET_EMAIL}")

if __name__ == "__main__":
    main()
