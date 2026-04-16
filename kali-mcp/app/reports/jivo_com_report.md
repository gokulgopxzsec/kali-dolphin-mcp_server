# Security Report for jivo.com

Generated: 2026-04-16 14:19:56.148286

## Recon Results
{'domain': 'jivo.com', 'subdomains': ['www.jivo.com'], 'live_hosts': ['https://www.jivo.com [\x1b[33m301\x1b[0m] [\x1b[36m301 Moved Permanently\x1b[0m] [\x1b[35mNginx,OpenResty:1.27.1.2\x1b[0m]'], 'urls': ['http://jivo.com:80/', 'http://jivo.com:80/aNTTU/?', 'http://jivo.com/favicon.ico', 'https://www.jivo.com/files/personal_data_processing_policy.pdf', 'http://jivo.com:80/gSMLP/', 'http://www.jivo.com:80/hPoQW/', 'http://jivo.com:80/KPgTe/?', 'http://jivo.com:80/KXfVe/', 'http://www.jivo.com:80/LNPKZ/RikfZ', 'http://www.jivo.com:80/NWNoZ/', 'http://www.jivo.com:80/OVKYZ', 'http://www.jivo.com:80/PhToZ', 'http://www.jivo.com:80/PYnXZ/OVKYZ', 'http://www.jivo.com:80/QSQmZ/RikfZ', 'http://www.jivo.com:80/RikfZ', 'http://www.jivo.com:80/RjLPZ/site.aspx?', 'http://jivo.com/robots.txt', 'http://jivo.com:80/RpPUT/?', 'http://jivo.com/script/jquery-1.3.1.min.js', 'http://www.jivo.com:80/site.aspx?', 'http://www.jivo.com:80/SnNUZ/', 'http://www.jivo.com:80/SSVgZ/OVKYZ', 'http://jivo.com/UbLfZ/robots.txt', 'http://www.jivo.com:80/VKeZZ/', 'http://www.jivo.com:80/XjXjZ/OVKYZ', 'http://jivo.com:80/YMSWZ/', 'http://jivo.com/YNnnZ/robots.txt', 'http://jivo.com:80/ZKhKj/?', 'http://www.jivo.com:80/ZLilZ/RikfZ', '']}

## Nuclei Results
{'status': 'failed', 'error': "Command '['C:\\\\Users\\\\gokul\\\\go\\\\bin\\\\nuclei.exe', '-u', 'jivo.com', '-severity', 'low,medium,high,critical', '-o', 'nuclei_results/jivo_com.txt']' returned non-zero exit status 1."}

## RAG Correlation
{'ids': [[]], 'embeddings': None, 'documents': [[]], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[]], 'distances': [[]]}
